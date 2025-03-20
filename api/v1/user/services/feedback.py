from django.db import transaction
from django.utils.translation import gettext_lazy as _

from api.v1.user.models import Feedback
from api.v1.user.serializers import FeedbackSerializer
from justagile_be.exceptions import BusinessException


class FeedbackService:
    @staticmethod
    def save_feedback(request, user):
        """
        Service function to save feedback

        Attributes:
        - request : (JSON)
            - Feedback save request
        - user : (User)
            - User object
        """
        with transaction.atomic():
            if user is None:
                raise BusinessException(
                    "USER_NOT_EXIST", _("User does not exist"))

            feedback = Feedback.objects.create(
                feedback=request.get('feedback'),
                reaction=request.get('reaction'),
                user=user
            )

            res = FeedbackSerializer(feedback).data

            return res
