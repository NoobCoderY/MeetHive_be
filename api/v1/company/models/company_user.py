from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from utils import generate_token
from .company import Company
from api.v1.user.models import User
from api.core.models import BaseModel
from .managers import CompanyUserManager
from .company_role import CompanyRole


class CompanyUser(BaseModel):
    """
    An association Entity that connects user and company tables

    Attributes:
        - id (uuid): A unique field to identify the CompanyUser.
        - user (ForeignKey): A User foreign key representing the user in company.
        - company (ForeignKey): A Company foreign key representing the company.
        - token (str): A random unique string generated for identification and verification.
        - role (CompanyRole): Represents the role of the user in the company.
        - is_active (bool): Represent if the user is currently active in the company.
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    token = models.CharField(
        max_length=255, default=generate_token, unique=True)
    role = models.ForeignKey(
        CompanyRole, on_delete=models.DO_NOTHING, null=False,
        help_text=_("Role of the user in company")
    )
    is_active = models.BooleanField(
        default=False, help_text=_("Is the user active in the company?"))

    objects = CompanyUserManager()

    class Meta:
        app_label = "company"
        verbose_name = "Company User"
        verbose_name_plural = "Company Users"
        db_table = "company_users"
        indexes = [
            models.Index(fields=['user', 'company']),
            models.Index(fields=['role', 'token'])
        ]

    def __str__(self):
        return f"{self.user.get_name()} in {self.company.name}"
