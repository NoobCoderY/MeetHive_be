from rest_framework.views import APIView
from api.core.permissions.company_permissions import has_company_permission
from api.core.permissions.project_permissions import has_project_permission
from api.v1.project.serializers.summary import SummarySerializer
from api.v1.project.serializers import CreateSummarySerializer ,UpdateSummarySerializer
from api.core.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.core.swagger import TENANT_ID_HEADER, PROJECT_ID_HEADER
from django.utils.translation import gettext_lazy as _
from justagile_be.exceptions import BusinessException
from api.v1.project.services import SummaryService
from utils import  get_response
from utils import GenericPagination


class SummaryView(APIView):
    """
    API View to List all summary under project
    """
    permission_classes = [IsAuthenticated]
 
    @swagger_auto_schema(
        tags=['Summary'],
        operation_summary=_('API to List summary and '),
        operation_id=_('List summary under project '),
        manual_parameters=[
            TENANT_ID_HEADER,
            PROJECT_ID_HEADER
        ],
        responses={
            200: 'Summary retrieved successfully',
            400: 'Summary retrieved  Failed'
        }
    )
    @has_company_permission(['VIEW_PROJECT'])
    @has_project_permission(['VIEW_SUMMARY'])
    def get(self, request):
        search_query = request.GET.get('search', None)
        summary=SummaryService.list_summary(request.project,search_query)
        paginator = GenericPagination()
        paginated_summary = paginator.paginate_queryset(summary, request)
        res = SummarySerializer(paginated_summary, many=True).data
        return paginator.get_paginated_response(res)
    
    """
    API View to generate a summary using Hugging Face Inference API and store it.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        tags=['Summary'],
        operation_summary=_('API to Generate summary and create summary'),
        operation_id=_('Generate summary by transcription'),
        request_body=CreateSummarySerializer,
        manual_parameters=[
            TENANT_ID_HEADER,
            PROJECT_ID_HEADER
        ],
        responses={
            201: 'Summary created successfully',
            400: 'Summary creation Failed'
        }
    )
    
    @has_company_permission(['VIEW_PROJECT'])
    @has_project_permission(['CREATE_SUMMARY'])
    def post(self, request):
        """
        `POST` API to generate and crate a summary

        ---
        URL:
            <BASE_URL>/api/v1/project/summary/
        ---
        Request:
            CreateSummarySerializer
        ---
        Response:
            SummarySerializer
        ---
        """
        data=request.data
        
        serializer=CreateSummarySerializer(data=data)
        if not serializer.is_valid():
            raise BusinessException(
                "Summary_CREATION_FAILED", _("The request is not valid")
            )
        
        data = serializer.validated_data
        
        summary=SummaryService.create_summary(data,request.project, request.project_user)
        
        res=SummarySerializer(summary).data
        
        return get_response(201, res)
      

class SummaryIdView(APIView):
    """
    API View to handle Summary based on ID
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Summary'],
        operation_summary=_('API to get summary by ID'),
        operation_id=_('Get summary by ID'),
        manual_parameters=[
            TENANT_ID_HEADER,
            PROJECT_ID_HEADER
        ],
        responses={
            200: 'summary retrieved successfully',
            400: 'summary retrieval Failed'
        }
    )
    @has_company_permission(['VIEW_PROJECT'])
    @has_project_permission(['VIEW_PROJECT'])
    def get(self, request, pk: str):
        summary = SummaryService.get_summary_by_id(
            pk, request.project
        )
        res = SummarySerializer(summary).data
        return get_response(200, res)

    @swagger_auto_schema(
        tags=['Summary'],
        operation_summary=_('API to update summary'),
        operation_id=_('Update summary'),
        request_body=UpdateSummarySerializer,
        manual_parameters=[
            TENANT_ID_HEADER,
            PROJECT_ID_HEADER
        ],
        responses={
            200: 'Summary updated successfully',
            400: 'Summary updation Failed'
        }
    )
    @has_company_permission(['VIEW_PROJECT'])
    @has_project_permission(['UPDATE_SUMMARY'])
    def put(self, request, pk):
        serializer = UpdateSummarySerializer(data=request.data)
        if not serializer.is_valid():
            raise BusinessException(
                "SUMMARY_UPDATION_FAILED", _("The request is not valid")
            )

        data = serializer.validated_data
        summary = SummaryService.update_summary(
            pk, data, request.project, request.project_user
        )
        res = SummarySerializer(summary).data
        return get_response(200, res)

    @swagger_auto_schema(
        tags=['Summary'],
        operation_summary=_('API to delete summary'),
        operation_id=_('Delete summary'),
        manual_parameters=[
            TENANT_ID_HEADER,
            PROJECT_ID_HEADER
        ],
        responses={
            200: 'Summary deleted successfully',
            400: 'Summary deletion Failed'
        }
    )
    @has_company_permission(['VIEW_PROJECT'])
    @has_project_permission(['DELETE_SUMMARY'])
    def delete(self, request, pk):
        res = SummaryService.delete_summary(
            pk, request.project, request.user.get_name()
        )

        return get_response(200, res)
      
          
     