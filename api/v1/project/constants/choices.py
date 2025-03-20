from django.db import models
from django.utils.translation import gettext_lazy as _


class ProjectRoleChoices(models.TextChoices):
    ADMIN = 'ADMIN', _("Admin")
    EDITOR = 'EDITOR', _("Editor")
    VIEWER = 'VIEWER', _("Viewer")
