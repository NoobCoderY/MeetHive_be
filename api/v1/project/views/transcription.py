from django.utils.translation import gettext_lazy as _
from django.db import transaction
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from api.core.swagger import TENANT_ID_HEADER, PROJECT_ID_HEADER
from api.core.permissions import has_company_permission, has_project_permission
from justagile_be.exceptions import BusinessException
from api.v1.project.services import TranscriptionService
from api.v1.project.serializers import TranscriptionSerializer, CreateTranscriptionSerializer, UpdateTranscriptionSerializer,CreateUploadRecordingTranscriptionSerializer
from utils import get_response ,GenericPagination
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser
from api.core.permissions import IsAuthenticated
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.utils.timezone import make_aware
from datetime import datetime



class TranscriptionView(APIView):
    """
    API view for transcription APIs for CRUD operations
    """
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Transcription'],
        operation_summary=_('API to list all transcriptions in a project'),
        operation_id=_('List transcriptions by project'),
        manual_parameters=[
            TENANT_ID_HEADER,
            PROJECT_ID_HEADER
        ],
        responses={
            200: 'Transcriptions retrieved successfully',
            400: 'Transcription list Failed'
        }
    )
    @has_company_permission(['VIEW_PROJECT'])
    @has_project_permission(['VIEW_PROJECT'])
    def get(self, request):
        current_date = make_aware(datetime.now())
        search_query = request.GET.get('search', None)
        filter_by=request.GET.get('filter', None)
        if filter_by == '1_week':
          date_from = current_date - timedelta(days=7)
        elif filter_by == '1_month':
            date_from = current_date - relativedelta(months=1)
        elif filter_by == '1_year':
            date_from = current_date - relativedelta(years=1)  
        else:
            date_from = None  
            
        transcriptions=TranscriptionService.list_transcriptions(request.project,search_query,date_from)
        paginator = GenericPagination()
        paginated_transcriptions = paginator.paginate_queryset(transcriptions, request)
        res = TranscriptionSerializer(paginated_transcriptions, many=True).data
        return paginator.get_paginated_response(res)

    @swagger_auto_schema(
        tags=['Transcription'],
        operation_summary=_('API to save transcription'),
        operation_id=_('Save Transcription'),
        request_body=CreateTranscriptionSerializer,
        manual_parameters=[
            TENANT_ID_HEADER,
            PROJECT_ID_HEADER
        ],
        responses={
            200: 'Transcription created successfully',
            400: 'Transcription creation Failed'
        }
    )
    @has_company_permission(['VIEW_PROJECT'])
    @has_project_permission(['CREATE_TRANSCRIPTION'])
    def post(self, request):
        """
        `POST` API to create a new transcription

        ---
        URL:
            <BASE_URL>/api/v1/project/transcription/
        ---
        Request:
            CreateProjectSerializer
        ---
        Response:
            ProjectSerializer
        ---
        """
        data = request.data
        # TODO: will revert back once audio feature is added to transcriptions
        # data['audio'] = request.FILES.get('audio')

        serializer = CreateTranscriptionSerializer(data=data)

        if not serializer.is_valid():
            raise BusinessException(
                "TRANSCRIPTION_CREATION_FAILED", _("The request is not valid")
            )

        data = serializer.validated_data
        transcription = TranscriptionService.create_transcription(
            data, data.get('audio'), request.project, request.project_user
        )
        res = TranscriptionSerializer(transcription).data

        return get_response(201, res)


class TranscriptionIDView(APIView):
    """
    API View to handle Transcription based on ID
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Transcription'],
        operation_summary=_('API to get transcription by ID'),
        operation_id=_('Get transcriptions by ID'),
        manual_parameters=[
            TENANT_ID_HEADER,
            PROJECT_ID_HEADER
        ],
        responses={
            200: 'Transcription retrieved successfully',
            400: 'Transcription retrieval Failed'
        }
    )
    @has_company_permission(['VIEW_PROJECT'])
    @has_project_permission(['VIEW_PROJECT'])
    def get(self, request, pk: str):
        transcription = TranscriptionService.get_transcription_by_id(
            pk, request.project
        )
        res = TranscriptionSerializer(transcription).data
        return get_response(200, res)

    @swagger_auto_schema(
        tags=['Transcription'],
        operation_summary=_('API to update transcription'),
        operation_id=_('Update transcription'),
        request_body=UpdateTranscriptionSerializer,
        manual_parameters=[
            TENANT_ID_HEADER,
            PROJECT_ID_HEADER
        ],
        responses={
            200: 'Transcription updated successfully',
            400: 'Transcription updation Failed'
        }
    )
    @has_company_permission(['VIEW_PROJECT'])
    @has_project_permission(['UPDATE_TRANSCRIPTION'])
    def put(self, request, pk):
        serializer = UpdateTranscriptionSerializer(data=request.data)
        if not serializer.is_valid():
            raise BusinessException(
                "TRANSCRIPTION_UPDATION_FAILED", _("The request is not valid")
            )

        data = serializer.validated_data
        transcription = TranscriptionService.update_transcription(
            pk, data, request.project, request.project_user
        )
        res = TranscriptionSerializer(transcription).data
        return get_response(200, res)

    @swagger_auto_schema(
        tags=['Transcription'],
        operation_summary=_('API to delete transcription'),
        operation_id=_('Delete transcription'),
        manual_parameters=[
            TENANT_ID_HEADER,
            PROJECT_ID_HEADER
        ],
        responses={
            200: 'Transcription deleted successfully',
            400: 'Transcription deletion Failed'
        }
    )
    @has_company_permission(['VIEW_PROJECT'])
    @has_project_permission(['DELETE_TRANSCRIPTION'])
    def delete(self, request, pk):
        res = TranscriptionService.delete_transcription(
            pk, request.project, request.user.get_name()
        )

        return get_response(200, res)


class UploadTranscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Transcription'],
        operation_summary=_('API to upload Recording transcription'),
        operation_id=_('Upload Recording transcription'),
        manual_parameters=[
            TENANT_ID_HEADER,
            PROJECT_ID_HEADER
        ],
        responses={
            200: 'Transcription uploaded successfully',
            400: 'Transcription upload Failed'
        }
    )
    @has_company_permission(['VIEW_PROJECT'])
    @has_project_permission(['VIEW_PROJECT'])
    def post(self, request):
        """
        `POST` API to create a new upload recordiing transcription

        ---
        URL:
            <BASE_URL>/api/v1/project/transcription/upload/
        ---
        Request:
            CreateUploadRecordingTranscriptionSerializer
        ---
        Response:
            TranscriptionSerializer
        ---
        """
        data = request.data
        serializer=CreateUploadRecordingTranscriptionSerializer(data=data)

        if not serializer.is_valid():
            
            raise BusinessException(
                "TRANSCRIPTION_CREATION_FAILED", _("The request is not valid")
            )
            
        data = serializer.validated_data
        audio=None
        transcription = TranscriptionService.create_upload_recording_transcription(
           data, audio, request.project, request.project_user
        )
        res = TranscriptionSerializer(transcription).data
        return get_response(201, res)
    
    
    

class GenerateSignedUrlView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Transcription'],
        operation_summary=_('API to generate signed url'),
        operation_id=_('Generate signed url'),
        manual_parameters=[TENANT_ID_HEADER, PROJECT_ID_HEADER],
        responses={200: 'Signed url generated successfully', 400: 'Signed url generation Failed'}
    )
    @has_company_permission(['VIEW_PROJECT'])
    @has_project_permission(['VIEW_PROJECT'])
    def post(self, request):
        file_name = request.data.get('fileName')
        file_type = request.data.get('fileType')
        user_id=request.user.id
        
        if not file_name or not file_type:
            raise BusinessException("MISSING_FILE_INFO", _("File name and file type are required"))

        signed_url = TranscriptionService.generate_signed_url(user_id,file_name, file_type)
        return get_response(200, {'signed_url': signed_url})