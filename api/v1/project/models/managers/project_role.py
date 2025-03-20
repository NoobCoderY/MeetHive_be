from api.core.models import BaseModelManager
from api.v1.project.constants import ProjectRoleChoices, ProjectPermissionsEnum
from django.db import transaction


class ProjectRoleManager(BaseModelManager):
    def get_by_name(self, name, create=False):
        """
            Returns the role object having name provided.

            Attributes:
                - name (str) : role name to filter
                - create (bool) : Flag whether to create role if not exist
            """
        role = self.filter(name=name).first()

        if role is None and create and name in ProjectRoleChoices.names:
            role = self.create_role(
                name, ProjectPermissionsEnum.get_permissions(name))

        return role

    def create_role(self, name, permissions):
        """
        Creates a new ProjectRole object and returns it.

        Attributes:
            - name : (str) - Role name
            - permissions : (List[str]) - List of all the permissions included for the role
        """
        with transaction.atomic():
            role = self.create(
                name=name, permissions=permissions
            )

            return role
