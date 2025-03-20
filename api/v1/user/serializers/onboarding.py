from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from api.v1.user.models import UserOnboarding
from justagile_be.exceptions import BusinessException


class UserOnboardingSerializer(serializers.ModelSerializer):
    """
    Handler serialization of User model
    """
    class Meta:
        model = UserOnboarding
        fields = ['id', 'user', 'profession', 'interests']
        read_only_fields = fields


class SaveOnboardingRequestSerializer(serializers.Serializer):
    """
    Serializer for save user onboarding request

    Attributes:
    - profession : (str)
        - Answer to: "What interests you the most?"
    - interests : (List[str])
        - Answer to: "What interests you the most?"
    """

    profession = serializers.CharField(
        required=True, error_messages={'required': _("Missing anwer to: `What interests you the most?`")}
    )
    interests = serializers.ListField(child=serializers.CharField())
