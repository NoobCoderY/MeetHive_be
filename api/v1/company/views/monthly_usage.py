from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from api.core.swagger import TENANT_ID_HEADER
from utils import get_response

from api.core.permissions import has_company_permission
from api.v1.company.models import CompanyMonthlyUsage
from api.v1.company.serializers import CompanyMonthlyUsageSerializer
from api.core.permissions import IsAuthenticated


class CompanyMonthlyUsageView(APIView):
    """
    API View for monthly usage APIs
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Company'],
        operation_summary=_('API to get company`s month usage'),
        operation_id=_('Get Monthly usage of a company'),
        manual_parameters=[TENANT_ID_HEADER],
        responses={
            200: 'Monthly usage retrieved successfully',
            400: 'Failed to get monthly usage'
        }
    )
    @has_company_permission(['VIEW_COMPANY'])
    def get(self, request):
        monthly_usage = CompanyMonthlyUsage.objects.get_current_month_usage(
            request.company, create=True
        )

        res = CompanyMonthlyUsageSerializer(monthly_usage).data
        return get_response(200, res)
