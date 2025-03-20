from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.utils.translation import gettext_lazy as _
from justagile_be.exceptions import BusinessException
from api.core.permissions import IsAuthenticated
from utils import get_response

from api.v1.company.models import Company, CompanyUser
from api.v1.company.serializers import CompanySerializer


class CompanyView(APIView):
    """
    API View to handle Company APIs
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Company'],
        operation_summary=_(
            "API to List all the companies where user is part of"),
        operation_id=_("List Companies"),
        responses={
            200: 'Login successful',
            400: 'Login Failed'
        }
    )
    def get(self, request):
        """
        `GET` API to list all users in the company.

        ---
        URL:
            <BASE_URL>/api/v1/company/
        ---
        Request:
            None
        ---
        Response:
            CompanySerializer
        ---
        """
        if not request.user:
            raise BusinessException(
                "USER_NOT_FOUND", _("The user was not found")
            )

        companies = Company.objects.filter(users=request.user)
        companies_list = CompanySerializer(companies, many=True).data

        return get_response(200, companies_list)
