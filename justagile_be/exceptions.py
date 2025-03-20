from django.utils.translation import gettext_lazy as _
from .error_codes import ErrorCodes
from utils import get_response


class BusinessException(Exception):
    """
    Business Exception handler
    """

    def __init__(self, code, error):
        super().__init__(code, error)


class UnauthorizedException(Exception):
    """
    Unauthorized Exception handler which will send 403 response
    """

    def __init__(self, code='UNAUTHORIZED', error=_('Token Expired')):
        super().__init__(code, error)


def global_exception_handler(exc, context):
    """
    Exception handler function that handles all exceptions before sending the response
    """
    if isinstance(exc, BusinessException):
        response = get_response(400, None, exc.args[0], exc.args[1])

    elif isinstance(exc, UnauthorizedException):
        response = get_response(403, None, exc.args[0], exc.args[1])

    else:
        response = get_response(500, None, 'Exception', f"{exc}")

    return response
