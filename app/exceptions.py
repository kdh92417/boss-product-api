from rest_framework.views import exception_handler as drf_exception_handler


def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    custom_response_data = {
        "meta": {"code": exc.status_code, "message": response.data},
        "data": None,
    }

    response.data = custom_response_data
    return response
