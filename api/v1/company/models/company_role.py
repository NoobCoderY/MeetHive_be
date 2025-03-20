from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from api.core.models import BaseModel
from api.v1.company.constants.choices import CompanyRoleChoices
from .managers import CompanyRoleManager


class CompanyRole(BaseModel):
    """
    Represents the role data model in a company.

    Attributes:
        - id (uuid): A unique field to identify the role
        - name (str): Name of the role
        - permissions (json): List of all possible permissions for the role
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    name = models.CharField(
        max_length=255, null=False,
        blank=False, choices=CompanyRoleChoices.choices
    )
    permissions = models.JSONField(default=list)

    objects = CompanyRoleManager()

    class Meta:
        app_label = "company"
        verbose_name = _("Company Role")
        verbose_name_plural = _("Company Roles")
        db_table = "company_roles"
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return f"{self.name}"
