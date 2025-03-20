from rest_framework import serializers
from api.v1.company.models import CompanyMonthlyUsage
from .company import CompanyListItemSerializer


class CompanyMonthlyUsageSerializer(serializers.ModelSerializer):
    company = CompanyListItemSerializer()

    class Meta:
        model = CompanyMonthlyUsage
        fields = [
            'company', 'month', 'year', 'transcription_duration', 'summaries_count'
        ]
