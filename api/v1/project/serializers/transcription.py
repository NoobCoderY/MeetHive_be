from rest_framework import serializers
from api.v1.project.models import Transcription
from .project import ProjectListItemSerializer, ProjectCreatorSerializer


class TranscriptionSerializer(serializers.ModelSerializer):
    project = ProjectListItemSerializer()
    created_by = ProjectCreatorSerializer()
    updated_by = ProjectCreatorSerializer()
    summary = serializers.SerializerMethodField()

    class Meta:
        model = Transcription
        fields = [
            'id', 'title', 'description', 'audio', 'text', 'project',
            'created_by', 'updated_by', 'created_at', 'updated_at', 'summary','status','audio_url'
        ]
        read_only_fields = fields

    def get_summary(self, obj):
        summary = obj.summary_set.first()
        return summary.id if summary else None


class TranscriptionListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcription
        fields = ['id', 'title']
        read_only_fields = fields
