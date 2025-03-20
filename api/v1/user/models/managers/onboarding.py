from api.core.models import BaseModelManager


class UserOnboardingManager(BaseModelManager):
    def get_by_user(self, user_id: str):
        """
        Retrieves the onboarding information by it's user id and if it is not soft deleted

        Attributes:
        - pk : (str | int)
            - The primary key of the record
        """
        try:
            
            return self.get(user=user_id, is_deleted=False)
        except self.model.DoesNotExist:
            return None
