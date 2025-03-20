from api.core.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from api.v1.user.constants import AuditLogTaskChoices
from .managers import AuditLogManager


class AuditLog(BaseModel):
    """
    Represents the data model for audit logs

    Attributes:
    - created_by : (str)
        - User who triggered the log
    - company : (str)
        - Company where the log is triggered
    - project : (str)
        - Project where log is triggered
    - task : (str)
        - Task name where log is triggered
    - extra_fields : (dict)
        - Extra information that is useful for the logging
    """

    user = models.CharField(max_length=255, null=False)
    company = models.CharField(max_length=255, null=True, blank=True)
    project = models.CharField(max_length=255, null=True, blank=True)
    task = models.CharField(
        max_length=255, null=False,
        choices=AuditLogTaskChoices.choices
    )
    extra_fields = models.JSONField(default=dict)

    objects = AuditLogManager()

    class Meta:
        app_label = "user"
        verbose_name = _("Audit Log")
        verbose_name_plural = _("Audit Logs")
        db_table = "audit_logs"

    def __str__(self):
        return f"User: {self.user} did {self.task} in Company: {self.company} and in Project: {self.project} on {self.created_at}"
