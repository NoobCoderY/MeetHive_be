from api.core.models import BaseModelManager


class CompanyUserManager(BaseModelManager):
    def create_company_user(self, company, user, role, **kwargs):
        """
        Creates a new CompanyUser object and returns it.

        Attributes:
            - company : (Company) - Represents the company
            - user : (User) - Represents the user
            - role : (CompanyRole) - Represents the role of the user in the company
        """
        company_user = self.model(
            company=company, user=user, role=role, **kwargs)

        return company_user

    def get_by_token(self, token: str):
        """
        Filters the CompanyUser having the token

        Attributes:
        - token : (str)
            - User's Token

        Returns: CompanyUser
        """
        company_user = self.filter(token=token).first()

        return company_user

    def get_company_user(self, company, user):
        """
        Filters the CompanyUser having the company and user

        Attributes:
        - company : (Company)
            - Company the user belongs to
        - user : (User)
            - User model

        Returns: CompanyUser
        """
        company_user = self.filter(company=company, user=user).first()
        return company_user
