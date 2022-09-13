from .models import Count


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        c = Count.objects.all().first()
        c.counter = c.counter+1
        c.save()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
