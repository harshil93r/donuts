import json


class JsonMagic:

    def __init__(self, get_response):
        self.get_response = get_response

        # # overriding Django's inbuilt error handling
        # setattr(settings, 'DEBUG_PROPAGATE_EXCEPTIONS', True)

    def __call__(self, request):
        print(request.META.get('HTTP_AUTHORIZATION'))
        if request.body:
            s = request._body.decode('utf-8')
            request._json_body = json.loads(s)
            print(request._json_body)
        return self.get_response(request)
