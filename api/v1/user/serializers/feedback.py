from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from api.v1.user.models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    """
    Handler serialization of User Feedback model
    """
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'reaction', 'feedback']
        read_only_fields = fields


class SaveFeedbackRequestSerializer(serializers.Serializer):
    """
    Serializer for save feedback request

    Attributes:
    - reaction : (bool)
        - Represents whether the user has liked/disliked the product
    - feedback : (str)
        - Represents the user feedback text
    """

    reaction = serializers.BooleanField()
    feedback = serializers.CharField(
        required=True, error_messages={
            'required': _('Feedback is required')
        }
    )


class SupportEmailRequestSerializer(serializers.Serializer):
    """
    Serializer for send a support email

    Attributes:
    - subject : (str)
        - Subject of the email
    - body : (str)
        - body of the email
    """

    subject = serializers.CharField(
        required=True, error_messages={
            'required': _('Subject is required')
        }
    )
    body = serializers.CharField(
        required=True, error_messages={
            'required': _('Body is required')
        }
    )
