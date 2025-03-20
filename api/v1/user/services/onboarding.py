from django.db import transaction
from django.utils.translation import gettext_lazy as _

from api.v1.user.models import User, UserOnboarding
from api.v1.user.serializers import UserOnboardingSerializer
from justagile_be.exceptions import BusinessException


class OnboardingService:

    @staticmethod
    def get_user_onboarding(user_id: str):
        """
        Service function to get User onboarding information

        Attributes:
        - user_id : (str)
            - ID of the User to retrieve onboarding info
        """
       
        onboarding = UserOnboarding.objects.get_by_user(user_id)
        if onboarding:
            return UserOnboardingSerializer(onboarding).data

        return None

    @staticmethod
    def save_onboarding(request, user: str):
        """
        Service function to save use onboarding information

        Attributes:
        - request : (JSON)
            - User onboaridng request information
        """
        with transaction.atomic():
            user = User.objects.get_by_id(user)
            if user is None:
                raise BusinessException(
                    "USER_NOT_EXIST", _("User does not exist"))

            onboarding, created = UserOnboarding.objects.update_or_create(
                user=user, defaults={**request}
            )

            return UserOnboardingSerializer(onboarding).data
