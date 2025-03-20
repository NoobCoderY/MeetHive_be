from api.core.models import BaseModelManager
from api.v1.user.constants import AuditLogTaskChoices
from django.db import transaction
from api.v1.company.models import CompanyMonthlyUsage
from api.v1.user.models import AuditLog
from django.db.models import Q
import threading


class SummaryManager(BaseModelManager):

    lock = threading.Lock()

    def list_by_project(self, project):
        """
        List all the summary by project ID
        """
        return self.filter(project=project, is_deleted=False)

    def create_summary(self, data, project, project_user):
        """
        To create new summary
        """
        with self.lock:
            with transaction.atomic():
                CompanyMonthlyUsage.objects.add_summary_count(
                    project.company
                )

                result = self.create(
                    title=data.get('title'),
                    summary=data.get('summary'),
                    transcription=data.get('transcription'),
                    project=project,
                    created_by=project_user,
                    updated_by=project_user,
                    status=data.get('status')
                )

                AuditLog.objects.add_log(
                    user=project_user.user.user.get_name(),
                    company=project_user.user.company.name,
                    project=project.name,
                    # add proper permission
                    task=AuditLogTaskChoices.CREATE_SUMMARY,
                    extra_fields={
                        'id': f"{result.id}",
                        'name': result.title
                    }
                )

                return result

    def search(self, query, project):
        return self.filter(Q(title__icontains=query) | Q(summary__icontains=query), project=project)
