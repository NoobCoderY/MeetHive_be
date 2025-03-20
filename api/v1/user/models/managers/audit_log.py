from api.core.models.base import BaseModelManager
from django.db import transaction


class AuditLogManager(BaseModelManager):
    def add_log(self, user: str, task, company='', project='', extra_fields={}):
        """
        Saves log entry to database

        Attributes:
            - user : (str) 
                - Name of the user.
            - task : (str)
                - Task which is triggered the log.
            - company : (str)
                - Company where the action is triggered.
            - project : (str)
                - Name of the project
            - extra_fields : (dict)
                - Other userful information needed for debugging
        """
        with transaction.atomic():
            return self.create(
                user=user,
                company=company,
                project=project,
                task=task,
                extra_fields=extra_fields
            )
