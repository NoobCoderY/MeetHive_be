import uuid
from django.db import models
from api.core.models import BaseModel
from .managers import SummaryManager
from .project_user import ProjectUser
from django.utils.translation import gettext_lazy as _


class Summary(BaseModel):
    """
    Represents the Summary data model

    Attributes:
        - id (uuid): A unique field to identify the summary.
        - title (str): Title of the summary
        - summary (str): Summary of the transcription
        - is_editable (bool) : A Boolean field representing whether the summary can be editable or non-editable
        - transcription (Transcription) : A Foreign key representing the transcription the summary belongs to
        - status (str): Status of the summary, can be either 'pending' or 'completed'
        - created_by (ProjectUser): A foreign key representing the creator of the summary.
        - updated_by (ProjectUser): A foreign key representing the person who recently updated the summary.
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    title = models.CharField(max_length=255, null=False, blank=True)
    summary = models.TextField(null=True, blank=True)
    is_editable = models.BooleanField(default=True)
    transcription = models.ForeignKey(
        'Transcription', on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        'Project', on_delete=models.CASCADE, related_name="summary_project"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('failed', 'Failed')
        ],
        default='pending'
    )

    created_by = models.ForeignKey(
        ProjectUser, on_delete=models.SET_NULL, related_name="project_summary_created_by",
        null=True
    )
    updated_by = models.ForeignKey(
        ProjectUser, on_delete=models.SET_NULL, related_name="project_summary_updated_by",
        null=True
    )

    objects = SummaryManager()

    class Meta:
        app_label = "project"
        verbose_name = _("Project Summary")
        verbose_name_plural = _("Project Summaries")
        db_table = "project_summaries"
        indexes = [
            models.Index(fields=['transcription']),
            models.Index(fields=['created_by']),
            models.Index(fields=['project'])
        ]

    def __str__(self):
        return f"{self.title}"
