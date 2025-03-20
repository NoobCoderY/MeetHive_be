import uuid
from django.db import models
from api.core.models import BaseModel
from api.v1.company.constants import StatusChoices
from api.v1.company.models import Company, CompanyUser
from .managers import ProjectManager
from django.utils.translation import gettext_lazy as _
from .project_user import ProjectUser


class Project(BaseModel):
    """
    Represents the Project data model.

    Attributes:
        - id (uuid): A unique field to identify the project
        - name (str): Name of the project
        - description (str): Project description
        - status (ACTIVE|INACTIVE): Represents the status of the project
        - created_by (ForeignKey): A CompanyUser foreign key representing the creator of the project
        - updated_by (ForeignKey): A CompanyUser foreign key representing the user who updated the project last time
        - company (ForeignKey): A Company foreign key representing the company, the project is part of.
        - users (n:m): A Many-Many Relationship representing all the ProjectUser model indicating all the users who are part of the project
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    status = models.CharField(
        max_length=15, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    users = models.ManyToManyField(
        CompanyUser, through="ProjectUser", related_name="project_users")

    created_by = models.ForeignKey(
        CompanyUser, on_delete=models.SET_NULL, related_name="project_created_by",
        null=True
    )
    updated_by = models.ForeignKey(
        CompanyUser, on_delete=models.SET_NULL, related_name="project_updated_by",
        null=True
    )

    objects = ProjectManager()

    class Meta:
        app_label = "project"
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        db_table = "projects"
        indexes = [
            models.Index(fields=['company'])
        ]

    def __str__(self):
        return f"{self.id} - {self.name}"
