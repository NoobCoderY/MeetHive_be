from api.core.models import BaseModelManager
from datetime import datetime
from django.db import transaction
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from justagile_be.exceptions import BusinessException


class CompanyMonthlyUsageManager(BaseModelManager):
    def get_current_month_usage(self, company, create=False):
        """
        Get the Usage for current month and year.

        Attributes:
                - company (Company) : Company to get the usage
                - create (bool) : Flag whether to create usage if not exist
        """
        month = datetime.now().month
        year = datetime.now().year

        current_month_usage = self.filter(
            month=month, year=year, company=company
        ).first()
        if not current_month_usage and create:
            with transaction.atomic():
                return self.create(
                    month=month, year=year, company=company
                )

        return current_month_usage
    
    def add_transcription_duration(self, company, duration):
        """
        Add transcription duration to company's current monthly usage

        Attributes:
            - company (Company) : Company to add the usage to
            - duration (float) : Duration of the transcription usage
        """

        with transaction.atomic():
            current_month_usage = self.get_current_month_usage(
                company, create=True
            )

            total_duration = current_month_usage.transcription_duration + duration
            if total_duration > settings.TRANSCRIPTION_MONTHLY_LIMIT:
                raise BusinessException(
                    "TRANSCRIPTION_LIMIT_EXCEEDED",
                    _("Transcription cannot be added as the limit has been reached for this month.")
                )
            current_month_usage.transcription_duration += duration
            current_month_usage.save()

            return current_month_usage
        
    def add_summary_count(self, company):
        """
        Add summary count to company's current monthly usage

        Attributes:
            - company (Company) : Company to add the usage to
        """

        with transaction.atomic():
            current_month_usage = self.get_current_month_usage(
                company, create=True
            )

            total_count = current_month_usage.summaries_count + 1
            if total_count > settings.SUMMARY_MONTHLY_LIMIT:
                raise BusinessException(
                    "SUMMARY_LIMIT_EXCEEDED",
                    _("Summary cannot be generated as the limit has been reached for this month")
                )
            current_month_usage.summaries_count += 1
            current_month_usage.save()

            return current_month_usage
