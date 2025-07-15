# middleware.py
import sys


class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"Request path: {request.path}", file=sys.stderr, flush=True)
        print(f"Request method: {request.method}", file=sys.stderr, flush=True)
        print(f"Content-Type: {request.content_type}", file=sys.stderr, flush=True)
        print(f"Request body: {request.body}", file=sys.stderr, flush=True)

        response = self.get_response(request)
        print(f"Response status: {response.status_code}", file=sys.stderr, flush=True)
        print(f"Response content: {response.content}", file=sys.stderr, flush=True)
        return response
