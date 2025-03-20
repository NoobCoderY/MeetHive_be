import uuid
from django.db import models
from django.apps import apps
from api.core.models import BaseModel
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


# Create your models here.

def profile_picture_directory_path(instance, filename):
    return f'profile_pictures/user_{instance.id}/{filename}'


class User(AbstractUser, BaseModel):
    """
    Represents the user data model

    Attributes:
        - id (uuid): A unique field to identify the user
        - username (datetime): A unique username representing the user
        - first_name (str): First name of the user
        - last_name (str): Last name of the user
        - email (str): Unique email of the user
        - is_active (boolean): Represents if a user is active or not
        - is_admin (boolean): Represents if a user is admin or not
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    first_name = models.CharField(max_length=127, null=False)
    last_name = models.CharField(max_length=127, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    profile_picture=models.FileField(upload_to=profile_picture_directory_path, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name','email']

    objects = UserManager()

    class Meta:
        app_label = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "users"
        # Added an index for email to improve the query performance
        indexes = [
            models.Index(fields=['email'])
        ]

    def get_name(self):
        """
        Returns full name of the user object by concatenating first name and last name
        """
        return f"{self.first_name} {self.last_name or ''}"

    def __str__(self):
        return self.get_name()
