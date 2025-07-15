# middleware.py
import sys
from django.urls import resolve
from django.urls.exceptions import Resolver404


class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"Request path: {request.path}", file=sys.stderr, flush=True)
        print(f"Request method: {request.method}", file=sys.stderr, flush=True)
        print(f"Content-Type: {request.content_type}", file=sys.stderr, flush=True)

        # Test URL resolution
        try:
            resolved = resolve(request.path)
            print(
                f"URL resolved to: {resolved.func} in {resolved.app_name}",
                file=sys.stderr,
                flush=True,
            )
            print(f"View name: {resolved.view_name}", file=sys.stderr, flush=True)
        except Resolver404:
            print("URL NOT FOUND - Resolver404 error", file=sys.stderr, flush=True)

        response = self.get_response(request)
        print(f"Response status: {response.status_code}", file=sys.stderr, flush=True)
        return response
