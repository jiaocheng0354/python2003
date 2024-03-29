import logging

from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status

logger = logging.getLogger("django")


def exception_handler(exc, context):
    error = "%s %s %s" % (context['view'], context['request'].method, exc)

    response = drf_exception_handler(exc, context)

    if response is None:
        logger.error(error)
        return Response(
            {"error_msg": "开会小差"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=None)

    return response