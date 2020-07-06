from rest_framework.response import Response
from rest_framework.views import exception_handler as as_exception_handler


def exception_handler(exc, context):
    result = as_exception_handler(exc, context)
    if result is None:
        return Response({
            "essor_msg": "开小差了"
        }, status=500, exception=None)
    return result
