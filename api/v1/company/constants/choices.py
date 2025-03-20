from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusChoices(models.TextChoices):
    ACTIVE = 'ACTIVE', _("Active")
    INACTIVE = 'INACTIVE', _("Inactive")


class CompanyRoleChoices(models.TextChoices):
    COMPANY_ADMIN = 'COMPANY_ADMIN', _("Company Admin")
    MANAGER = 'MANAGER', _("Project Manager")
    MEMBER = 'MEMBER', _("Member")
