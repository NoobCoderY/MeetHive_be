from django.db import transaction
from api.v1.company.models import CompanyUser
from api.v1.project.models import Project, ProjectUser, ProjectRole, Transcription, Summary
from api.v1.project.serializers import TranscriptionListItemSerializer, SummaryListItemSerializer
from api.v1.project.models import ProjectRoleChoices


class ProjectService:

    @staticmethod
    def create_project_user(project, user, role):
        """
        Service function to create project user based on 

        Attributes:
            - project : (Project) - Project model
            - user : (CompanyUser) - CompanyUser model
            - role : (str) - Role of the user in the project
        """

        with transaction.atomic():
            project_role = ProjectRole.objects.get_by_name(role, create=True)
            project_user = ProjectUser.objects.create(
                project=project,
                user=user,
                role=project_role,
                is_active=True
            )
            return project_user

    @staticmethod
    def create_project(data: dict, company, creator):
        """
        Service function to create project

        Attributes:
        - data : (CreateProjectSerializer)
            - Project creation request information
        - company : (Company)
            - Company where the project is part of.
        - creator : (CompanyUser | None)
            - Creator of the project
        """

        with transaction.atomic():
            project = Project.objects.create(
                **data,
                company=company,
                created_by=creator
            )

            project_admin = ProjectService.create_project_user(
                project, creator, ProjectRoleChoices.ADMIN
            )

            return project

    def update_project(data: dict, project: Project, updated_by: CompanyUser):
        """
        Service function to update project

        Attributes:
        - data : (UpdateProjectSerializer)
            - Project data to update
        - project : (Project)
            - Project data model
        - updated_by : (CompanyUser)
            - The company user who updated the project
        """
        with transaction.atomic():
            project.name = data['name']
            project.description = data['description']
            project.updated_by = updated_by

            project.save()

        return project

    def search(query: str, project):

        if not query:
            return {
                "transcriptions": [],
                "summaries": []
            }
    
        transcriptions = Transcription.objects.search(query, project)

        summaries = Summary.objects.search(query, project)
        transcription_list = TranscriptionListItemSerializer(
            transcriptions, many=True).data
       
        summaries_list = SummaryListItemSerializer(summaries, many=True).data
        
        return {
            "transcriptions": transcription_list,
            "summaries": summaries_list
        }