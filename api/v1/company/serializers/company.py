from rest_framework import serializers
from api.v1.company.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'description', 'website', 'status',
            'created_at', 'updated_at'
        ]


class CompanyListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']
