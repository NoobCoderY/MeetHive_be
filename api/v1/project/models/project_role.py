import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from api.v1.project.constants import ProjectRoleChoices
from .managers import ProjectRoleManager
from api.core.models import BaseModel


class ProjectRole(BaseModel):
    """
    Represents the role data model in the project

    Attributes:
        - id (uuid): A unique field to identify the project role.
        - name (str): Name of the role
        - permissions (json): List of all possible permissions for the role
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    name = models.CharField(
        max_length=255, null=False, blank=False,
        choices=ProjectRoleChoices.choices
    )
    permissions = models.JSONField(default=list)

    objects = ProjectRoleManager()

    class Meta:
        app_label = "project"
        verbose_name = _("Project Role")
        verbose_name_plural = _("Project Roles")
        db_table = "project_roles"
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return f"{self.name}"
