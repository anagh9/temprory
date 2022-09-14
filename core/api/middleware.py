from .models import Count


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        try:
            print(request)
            c = Count.objects.all().first()
            c.counter = c.counter+1
            c.save()

            response = self.get_response(request)

            return response

        except Exception as e:
            return e
