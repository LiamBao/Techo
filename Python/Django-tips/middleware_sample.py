"""
统计每次页面访问的消耗时间,
也就是wsgi接口或者socket接口接到请求,到最终返回的时间.
"""

import time

from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse

class TimeBenchMarkMiddleware(MiddlewareMixin):
    """
    - process_request : 一个请求来到 middleware层,进入的第一个方法. 
            一般可以在这里做一些校验,登录或者HTTP是否有认证头之类的.
            这个方法需要两种返回值, HttpResponse/None
            如果返回的是HttpResponse,接下来的处理方法是 process_response其他的方法将不会执行
            需要注意的是,如果你的middleware在setting配置的MIDDLEWARE_CLASS的第一个的话,那么
            剩下的middleware也不会执行.
            如果返回None,Django会继续执行其他的方法
    """
    def process_requests(self, request):
        return


    """
    - process_view :这个方法是在process_request之后执行的,其中的func就是我们要执行的view方法,
            所以我们要统计一个view的执行时间,可以添加在此处.
            他的返回值和 process_request 一样,逻辑也是一样.
            如果返回None,Django会执行view函数从而得到最终的response
    """
    def process_view(self, request, func, *args, **kwargs):
        if request.path != reverse('index'):
            return None

            start = time.time()
            response = func(request)
            costed = time.time() - start
            print('{:.2f}'.format(costed))
            return response

    """
    - process_template_response : 执行上面的方法,并且在django帮我们执行view方法之后,拿到最终的response,
            如果是使用了模板的response 是指通过 return render(request, 'index.html', context={})的
            方式返回response,就会来到这个方法中.在这里我们可以对response做一下操作,比如:
            content-Type 设置,或者其他HEADER的修改或增加
    """
    def process_template_response(self, request, response):
        return response
    
    """
    process_response : 当所有的流程都处理完毕,就来到这个方法.
            这个方法逻辑是和process_template_response完全一样的.
            只是 process_template_response是针对带有带有模板的response的处理.
    """
    def process_response(self, request, response):
        return response

    """
    - process_exception : 只有在发生异常时，才会进入到这个方法.
    """
    def process_exception(self, request, exceptipn):
        pass
