import os
import uuid
from django.db import models
from api.core.models import BaseModel
from .project_user import ProjectUser
from .managers import TranscriptionManager
from django.utils.translation import gettext_lazy as _


def get_transcription_upload_to(instance, filename: str):
    """
    Returns the S3 file upload location for transcription audio file

    Attributes:
        - instance (Transcription) : Transcription data model
        - filename (str) : Name of the file uploaded

    Returns: Path of the transcription audio in S3
    """
    return os.path.join(f"{instance.created_by.user.company.id}", f"{instance.project.id}", f"transcriptions", f"{instance.id}-{filename}")


class Transcription(BaseModel):
    """
    Represents the Transcription data model

    Attributes:
        - id (uuid): A unique field to identify the transcription
        - title (str): Name of the transcription
        - description (str): Transcription description
        - audio (URL): URL to access transcription audio
        - text (dict): transcription data JSON
        - audio_url (URL): URL to access transcription audio file directly.
        - status (str): Current status of the transcription (pending, completed,failed).
        - created_by (ProjectUser): A foreign key representing the creator of the transcription.
        - updated_by (ProjectUser): A foreign key representing the person who recently updated the transcription.
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    title = models.CharField(max_length=255, null=False, blank=True)
    description = models.TextField(null=True, blank=True)
    # TODO: Keeping this field nullable.  Need to check if we can handle this via AWS Transcribe
    audio = models.FileField(
        max_length=500, upload_to=get_transcription_upload_to, null=True
    )
    text = models.JSONField(default=dict, null=True)
    audio_url = models.URLField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('failed', 'Failed')
        ],
        null=True,
        blank=True
    )
    project = models.ForeignKey(
        'Project', on_delete=models.CASCADE, related_name="transcription_project"
    )
    

    created_by = models.ForeignKey(
        ProjectUser, on_delete=models.SET_NULL, related_name="project_transcription_created_by",
        null=True
    )
    updated_by = models.ForeignKey(
        ProjectUser, on_delete=models.SET_NULL, related_name="project_transcription_updated_by",
        null=True
    )

    objects = TranscriptionManager()

    class Meta:
        app_label = "project"
        verbose_name = _("Transcription")
        verbose_name_plural = _("Transcriptions")
        db_table = "transcriptions"
        indexes = [
            models.Index(fields=['created_by']),
            models.Index(fields=['project'])
        ]

    def __str__(self):
        return f"{self.title}"
