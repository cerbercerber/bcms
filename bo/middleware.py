from django.conf import settings
#from django.contrib import messages

class StackOverflowMiddleware :
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
    def process_exception(self, request, exception):
        if settings.DEBUG:
           # messagetab.append({ exception.__class__.__name__,exception.message});
           # print('<script>$("document").ready(function(e){$("#modalmessage")});</script>')
            print('Exception middleware')
            print (exception.__class__.__name__)
            print (exception.message)
        return None
