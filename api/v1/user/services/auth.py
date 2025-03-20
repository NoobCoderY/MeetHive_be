import jwt
from datetime import datetime
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from api.v1.user.models import User, Feedback, UserOnboarding
from api.v1.company.models import Company, CompanyUser, CompanyRole
from api.core.services import EmailService
from api.v1.company.constants.choices import StatusChoices, CompanyRoleChoices
from justagile_be.exceptions import BusinessException, UnauthorizedException
from utils import get_jwt_token
from api.v1.project.models import Project,Transcription,Summary,ProjectUser

#Crete instance of EmailService
EmailService=EmailService()


class AuthService:

    @staticmethod
    def signup_user(data: dict):
        """
        Service function to signup user.

        Attributes:
        - data : (SignupSerializer)
            - User signup request information
        """

        with transaction.atomic():
            user = User.objects.create_user(**data)
            company = Company.objects.create_company(name=user.get_name())
            role = CompanyRole.objects.get_by_name(
                CompanyRoleChoices.COMPANY_ADMIN, create=True
            )

            company_user = CompanyUser.objects.create_company_user(
                company=company, user=user, role=role
            )

            AuthService.send_signup_confirmation_mail(company_user)

            user.save()
            company.save()
            company_user.save()

            return user

    @staticmethod
    def send_signup_confirmation_mail(company_user: CompanyUser):
        """
        Service function to send signup confirmation email to the user after signup

        Attributes:
        - user : (CompanyUser)
            - CompanyUser data model indicating the signup user
        """

        context = {
            "name": company_user.user.first_name,
            "confirmation_link": f"{settings.JA_FRONTEND_URL}/account/verify/{company_user.token}",
            "support_link": f"{settings.JA_FRONTEND_URL}/support",
        }

        EmailService.send_mail(
            "emails/account/signup_confirmation.html",
            _("Confirm your account"),
            company_user.user.email, context
        )

    @staticmethod
    def verify_user(company_user: CompanyUser):
        """
        Service function to verify the user after signup

        Attributes:
        - company_user : (CompanyUser)
            - CompanyUser data model indicating the signup user
        """
        with transaction.atomic():
            company_user.is_active = True
            company_user.company.status = StatusChoices.ACTIVE
            company_user.user.is_active = True
            company_user.user.save()
            company_user.company.save()
            company_user.save()

    @staticmethod
    def update_password(password: str, token: str):
        """
        Service function to update the user's password

        Attributes:
        - user : (User)
            - User data model indicating the signup user
        - password : (str)
            - New password to update
        """
        company_user = CompanyUser.objects.get_by_token(token)
        if company_user is None:
            raise BusinessException(
                "TOKEN_INVALID", _(
                    "User with the token does not exist")
            )

        user = company_user.user
        with transaction.atomic():
            user.set_password(password)
            user.save()

        AuthService.confirmation_email(user)

    @staticmethod
    def forgot_password(user: User):
        """
       Service function to send forgot password confirmation email to the user after submit email

       Attributes:
       - user : (User)
           - User data model indicating the user
       """
        company_user = CompanyUser.objects.filter(user=user.id).first()
        context = {
                    "name": user.first_name,
                    "confirmation_link": f"{settings.JA_FRONTEND_URL}/reset-password/{company_user.token}",
                    "support_link": f"{settings.JA_FRONTEND_URL}/support"
                }

        EmailService.send_mail(
                    template="emails/account/forgot_password_confirmation.html",
                    subject=_("Reset your password"),
                    to=user.email,
                    context=context
                )

                

    def refresh_token(token: str):
        """
        Service function to refresh access token

        Attributes:
        - token : (str)
            - Refresh token to get new access token
        """

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            payload_data=payload['data']
            token = get_jwt_token(
                payload_data, datetime.now() + settings.JWT_ACCESS_TOKEN_LIFETIME
            )

            return token
        except jwt.ExpiredSignatureError: \


            raise UnauthorizedException(
                "INVALID_TOKEN", _("Invalid Refresh token"))

    def confirmation_email(user: User):
        """
        Service function to send  confirmation email to the user after reset password

        Attributes:
        - user : (User)
            - User data model 
        """

        context = {
            "name": user.first_name,
            "confirmation_link": f"{settings.JA_FRONTEND_URL}/login",
            "support_link": f"{settings.JA_FRONTEND_URL}/support"
        }

        EmailService.send_mail(
            "emails/account/change_password_confirmation.html",
            _("Successfully Password Updated"),
            user.email, context
        )
        
        
    @staticmethod
    def edit_profile(user: User, data: dict):
        user = User.objects.get_by_id(id=user.id)
        if user is None:
            raise BusinessException(
                "USER_NOT_FOUND", _("User does not exist")
            )
        
        for field in ['first_name', 'last_name', 'email', 'profile_picture']:
            if field in data:
                setattr(user, field, data[field])
        
        user.save()
        return user
    
    @staticmethod 
    def send_delete_confirmation_mail(user: User):
        context = {
            "first_name": user.first_name,
            "last_name": user.last_name
            
        }

        EmailService.send_mail(
            "emails/account/delete_account_confirmation.html",
            _("Delete your account"),
            user.email, context
        )
    
    @staticmethod 
    def delete_bulk_transcription_summary(project_id: int):
        try:
            transcriptions=Transcription.objects.filter(project_id=project_id)
            for transcription in transcriptions:
                        summary = Summary.objects.filter(transcription_id=transcription.id).first()
                        summary.is_deleted = True
                        summary.save()
                        transcription.is_deleted = True
                        transcription.save()
        except Exception as e:
            raise BusinessException("DELETE_FAILED", _("Failed to delete transcription summaries"))
        
    @staticmethod
    def delete_profile(user_id: int):
        """
        Service function to delete user profile

        Attributes:
        - user_id : (int)
        """
        try:
            with transaction.atomic():
            
            #1->delete onboarding data
                user_onboarding =UserOnboarding.objects.get_by_user(user_id)
                if user_onboarding:
                    user_onboarding.is_deleted = True
                    user_onboarding.save()
    
                
            # 2-> delete feedback
                feedback=Feedback.objects.get_by_id(user_id)
                if feedback:
                    feedback.is_deleted = True
                    feedback.save()
                
        
            # 3-> delete company_user
                company_user=CompanyUser.objects.filter(user=user_id).first()
                if company_user:
                    # 4->delete company
                    company = Company.objects.filter(users=company_user.user.id).first()
                    if company:
                        company.is_deleted = True
                        company.save()
                
                    # 5-> delete project_user and project
                    project_users = ProjectUser.objects.filter(user=company_user)
                    for project_user in project_users:
                            AuthService.delete_bulk_transcription_summary(project_user.project.id)
                            project_user.project.is_deleted = True
                            project_user.project.save()
                            project_user.is_deleted = True
                            project_user.save()
                        
                    company_user.is_deleted = True
                    company_user.save()
                
                
                # 6-> delete user
                user = User.objects.get_by_id(id=user_id)
                user.is_deleted = True
                user.save()
                AuthService.send_delete_confirmation_mail(user)    

        
        except Exception as e:
            raise BusinessException(
                "DELETE_PROFILE_FAILED", _("Failed to delete profile"))
        
        
        
       
        
