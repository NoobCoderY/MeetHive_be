from api.core.models import BaseModelManager


class ProjectUserManager(BaseModelManager):
    def get_project_user(self, project, user):
        return self.filter(project=project, user=user).first()
