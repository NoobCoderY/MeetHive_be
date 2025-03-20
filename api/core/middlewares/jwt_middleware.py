import jwt
from api.v1.user.models import User
from justagile_be.exceptions import BusinessException
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class JWTMiddleware:
    """
    Middleware for JWT Authorization
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if not request.COOKIES.get('csrftoken'):
                print("CSRF: ", request.META.get('HTTP_X_CSRFTOKEN'))
                request.COOKIES['csrftoken'] = request.META.get(
                    'HTTP_X_CSRFTOKEN'
                )
            auth_header = request.headers.get('Authorization')
            if auth_header:
                auth_token = auth_header[7:]
                payload = jwt.decode(
                    auth_token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
                jwt_data = payload['data']
                user = User.objects.get(id=jwt_data['user'])
                request.user = user
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist, IndexError):
            pass

        response = self.get_response(request)
        return response
