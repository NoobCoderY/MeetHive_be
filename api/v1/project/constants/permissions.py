from enum import Enum
from django.utils.translation import gettext_lazy as _
from .choices import ProjectRoleChoices


class ProjectPermissionsEnum(Enum):
    """
    Enum for project level permissions
    """
    INVITE_USERS = _("Can invite users to the project")
    VIEW_PROJECT = _('Can view the project')
    UPDATE_PROJECT = _('Can update the project')
    VIEW_TRANSCRIPTION = _('Can view transcriptions')
    CREATE_TRANSCRIPTION = _('Can create transcription')
    UPDATE_TRANSCRIPTION = _('Can update transcription')
    DELETE_TRANSCRIPTION = _('Can delete transcription')
    VIEW_SUMMARY = _('Can view summaries')
    CREATE_SUMMARY = _('Can create summaries')
    UPDATE_SUMMARY = _('Can update summaries')
    DELETE_SUMMARY = _('Can delete summaries')

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
    def get_editor_permissions(cls):
        """
        Returns list of all editor permissions
        """
        return [
            ProjectPermissionsEnum.VIEW_PROJECT.name, ProjectPermissionsEnum.UPDATE_PROJECT.name
        ]

    @classmethod
    def get_viewer_permissions(cls):
        """
        Returns list of all viewer permissions
        """
        return [
            ProjectPermissionsEnum.VIEW_PROJECT.name
        ]

    @staticmethod
    def get_permissions(role: str):
        """
        Returns a list of all permissions for a role

        Attributes:
            - role (str) : Role to get permissions 
        """
        if role == ProjectRoleChoices.ADMIN:
            return ProjectPermissionsEnum.get_admin_permissions()
        elif role == ProjectRoleChoices.EDITOR:
            return ProjectPermissionsEnum.get_editor_permissions()
        elif role == ProjectRoleChoices.VIEWER:
            return ProjectPermissionsEnum.get_viewer_permissions()

        return []
