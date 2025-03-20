from django.db.models import Q
from api.core.models import BaseModelManager
from api.v1.user.constants import AuditLogTaskChoices
from django.db import transaction
from api.v1.company.models import CompanyMonthlyUsage
from api.v1.user.models import AuditLog
from django.contrib.postgres.search import SearchVector


class TranscriptionManager(BaseModelManager):
    def list_by_project(self, project):
        """
        List all the transcriptions by project ID
        """
        return self.filter(project=project, is_deleted=False)

    def create_transcription(self, data, project, project_user, audio_file,status='completed'):
        """
        To create new transcription
        """
        with transaction.atomic():
            CompanyMonthlyUsage.objects.add_transcription_duration(
                project.company, data.get('duration') or 0
            )

            result = self.create(
                title=data.get('title'),
                description=data.get('description') or '',
                audio=audio_file,
                text=data.get('text'),
                project=project,
                created_by=project_user,
                updated_by=project_user,
                status=status,
                audio_url=data.get('audio_url')
            )

            AuditLog.objects.add_log(
                user=project_user.user.user.get_name(),
                company=project_user.user.company.name,
                project=project.name,
                task=AuditLogTaskChoices.CREATE_TRANSCRIPTION,
                extra_fields={
                    'id': f"{result.id}",
                    'name': result.title
                }
            )

            return result

    def search(self, query, project):
        """
        Search transcriptions based on query in project
        """
        return (
            self.filter(Q(title__icontains=query) | Q(text__icontains=query), project=project)
       )
