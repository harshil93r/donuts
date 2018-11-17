from django.http.response import (
    HttpResponse,
    JsonResponse,
    StreamingHttpResponse,
    HttpResponseNotAllowed
)


class Response(Exception):

    def __init__(self, response, code=200):
        pass

    @property
    def response(self):
        return self._response


class ReponseGrasper:

    def __init__(self, get_response):
        self.get_response = get_response

        # # overriding Django's inbuilt error handling
        # setattr(settings, 'DEBUG_PROPAGATE_EXCEPTIONS', True)

    def __call__(self, request):
        '''Handler method for middleware

        Args:
            request: Django's request object.

        Returns:
            Response passed by next middleware or view.

        '''

        try:
            response = self.get_response(request)

            if isinstance(response, HttpResponseNotAllowed):
                return response

            if isinstance(response, (HttpResponse, StreamingHttpResponse)):
                return response
            else:
                return JsonResponse(response)

        except HttpError as e:
            return e.response
