import json

from django.utils.deprecation import MiddlewareMixin


class CustomResponseMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        content_type = response.get("Content-Type")
        if not content_type or response.get("Content-Type") != "application/json":
            return response

        if response.status_code != 204:
            new_content = {
                "meta": {"code": response.status_code, "message": "ok"},
                "data": json.loads(response.content),
            }
            response.content = json.dumps(new_content)

        return response
