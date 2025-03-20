from api.core.models import BaseModel
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from . import User
from .managers import FeedbackManager


class Feedback(BaseModel):
    """
    Represents the feedback data model

    Attributes:
        - id (uuid): A unique field to identify the feedback
        - feedback (str): Feedback by the user
        - 
        - user (User::1-*): Represents the user who gave the feedback
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    feedback = models.TextField(null=True, blank=True)
    reaction = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    objects = FeedbackManager()

    class Meta:
        app_label = "user"
        verbose_name = "User Feedback"
        verbose_name_plural = "User Feedbacks"
        db_table = "user_feedbacks"
        indexes = [
            models.Index(fields=['user'])
        ]

    def __str__(self):
        return f"{self.user.get_name()}"
