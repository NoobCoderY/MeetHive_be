from rest_framework import serializers
from api.v1.project.models import Summary
from .project import ProjectListItemSerializer, ProjectCreatorSerializer
from .transcription import TranscriptionListItemSerializer


class SummarySerializer(serializers.ModelSerializer):
    transcription = TranscriptionListItemSerializer()
    project = ProjectListItemSerializer()
    created_by = ProjectCreatorSerializer()
    updated_by = ProjectCreatorSerializer()

    class Meta:
        model = Summary
        fields = [
            'id', 'title', 'summary', 'is_editable', 'transcription', 'project', 'status',
            'created_by', 'updated_by', 'created_at', 'updated_at'
        ]
        read_only_fields = fields


class SummaryListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = ['id', 'title']
        read_only_fields = fields
