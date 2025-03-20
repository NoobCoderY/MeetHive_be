import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from api.core.models import BaseModel
from api.v1.company.models import CompanyUser
from .project_role import ProjectRole
from .managers import ProjectUserManager


class ProjectUser(BaseModel):
    """
    An association Entity that connects Project and CompanyUser tables

    Attributes:
        - id (uuid): A unique field to identity ProjectUser.
        - project (Project): A foreign key representing the project.
        - user (CompanyUser): A foreign key representing the user in project.
        - role (ProjectRole): A foreign key representing the role of the user in the project.
        - is_active (bool): Represents if the user is active in the project.
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    user = models.ForeignKey(CompanyUser, on_delete=models.CASCADE)
    role = models.ForeignKey(
        ProjectRole, on_delete=models.DO_NOTHING, null=False,
        help_text=_("Role of the user in project")
    )
    is_active = models.BooleanField(
        default=False, help_text=_("Is the user active in the project?"))

    objects = ProjectUserManager()

    class Meta:
        app_label = "project"
        verbose_name = _("Project User")
        verbose_name_plural = _("Project Users")
        db_table = "project_users"
        indexes = [
            models.Index(fields=['project', 'user']),
            models.Index(fields=['role'])
        ]

    def __str__(self):
        return f"Project: {self.project.name}, User: {self.user}"
