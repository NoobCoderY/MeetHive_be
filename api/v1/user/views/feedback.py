from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from utils import get_response
from api.v1.user.models import Feedback
from api.v1.user.services import FeedbackService
from api.v1.user.serializers import FeedbackSerializer, SaveFeedbackRequestSerializer, SupportEmailRequestSerializer
from api.core.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from justagile_be.exceptions import BusinessException
from api.core.services import EmailService
from django.conf import settings

#Crete instance of EmailService
EmailService=EmailService()


class FeedbackView(APIView):
    """
    API View to handle User feedbacks
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['user'],
        operation_summary=_("API to create new feedback"),
        operation_id=_("Create Feedback"),
        request_body=SaveFeedbackRequestSerializer,
        responses={
            200: "Feedback saved successfully",
            400: 'Failed to save Feedback'
        }
    )
    def post(self, request):
        """
        `POST` API to save user's feedback

        ---
        URL:
            <BASE_URL>/api/v1/user/feedback/
        ---
        Request:
            - SaveFeedbackRequestSerializer
        ---
        Response:
            FeedbackSerializer
        ---
        """
        serializer = SaveFeedbackRequestSerializer(data=request.data)

        if not serializer.is_valid():
            raise BusinessException(
                "SAVE_FEEDBACK_FAILED", _("The request is not valid")
            )

        data = serializer.validated_data
        res = FeedbackService.save_feedback(data, request.user)

        return get_response(201, res)


class SupportView(APIView):
    """
    API View to handle User support
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['user'],
        operation_summary=_("API to send support email"),
        operation_id=_("Send support mail"),
        request_body=SupportEmailRequestSerializer,
        responses={
            200: "Support mail sent successfully",
            400: 'Failed to send support mail'
        }
    )
    def post(self, request):
        """
        `POST` API to send support email

        ---
        URL:
            <BASE_URL>/api/v1/user/support/
        ---
        Request:
            - SupportEmailRequestSerializer
        ---
        Response:
            - boolean
        ---
        """
        serializer = SupportEmailRequestSerializer(data=request.data)
        user = request.user

        if not serializer.is_valid():
            raise BusinessException(
                "SUPPORT_MAIL_FAILED", _("The request is not valid")
            )

        data = serializer.validated_data

        EmailService.send_mail(
            "emails/account/support_mail.html",
            data.get('subject'),
            user.email, context=data,
            reply_to=[settings.EMAIL_HOST_USER]
        )

        return get_response(200, True)
