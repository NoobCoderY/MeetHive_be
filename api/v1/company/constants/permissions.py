from enum import Enum
from django.utils.translation import gettext_lazy as _
from .choices import CompanyRoleChoices


class CompanyPermissionsEnum(Enum):
    """
    Enum for company level permissions
    """
    VIEW_COMPANY = _("Can view company details")
    UPDATE_COMPANY = _("Can update company details")
    UPDATE_COMPANY_LOGO = _("Can update company logo")
    CREATE_PROJECT = _("Can Create new project")
    VIEW_PROJECT = _("Can view projects")
    UPDATE_PROJECT = _("Can update project details")
    DELETE_PROJECT = _("Can delete project")

    @classmethod
    def get_all(cls):
        """
        Returns all the permissions
        """
        return [i.name for i in cls]

    @classmethod
    def get_all_info(cls):
        """
        Returns list of permissions and the descriptions
        """
        return [{"name": i.name, "description": i.value} for i in cls]

    @classmethod
    def get_admin_permissions(cls):
        """
        Returns list of all admin permissions
        """
        return cls.get_all()

    @classmethod
    def get_manager_permissions(cls):
        """
        Returns list of all manager permissions
        """
        return [cls.VIEW_COMPANY.name, cls.VIEW_PROJECT.name, cls.CREATE_PROJECT.name, cls.UPDATE_PROJECT.name, cls.DELETE_PROJECT.name]

    @classmethod
    def get_member_permissions(cls):
        """
        Returns list of all member permissions
        """
        return [cls.VIEW_COMPANY.name, cls.VIEW_PROJECT.name]

    @staticmethod
    def get_permissions(role: str):
        """
        Returns a list of all permissions for a role

        Attributes:
            - role (str) : Role to get permissions 
        """
        if role == CompanyRoleChoices.COMPANY_ADMIN:
            return CompanyPermissionsEnum.get_admin_permissions()
        elif role == CompanyRoleChoices.MANAGER:
            return CompanyPermissionsEnum.get_manager_permissions()
        elif role == CompanyRoleChoices.MEMBER:
            return CompanyPermissionsEnum.get_member_permissions()

        return []
