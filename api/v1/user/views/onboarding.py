from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from utils import get_response
from api.v1.user.serializers import SaveOnboardingRequestSerializer
from django.utils.translation import gettext_lazy as _
from justagile_be.exceptions import BusinessException
from api.v1.user.services import OnboardingService
from drf_yasg import openapi
from api.core.permissions import IsAuthenticated
from api.core.swagger import TENANT_ID_HEADER


class UserOnboardingView(APIView):
    """
    API View to handle User onboarding.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['user'],
        operation_summary=_("API to get user onboarding information"),
        operation_id=_("Get Onboarding"),
        manual_parameters=[
            openapi.Parameter(
                name="user",
                required=True,
                type=openapi.TYPE_STRING,
                in_=openapi.IN_PATH,
                description="User ID",
            ),
        ],
        responses={
            200: 'Onboarding data retrieval successful',
            400: 'Onboarding data retrieval Failed'
        }
    )
    def get(self, request, user):
        """
        `GET` API to get user's onboarding information.

        ---
        URL:
            <BASE_URL>/api/v1/user/onboarding/<str:user>/
        ---
        Request:
            user: (str) - passed as part of the URL
        ---
        Response:
            UserOnboardingSerializer
        ---
        """
        onboarding = OnboardingService.get_user_onboarding(user)

        return get_response(200, onboarding)

    @swagger_auto_schema(
        tags=['user'],
        operation_summary=_("API to save user onboarding information"),
        operation_id=_("Save Onboarding"),
        request_body=SaveOnboardingRequestSerializer,
        manual_parameters=[
            openapi.Parameter(
                name="user",
                required=True,
                type=openapi.TYPE_STRING,
                in_=openapi.IN_PATH,
                description="User ID",
            ),
            TENANT_ID_HEADER
        ],
        responses={
            200: 'Onboarding data retrieval successful',
            400: 'Onboarding data retrieval Failed'
        }
    )
    def put(self, request, user):
        """
        `PUT` API to save/update user's onboarding information.

        ---
        URL:
            <BASE_URL>/api/v1/user/onboarding/<str:user>/
        ---
        Request:
            - user: (str) - passed as part of the URL
            - SaveOnboardingRequestSerializer
        ---
        Response:
            UserOnboardingSerializer
        ---
        """
        serializer = SaveOnboardingRequestSerializer(data=request.data)

        if not serializer.is_valid():
            raise BusinessException(
                "SAVE_ONBOARDING_FAILED", _("The request is not valid"))

        if f"{request.user.id}" != user:
            raise BusinessException(
                "UNAUTHORIZED",
                _("You are not allowed to save other user's onboarding information")
            )

        data = serializer.validated_data
        onboarding = OnboardingService.save_onboarding(data, user)

        return get_response(200, onboarding)
