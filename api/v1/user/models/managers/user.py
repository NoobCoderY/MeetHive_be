from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **kwargs):
        if not email:
            raise ValueError(_("Email is required"))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **kwargs):
        user = self.create_user(username, email, password, **kwargs)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        return user

    def get_by_natural_key(self, username: str):
        return self.get(username=username)

    def get_by_id(self, id: str):
        """
        Retrieves the user by it's ID

        Attributes:
        - id : (str | int)
            - The primary key of the record
        """
        try:
            return self.get(pk=id)
        except self.model.DoesNotExist:
            return None
