"""
class based view :

Mixin和View的职能区分为：
    Mixin提供数据
    View提供模板和渲染
    所以一般get_context_data在Mixin中，get(),post(),head()在View中
    Mixin和View不是能随意组合的，必须要注意他们之间的方法的解析顺序，也就是MRO(method resolution order)

ContextMixin：直接就是一个get_context_data，用于返回context数据
View：会调用所有的get方法，post方法，具体是这些['get', 'post', 'put', 'delete', 'head', 'options', 'trace']
View中是没有返回一个response的，所以光继承View的话，必须要重写get等，以返回一个response
TemplateResponseMixin：故名思议，这个Mixin会加入Template的基本信息，也就是template的名字。但是光有Template信息是没有用的，因为她没有跟View想联系起来，如果想要跟View联系起来的话必须想办法把render_to_response插进MRO的调用顺序，而且TemplateResponseMixin是没有context的信息的

看了上面的三个类我们基本上能有一个清晰的认识了，Django中Mixin和View把原来的试图函数中的三个东西分开了，模板（TemplateResponseMixin），上下文数据（ContextMixin），负责将这些联系起来的一个东西（View）

TemplateView：TemplateView就继承自TemplateResponseMixin，ContextMixin以及View，所以它的调用思路就很明确了，在其中定义一个get方法，然后通过get方法去将上面的三个东西联系在一起.我们可以看一下TemplateView的源代码

Django 的URL 解析器将请求和关联的参数发送给一个可调用的函数而不是一个类，所以基于类的视图有一个as_view() 类方法用来作为类的可调用入口。

如果该方法没有定义则引发HttpResponseNotAllowed

====>>>> STEPS
step1. View类提供类方法as_view(),用于调用dipatch()，根据request类型分发给get，post...等对应方法处理。

step2. ContextMixin类，get_context_data(self, **kwargs)获取上下文数据，如果对数据库进行操作均可以继承该类，然后将增删改查的结果放入上下文数据中（即重写get_context_data）

step3. TemplateResponseMixin类，将内容渲染到指定模板上，通过render_to_response()方法实现对应功能
"""
from django.http import HttpResponse

# path:django.views.generic.base  
class View:
    """
    Intentionally simple parent class for all views. Only implements
    dispatch-by-method and simple sanity checking.
    """

    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    def __init__(self, **kwargs):
        """
        Constructor. Called in the URLconf; can contain helpful extra
        keyword arguments, and other things.
        """
        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classonlymethod
    def as_view(cls, **initkwargs):
        """Main entry point for a request-response process."""
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError("You tried to pass in the %s method name as a "
                                "keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError("%s() received an invalid keyword %r. as_view "
                                "only accepts arguments that are already "
                                "attributes of the class." % (cls.__name__, key))

        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.request = request
            self.args = args
            self.kwargs = kwargs
            return self.dispatch(request, *args, **kwargs)
        view.view_class = cls
        view.view_initkwargs = initkwargs

        
        """
        update_wrapper 函数可以把一个函数的属性去修饰另一个对象
        通过传入不同的view类,获取cls的信息去装饰最后返回的view函数,从而将当前类的信息传递给view函数
        """
        """
        第一个函数主要是修改 __module__  __name__ __doc__ 信息
        """
        # take name and docstring from class
        update_wrapper(view, cls, updated=())
        """
        下面的函数则是修改__dict__属性
        我们可以通过装饰cls.dpatch方法,去赋予一下属性, 比如我们要关闭csrf_token这种,则可以装饰dispatch方法
        然后通过下面的步骤来将对应的属性传递到view函数
        csrf_exempt其实也只是给当前的view函数增加一个属性,然后csrf_token的中间件里面会获取对应的属性,
        从而实现对指定的view不需要csrf验证下效果
        """
        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        return view

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        """
        获取对应的http方法,来获取到对应处理函数,进行对应逻辑的处理
        所以上面的csrf_exxmpt方法你装饰到具体的http请求处理函数上面,并不会有作用,因为它还没产生
        """
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        logger.warning(
            'Method Not Allowed (%s): %s', request.method, request.path,
            extra={'status_code': 405, 'request': request}
        )
        return HttpResponseNotAllowed(self._allowed_methods())

    def options(self, request, *args, **kwargs):
        """Handle responding to requests for the OPTIONS HTTP verb."""
        response = HttpResponse()
        response['Allow'] = ', '.join(self._allowed_methods())
        response['Content-Length'] = '0'
        return response

    def _allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]


class TemplateView(TemplateResponseMixin, ContextMixin, View):
    """
    A view that renders a template.  This view will also pass into the context
    any keyword arguments passed by the url conf.
    """
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


## HttpResponse 方法实现
class JSONResponse(HttpResponse):
    """ 
    return a JSON serialized HTTP response
    """

    def __int__(self, request, data, status=200):
        serialized = json.dumps(data)
        super(JSONResponse, self).__init__(
            content=serialized,
            content_type="application/json",
            status=status
        )

class JSONViewMixin(object):
    """
    add this mixin to a Django CBV subclass to easilly return JSON data
    """
    def json_response(self, data, status=200):
        return JSONResponse(self.request, data, status=200)



# =====   https://www.zhihu.com/question/25339933   CBV 用法
### 实现返回json数据
class JSONResponseMixin(object):
    """Json mixin
    """
    def render_to_response(self, context):
        return self.get_json_response(self.convert_context_to_json(context))
    
    def get_json_response(self, context, **httpresponse_kwargs)
        return HttpResponse(content,
                            content_type='application/json'),
                            **httpresponse_kwargs)
    
    def convert_context_to_json(self, context):
        return json.dumps(context)


#用法:
class CheckRemindUtilView(JSONResponseMixin, ListView):
    """
    check if there is reminder need to be reminded
    this view should be called every minute
    """
    def get_queryset(self):
        start = timezone.now()
        end = start + datetime.timedelta(minutes=1)
        return Reminder.objects.filter(next_t__gte=start,
                                       next_t__lte=end,
                                       is_valid=True)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        if (self.get_paginate_by(self.object_list) is not None
                and hasattr(self.object_list, 'exists')):
            is_empty = not self.object_list.exists()
        else:
            is_empty = len(self.object_list) == 0
        if is_empty:
            ret = {'code': 42, 'msg': 'empty'}
        else:
            for object_ in self.object_list:
                code = exec_remind(object_)
                object_.previous_t = object_.next_t
                update_reminder(object_)
            ret = {'code': code, 'msg': 'reminded.'}
        return self.render_to_response(ret)


class PrivateObjectMixin(object):
    """filter private object for request.user"""

    def filte_private(self, queryset):
        """filte private object for authentucated user"""
        ordering = getattr(self, 'ordering', '-date_created')
        if not hasattr(self, 'request'):
            return queryset
        if not hasattr(self.request, 'user'):
            return queryset
        if self.request.user.is_authenticated():
            queryset = queryset.filter(Q(is_valid=True), Q(is_private=True) &
                                       Q(user__id=self.request.user.id) |
                                       Q(is_private=False))
        else:
            queryset = queryset.filter.(is_valid=True, is_private=False)
        try:
            result = queryset.order_by(ordering)
        except FieldError:
            """the model doesnot have an 'ordering' field """
            return queryset
        return queryset

class NoteListView(PrivateObjectMixin, BaseNoteListView):
    """show note list"""

    def get_queryset(self):
        '''
        get notes
        '''
        queryset=Note.object.all()
        return filte_private(queryset)
