from api.core.models import BaseModelManager


class CompanyManager(BaseModelManager):
    def create_company(self, name, **kwargs):
        """
        Returns a new Company Object with name and data provided
        """
        company = self.model(name=name, **kwargs)

        return company
