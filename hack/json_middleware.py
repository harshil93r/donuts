import json


class JsonMagic:

    def __init__(self, get_response):
        self.get_response = get_response

        # # overriding Django's inbuilt error handling
        # setattr(settings, 'DEBUG_PROPAGATE_EXCEPTIONS', True)

    def __call__(self, request):
        if request.body:
            request._json_body = json.loads(request.body)

        return self.get_response(request)
