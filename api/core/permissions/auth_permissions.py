from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated as BaseIsAuthenticated
from justagile_be.exceptions import UnauthorizedException


class IsAuthenticated(BaseIsAuthenticated):
    """
    Permission class to check if user is authenticated
    """

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)

        if not is_authenticated:
            raise UnauthorizedException()

        if not request.user.is_active:
            raise UnauthorizedException(
                "UNAUTHORIZED", _('User is not active')
            )

        return True
