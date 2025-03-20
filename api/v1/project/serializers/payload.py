from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from api.v1.project.models import Project, Transcription


class CreateProjectSerializer(serializers.Serializer):
    """
    Serializer for Create Project API

    Attributes:
    - name : (str)
        - Name of the project
    - description : (str)
        - Project description
    """

    name = serializers.CharField(required=True, error_messages={
        'required': _('Project name is required')
    })
    description = serializers.CharField(
        required=False, allow_blank=True, default="")


class UpdateProjectSerializer(serializers.Serializer):
    """
    Serializer for Create Project API

    Attributes:
    - name : (str)
        - Name of the project
    - description : (str)
        - Project description
    """

    name = serializers.CharField(required=True, error_messages={
        'required': _('Project name is required')
    })
    description = serializers.CharField(
        required=False, allow_blank=True, default=""
    )


class CreateTranscriptionSerializer(serializers.Serializer):
    """
    Serializer to create new transcription

    Attributes:
    - title : (str)
        - Title of the transcription
    - audio : (File)
        - Audio file
    - text : (dict)
        - Transcription JSON data
    - duration : (int)
        - Duration of the audio/video
    """

    title = serializers.CharField(required=True, error_messages={
        'required': _('Transcription name is required')
    })
    description = serializers.CharField(
        required=False, allow_blank=True, default=""
    )
    audio = serializers.FileField(required=False, error_messages={
        'required': _('Audio file is required')
    })
    text = serializers.JSONField(required=True, error_messages={
        'required': _('Transcription text is required')
    })
    duration = serializers.IntegerField(required=True, error_messages={
        'required': _('Duration is required')
    })

    # TODO: Need to add validation for this serializer - VR-03SEP24


class UpdateTranscriptionSerializer(serializers.Serializer):

    title = serializers.CharField(required=True, error_messages={
        'required': _('Transcription name is required')
    })

    description = serializers.CharField(
        required=False, allow_blank=True, default=""
    )

    text = serializers.JSONField(required=True, error_messages={
        'required': _('Transcription text is required')
    })
        
    
class CreateSummarySerializer(serializers.Serializer):
    """
    Serializer to create new summary

    Attributes:
    - is_editable : (bool)
        - Whether the summary is editable or not
    - transcription : (uuid)
        - ForeignKey to the related transcription

    """

    is_editable = serializers.BooleanField(required=False, default=True)
    transcription = serializers.UUIDField(required=True, error_messages={
        'required': _('Transcription is required')
    })

class UpdateSummarySerializer(serializers.Serializer):
    """
    Serializer to update summary

    Attributes:
    -title : (string)
            -title of the summary
    -summary : (string)
            - edited summary content        
    - is_editable : (bool)
            - Whether the summary is editable or not

    """
    title=serializers.CharField(required=True)
    summary = serializers.CharField(required=True, allow_blank=True)
    is_editable = serializers.BooleanField(required=False, default=True)
  


class CreateUploadRecordingTranscriptionSerializer(serializers.Serializer):
    """
    Serializer to create a new transcription entry.

    Attributes:
    - title : (str)
        - Title of the transcription
    - description : (str)
        - Description of the transcription
    - file_url : (str)
        - URL to the audio or video file
    - duration : (int)
        - Duration of the audio/video
    """

    title = serializers.CharField(
        required=True,
        error_messages={'required': _('Transcription title is required')}
    )
    
    description = serializers.CharField(
        required=False, 
        allow_blank=True,
        default=""
    )

    audio_url = serializers.URLField(
        required=True,
        error_messages={'required': _('File URL is required')}
    )

    duration = serializers.IntegerField(
        required=True,
        error_messages={'required': _('Duration of the file is required')}
    )
