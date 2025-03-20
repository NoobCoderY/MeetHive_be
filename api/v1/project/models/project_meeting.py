import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from api.core.models import BaseModel
from .project_user import ProjectUser
from .managers import ProjectMeetingManager


class ProjectMeeting(BaseModel):
    """
    A Meeting data model which contains all the meeting informations such as transcriptions, summary, etc.,

    Attributes:
        - id (uuid): A unique field to identify the meeting of a project.
        - title (str): Name of the meeting.
        - project (Project): A foreign key representing the project.
        - created_by (ProjectUser): A foreign key representing the creator of the meeting.
        - updated_by (ProjectUser): A foreign key representing the person who recently updated the meeting.
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    title = models.CharField(max_length=255, null=False, blank=True)
    project = models.ForeignKey(
        'Project', on_delete=models.CASCADE, null=False, related_name="meeting_project"
    )

    created_by = models.ForeignKey(
        ProjectUser, on_delete=models.SET_NULL, related_name="project_meeting_created_by",
        null=True
    )
    updated_by = models.ForeignKey(
        ProjectUser, on_delete=models.SET_NULL, related_name="project_meeting_updated_by",
        null=True
    )

    objects = ProjectMeetingManager()

    class Meta:
        app_label = "project"
        verbose_name = _("Project Meeting")
        verbose_name_plural = _("Project Meetings")
        db_table = "project_meetings"
        indexes = [
            models.Index(fields=['project'])
        ]

    def __str__(self):
        return f"{self.title}"
