from api.core.models import BaseModelManager
from api.v1.company.constants import CompanyRoleChoices, CompanyPermissionsEnum
from django.db import transaction


class CompanyRoleManager(BaseModelManager):
    def get_by_name(self, name, create=False):
        """
        Returns the role object having name provided.

        Attributes:
            - name (str) : role name to filter
            - create (bool) : Flag whether to create role if not exist
        """
        role = self.filter(name=name).first()

        if role is None and create and name in CompanyRoleChoices.names:
            role = self.create_role(
                name, CompanyPermissionsEnum.get_permissions(name))

        return role

    def create_role(self, name, permissions):
        """
        Creates a new CompanyRole object and returns it.

        Attributes:
            - name : (str) - Role name
            - permissions : (List[str]) - List of all the permissions included for the role
        """
        with transaction.atomic():
            role = self.create(
                name=name, permissions=permissions
            )

            return role
