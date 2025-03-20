from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from api.v1.company.constants import StatusChoices
from .managers import CompanyManager
from api.core.models import BaseModel
from api.v1.user.models import User

# Create your models here.


class Company(BaseModel):
    """
    Represents the company data model.

    Attributes:
        - id (uuid): A unique field to identify the company
        - name (str): Name of the company
        - description (str): Information about the company
        - website (url): Company website
        - status (ACTIVE|INACTIVE): Current status of the company
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    name = models.CharField(max_length=255, null=False,
                            blank=False, verbose_name=_("Company Name"))
    description = models.TextField(verbose_name=_("Company Description"))
    website = models.URLField(
        max_length=255, verbose_name=_("Company Website"))
    status = models.CharField(
        max_length=15, choices=StatusChoices.choices, default=StatusChoices.INACTIVE)

    users = models.ManyToManyField(User, through='CompanyUser')

    objects = CompanyManager()

    class Meta:
        app_label = "company"
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        db_table = "companies"

    def __str__(self):
        return f"{self.name}"
