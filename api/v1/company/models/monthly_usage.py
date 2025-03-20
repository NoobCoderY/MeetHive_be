from django.db import models
from api.core.models import BaseModel
from .managers import CompanyMonthlyUsageManager
from django.utils.translation import gettext_lazy as _
from .company import Company


class CompanyMonthlyUsage(BaseModel):
    """
    Represents the Monthly usage information of company

    Attributes:
        - month (int): Month number of usage
        - year (int): Year of usave
        - transcription_minutes (float): Number of minutes transcripted in the month
        - summaries_count (int): Number of summaries created in the month
    """

    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=False)
    month = models.IntegerField(null=False, blank=False)
    year = models.IntegerField(null=False, blank=False)

    transcription_duration = models.FloatField(
        default=0,
        help_text=_('Number of Seconds transcripted in the month')
    )
    summaries_count = models.IntegerField(
        default=0,
        help_text=_('Number of summaries created in the month')
    )

    objects = CompanyMonthlyUsageManager()

    class Meta:
        app_label = "company"
        verbose_name = _('Company monthly usage')
        verbose_name_plural = _('Company monthly usages')
        db_table = "company_monthly_usage"
        indexes = [
            models.Index(fields=['month', 'year']),
            models.Index(fields=['company'])
        ]

    def __str__(self):
        return f"{self.month} - {self.year}"
