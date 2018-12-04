"""

    Middleware 具体流程 ,及结合 cache_page decorator 的Django内部实现


"""


"""
    Middleware 类
"""
class MiddlewareMixin:
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class UpdateCacheMiddleware(MiddlewareMixin):
    """
    Response-phase cache middleware that updates the cache if the response is
    cacheable.

    Must be used as part of the two-part update/fetch cache middleware.
    UpdateCacheMiddleware must be the first piece of middleware in MIDDLEWARE
    so that it'll get called last during the response phase.
    """
    def __init__(self, get_response=None):
        self.cache_timeout = settings.CACHE_MIDDLEWARE_SECONDS
        self.key_prefix = settings.CACHE_MIDDLEWARE_KEY_PREFIX
        self.cache_alias = settings.CACHE_MIDDLEWARE_ALIAS
        self.cache = caches[self.cache_alias]
        self.get_response = get_response

    def _should_update_cache(self, request, response):
        return hasattr(request, '_cache_update_cache') and request._cache_update_cache

    def process_response(self, request, response):
        """Set the cache, if needed."""
        pass


class FetchFromCacheMiddleware(MiddlewareMixin):
    """
    Request-phase cache middleware that fetches a page from the cache.

    Must be used as part of the two-part update/fetch cache middleware.
    FetchFromCacheMiddleware must be the last piece of middleware in MIDDLEWARE
    so that it'll get called last during the request phase.
    """
    def __init__(self, get_response=None):
        self.key_prefix = settings.CACHE_MIDDLEWARE_KEY_PREFIX
        self.cache_alias = settings.CACHE_MIDDLEWARE_ALIAS
        self.cache = caches[self.cache_alias]
        self.get_response = get_response

    def process_request(self, request):
        pass

class CacheMiddleware(UpdateCacheMiddleware, FetchFromCacheMiddleware):
    """
    Cache middleware that provides basic behavior for many simple sites.

    Also used as the hook point for the cache decorator, which is generated
    using the decorator-from-middleware utility.
    """
    def __init__(self, get_response=None, cache_timeout=None, **kwargs):
        self.get_response = get_response


def make_middleware_decorator(middleware_class):
    def _make_decorator(*m_args, **m_kwargs):
        middleware = middleware_class(*m_args, **m_kwargs)

        def _decorator(view_func):
            @wraps(view_func)
            def _wrapped_view(request, *args, **kwargs):
                if hasattr(middleware, 'process_request'):
                    result = middleware.process_request(request)
                    if result is not None:
                        return result
                if hasattr(middleware, 'process_view'):
                    result = middleware.process_view(request, view_func, args, kwargs)
                    if result is not None:
                        return result
                try:
                    response = view_func(request, *args, **kwargs)
                except Exception as e:
                    if hasattr(middleware, 'process_exception'):
                        result = middleware.process_exception(request, e)
                        if result is not None:
                            return result
                    raise
                if hasattr(response, 'render') and callable(response.render):
                    if hasattr(middleware, 'process_template_response'):
                        response = middleware.process_template_response(request, response)
                    # Defer running of process_response until after the template
                    # has been rendered:
                    if hasattr(middleware, 'process_response'):
                        def callback(response):
                            return middleware.process_response(request, response)
                        response.add_post_render_callback(callback)
                else:
                    if hasattr(middleware, 'process_response'):
                        return middleware.process_response(request, response)
                return response
            return _wrapped_view
        return _decorator
    return _make_decorator


def decorator_from_middleware_with_args(middleware_class):
    """
    Like decorator_from_middleware, but return a function
    that accepts the arguments to be passed to the middleware_class.
    Use like::

         cache_page = decorator_from_middleware_with_args(CacheMiddleware)
         # ...

         @cache_page(3600)
         def my_view(request):
             # ...
    """
    return make_middleware_decorator(middleware_class)


def cache_page(timeout, *, cache=None, key_prefix=None):
    """
    Decorator for views that tries getting the page from the cache and
    populates the cache if the page isn't in the cache yet.

    The cache is keyed by the URL and some data from the headers.
    Additionally there is the key prefix that is used to distinguish different
    cache areas in a multi-site setup. You could use the
    get_current_site().domain, for example, as that is unique across a Django
    project.

    Additionally, all headers from the response's Vary header will be taken
    into account on caching -- just like the middleware does.
    """

    """
        decorator(MiddlewareClass)(MiddlewareClassParams)
    """
    return decorator_from_middleware_with_args(CacheMiddleware)(
        cache_timeout=timeout, cache_alias=cache, key_prefix=key_prefix
    )
