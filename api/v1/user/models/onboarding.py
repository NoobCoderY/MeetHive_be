from api.core.models import BaseModel
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from . import User
from .managers import UserOnboardingManager


class UserOnboarding(BaseModel):
    """
    Represents the user onboarding information

    Attributes:
        - id (uuid): A unique field to identify the onboarding information
        - profession (str): Answer to - What describes you the best?
        - interest (JSON): Answer to - What interests you the most?
        - user (User::1-1): Represents the user who did the onboarding
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    profession = models.CharField(
        verbose_name=_("What describes you the best?"), max_length=255, null=True, blank=True
    )
    interests = models.JSONField(
        default=list, verbose_name=_("What interests you the most?")
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)

    objects = UserOnboardingManager()

    class Meta:
        app_label = "user"
        verbose_name = "User Onboarding"
        verbose_name_plural = "User Onboardings"
        db_table = "user_onboarding"
        indexes = [
            models.Index(fields=['user'])
        ]

    def __str__(self):
        return f"{self.user.get_name()}"
