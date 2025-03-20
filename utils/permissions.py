from api.v1.company.models import CompanyRole
from api.v1.company.constants import CompanyPermissionsEnum

from api.v1.project.models import ProjectRole
from api.v1.project.constants import ProjectPermissionsEnum


def add_all_company_permissions_to_db():
    """
    Utility function to save all the company level permissions to DB
    """
    admin_role = CompanyRole.objects.filter(name="COMPANY_ADMIN").first()
    manager_role = CompanyRole.objects.filter(name="MANAGER").first()
    member_role = CompanyRole.objects.filter(name="MEMBER").first()
    if admin_role:
        admin_role.permissions = CompanyPermissionsEnum.get_admin_permissions()
        admin_role.save()
    if manager_role:
        manager_role.permissions = CompanyPermissionsEnum.get_manager_permissions()
        manager_role.save()
    if member_role:
        member_role.permissions = CompanyPermissionsEnum.get_member_permissions()
        member_role.save()


def add_all_project_permissions_to_db():
    """
    Utility function to save all the project level permissions to DB
    """
    admin_role = ProjectRole.objects.filter(name="ADMIN").first()
    editor_role = CompanyRole.objects.filter(name="EDITOR").first()
    viewer_role = CompanyRole.objects.filter(name="VIEWER").first()
    if admin_role:
        admin_role.permissions = ProjectPermissionsEnum.get_admin_permissions()
        admin_role.save()
    if editor_role:
        editor_role.permissions = ProjectPermissionsEnum.get_editor_permissions()
        editor_role.save()
    if viewer_role:
        viewer_role.permissions = ProjectPermissionsEnum.get_viewer_permissions()
        viewer_role.save()
