from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission
from justagile_be.exceptions import BusinessException, UnauthorizedException
from api.v1.company.models import Company, CompanyUser
from api.v1.project.models import Project, ProjectUser


def has_project_permission(permissions=[]):
    """
    decorator to manage project level permissions

    **Note:** 
        Whenever using has_project_permission decorator, \
        It is mandatory to use has_company_permission decorator before that.
        Otherwise, the API will give error saying, `Request has no attribute company`.
    """
    def decorator(func):
        def wrapper(view, request, *args, **kwargs):
            if not request.user:
                raise UnauthorizedException()

            company_id = request.headers.get('X-Tenant-ID')
            if not company_id:
                raise BusinessException(
                    'TENANT_ID_NEEDED', _('Company ID is missing')
                )

            company = request.company
            if not company:
                if not company_id:
                    raise BusinessException(
                        'COMPANY_NOT_EXIST', _('Company does not exist')
                    )

                company = Company.objects.get_by_id(company_id)
                request.company = company

            company_user = request.company_user
            if not company_user:
                company_user = CompanyUser.objects.get_company_user(
                    company, request.user
                )
                request.company_user = company_user

            project_id = request.headers.get('X-Project-ID')
            project = Project.objects.get_by_id(project_id)

            if not project:
                raise BusinessException(
                    'UNAUTHORIZED', _('Project does not exist')
                )

            project_user = ProjectUser.objects.get_project_user(
                project, request.company_user)
            if not project_user:
                raise BusinessException(
                    'UNAUTHORIZED', _('User is not part of the project')
                )

            request.project = project
            request.project_user = project_user

            access_allowed = list(
                filter(lambda x: x not in project_user.role.permissions, permissions)
            )

            if len(access_allowed):
                raise BusinessException(
                    "UNAUTHORIZED",
                    _('You do not have permission in the project to access the API')
                )

            return func(view, request, *args, **kwargs)
        return wrapper
    return decorator
