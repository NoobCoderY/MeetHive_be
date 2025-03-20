from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission
from justagile_be.exceptions import BusinessException, UnauthorizedException
from api.v1.company.models import Company, CompanyUser


def has_company_permission(permissions=[]):
    """
    decorator to manage company level permissions
    """
    def decorator(func):
        def wrapper(view, request, *args, **kwargs):
            if not request.user:
                raise UnauthorizedException()

            company_id = request.headers.get('X-Tenant-ID')
            if not company_id:
                raise BusinessException(
                    'TENANT_ID_NEEDED', _('Company id is missing'))

            company = Company.objects.get_by_id(company_id)
            company_user = CompanyUser.objects.get_company_user(
                company, request.user
            )

            request.company = company
            request.company_user = company_user

            access_allowed = list(
                filter(lambda x: x not in company_user.role.permissions, permissions)
            )

            if len(access_allowed):
                raise BusinessException(
                    "UNAUTHORIZED",
                    _('You do not have permission to access the API')
                )

            return func(view, request, *args, **kwargs)
        return wrapper
    return decorator
