from django.utils.translation import gettext_lazy as _
from django.db import transaction
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from utils import get_response
from api.core.permissions import IsAuthenticated
from api.core.swagger import TENANT_ID_HEADER, PROJECT_ID_HEADER
from api.core.permissions import has_company_permission, has_project_permission
from justagile_be.exceptions import BusinessException
from api.v1.project.serializers import CreateProjectSerializer, ProjectSerializer, UpdateProjectSerializer
from api.v1.project.services import ProjectService
from api.v1.project.models import Project
from utils import GenericPagination
from django.db.models.functions import Coalesce



class ProjectView(APIView):
    """
    API view for project level APIs
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Project'],
        operation_summary=_('API to List user projects'),
        operation_id=_('List Projects'),
        manual_parameters=[
            TENANT_ID_HEADER
        ],
        responses={
            201: 'Project created successfully',
            400: 'Project creation Failed'
        }
    )
    @has_company_permission(['VIEW_PROJECT'])
    def get(self, request):
        """
        `GET` API to list projects

        ---
        URL:
            <BASE_URL>/api/v1/project/
        ---
        Request:
            None
        ---
        Response:
            List[ProjectSerializer]
        ---
        """
        search_query = request.GET.get('search')
        projects = Project.objects.filter(
                        company=request.company, users=request.company_user
                        ).annotate(
                        updated_or_created=Coalesce('updated_at', 'created_at')
                        ).order_by('-updated_or_created')

        if search_query:
            projects = projects.filter(name__icontains=search_query)

        paginator = GenericPagination()
        paginated_projects = paginator.paginate_queryset(projects, request)
        serialized_data = ProjectSerializer(paginated_projects, many=True).data

        return paginator.get_paginated_response(serialized_data)


    @swagger_auto_schema(
        tags=['Project'],
        operation_summary=_('API to create new project'),
        operation_id=_('Create Project'),
        request_body=CreateProjectSerializer,
        manual_parameters=[
            TENANT_ID_HEADER
        ],
        responses={
            201: 'Project created successfully',
            400: 'Project creation Failed'
        }
    )
    @has_company_permission(['CREATE_PROJECT'])
    def post(self, request):
        """
        `POST` API to create a new project

        ---
        URL:
            <BASE_URL>/api/v1/project/
        ---
        Request:
            CreateProjectSerializer
        ---
        Response:
            ProjectSerializer
        ---
        """
        serializer = CreateProjectSerializer(data=request.data)

        if not serializer.is_valid():
            raise BusinessException(
                "PROJECT_CREATION_FAILED", _("The request is not valid")
            )

        data = serializer.validated_data
        project = ProjectService.create_project(
            data, request.company, request.company_user
        )

        res = ProjectSerializer(project).data

        return get_response(201, res)

    @swagger_auto_schema(
        tags=['Project'],
        operation_summary=_('API to update project details'),
        operation_id=_('Update Project'),
        request_body=UpdateProjectSerializer,
        manual_parameters=[
            TENANT_ID_HEADER,
            PROJECT_ID_HEADER
        ],
        responses={
            200: 'Project retrieved successfully',
            400: 'Project creation Failed'
        }
    )
    @has_company_permission(['VIEW_PROJECT'])
    @has_project_permission(['UPDATE_PROJECT'])
    def put(self, request):
        """
        `PUT` API to update a project details

        ---
        URL:
            <BASE_URL>/api/v1/project/
        ---
        Request:
            UpdateProjectSerializer
        ---
        Response:
            ProjectSerializer
        ---
        """

        serializer = UpdateProjectSerializer(data=request.data)
        if not serializer.is_valid():
            raise BusinessException(
                "UPDATE_PROJECT_FAILED", serializer.errors.values()
            )

        project = ProjectService.update_project(
            request.data, request.project, request.company_user
        )
        res = ProjectSerializer(project).data
        return get_response(200, res)


class ProjectIDView(APIView):
    """
    API view for project level APIs by ID
    """

    @swagger_auto_schema(
        tags=['Project'],
        operation_summary=_('API to get project by ID'),
        operation_id=_('Get Project by ID'),
        manual_parameters=[
            TENANT_ID_HEADER,
            PROJECT_ID_HEADER
        ],
        responses={
            200: 'Project retrieved successfully',
            400: 'Project creation Failed'
        }
    )
    @has_company_permission(['VIEW_PROJECT'])
    @has_project_permission(['VIEW_PROJECT'])
    def get(self, request, pk):
        """
        `GET` API to get a project by ID

        ---
        URL:
            <BASE_URL>/api/v1/project/get/<pk>/
        ---
        Request:
            pk - Project ID passed as URL params
        ---
        Response:
            ProjectSerializer
        ---
        """
        project = Project.objects.get_by_id(pk)
        if project is None:
            raise BusinessException("PROJECT_NOT_FOUND", _(
                'The project you are looking for does not exist')
            )

        res = ProjectSerializer(project).data
        return get_response(200, res)


class SearchView(APIView):
    """
    API View to handle search operation across project
    """

    @swagger_auto_schema(
        tags=['Project'],
        operation_summary=_('API to search text in transcription and summary'),
        operation_id=_('Search project'),
        manual_parameters=[
            TENANT_ID_HEADER,
            PROJECT_ID_HEADER,
            openapi.Parameter(
                'query', openapi.IN_QUERY,
                description="Search Text", type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: 'Search results retrieved successfully',
            400: 'Search results retrieval Failed'
        }
    )
    @has_company_permission(['VIEW_PROJECT'])
    @has_project_permission(['VIEW_PROJECT'])
    def get(self, request):
        """
        `GET` API to get a projectwise search

        ---
        URL:
            <BASE_URL>/api/v1/project/search/?query=<search_text>
        ---
        Request:
            query - search text
        ---
        Response:
            { "transcriptions": TranscriptionListItemSerializer[], "summaries": SummaryListItemSerializer[] }
        ---
        """
        query = request.GET.get('query')
        res = ProjectService.search(query, request.project)

        return get_response(200, res)
