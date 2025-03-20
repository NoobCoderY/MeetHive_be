from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from api.v1.user.serializers.auth import EditProfileSerializer, ForgotPasswordSerializer
from utils import get_response
from api.v1.user.serializers import LoginSerializer, UserSerializer, SignupSerializer, UserVerifySerializer, \
    UpdateUserPasswordSerializer, RefreshTokenSerializer
from django.utils.translation import gettext_lazy as _
from justagile_be.exceptions import BusinessException
from utils import get_jwt_token
import datetime
from django.conf import settings
from api.v1.user.services import AuthService
from drf_yasg import openapi
from api.core.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class LoginView(APIView):
    """
    API view to handle user login
    """

    @swagger_auto_schema(
        tags=['user'],
        operation_summary=_("API to Login user"),
        operation_id=_("Login"),
        request_body=LoginSerializer,
        responses={
            200: 'Login successful',
            400: 'Login Failed'
        }
    )
    def post(self, request):
        """
        `POST` API to handle user login.

        ---
        URL:
            <BASE_URL>/api/v1/user/auth/login/
        ---
        Request:
            LoginSerializer
        ---
        Response:
            UserSerializer
        ---
        """
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            raise BusinessException(
                "LOGIN_FAILED", _("The request is not valid"))

        res = UserSerializer(serializer.validated_data).data
        jwt_payload = {'user': res['id']}
        res['access_token'] = get_jwt_token(
            jwt_payload, datetime.datetime.now() + settings.JWT_ACCESS_TOKEN_LIFETIME)
        res['refresh_token'] = get_jwt_token(
            jwt_payload, datetime.datetime.now() + settings.JWT_REFRESH_TOKEN_LIFETIME)

        return get_response(200, res)


class SignupView(APIView):
    """
    API view to handle user login
    """
    @swagger_auto_schema(
        tags=['user'],
        operation_summary=_("API to Signup user"),
        operation_id=_("Signup"),
        request_body=SignupSerializer,
        responses={
            200: 'Signup successful',
            400: 'Signup Failed'
        }
    )
    def post(self, request):
        """
        `POST` API to handle user signup.

        ---
        URL:
            <BASE_URL>/api/v1/user/auth/signup/
        ---
        Request:
            SignupSerializer
        ---
        Response:
            UserSerializer
        ---
        """

        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            raise BusinessException(
                "SIGNUP_FAILED", serializer.errors.values())

        AuthService.signup_user(serializer.validated_data)

        return get_response(200, True)


class UserVerifyView(APIView):
    """
    API View to handle verification of user.
    """
    @swagger_auto_schema(
        tags=['user'],
        operation_summary=_("API to Verify user"),
        operation_id=_("Verify User"),
        request_body=UserVerifySerializer,
        responses={
            200: 'Verification successful',
            400: 'Verification Failed'
        }
    )
    def post(self, request):
        """
        `POST` API to handle user verification.

        ---
        URL:
            <BASE_URL>/api/v1/user/auth/verify/
        ---
        Request:
            UserVerifySerializer
        ---
        Response:
            boolean
        ---
        """
        serializer = UserVerifySerializer(data=request.data)
        if not serializer.is_valid():
            raise BusinessException(
                "TOKEN_INVALID", serializer.errors.values()
            )

        res = AuthService.verify_user(serializer.validated_data)
        return get_response(200, True)


class UpdatePasswordView(APIView):
    """
    API View to update password of user.
    """
    @swagger_auto_schema(
        tags=['user'],
        operation_summary=_("API to update user password"),
        operation_id=_("Update password"),
        request_body=UpdateUserPasswordSerializer,
        manual_parameters=[
            openapi.Parameter(
                name="token",
                required=True,
                type=openapi.TYPE_STRING,
                in_=openapi.IN_PATH,
                description="User Token",
            ),
        ],
        responses={
            200: 'Password update successful',
            400: 'Password update Failed'
        }
    )
    def put(self, request, token):
        """
        `PUT` API to handle user password updation.

        ---
        URL:
            <BASE_URL>/api/v1/user/auth/update-password/<str:token>/
        ---
        Request:
            UserVerifySerializer
        ---
        Response:
            boolean
        ---
        """
        serializer = UpdateUserPasswordSerializer(
            data=request.data
        )
        if not serializer.is_valid():
            raise BusinessException(
                "TOKEN_INVALID", serializer.errors.values()
            )

        AuthService.update_password(
            serializer.data.get('password'), token
        )
        return get_response(200, True)

class ForgotPasswordView(APIView):
    """
    API View to Verify User Email For Forgot Password
    
     ---
        URL:
            <BASE_URL>/api/v1/user/auth/forgot-password/
        ---
        Request:
            ForgotPasswordSerialzer
        ---
        Response:
            boolean
        ---
    
    """
    @swagger_auto_schema(
        tags=['user'],
        operation_summary=_("API to Verify Email For Forgot Passowrd"),
        operation_id=_("Verify Forgot Password User Email"),
        request_body=ForgotPasswordSerializer,
        responses={
            200: 'Verification successful',
            400: 'Verification Failed'
        }
    )
    
    def post(self,request):

        serializer=ForgotPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            raise BusinessException("Forgot_password_failed", _("The request is not valid"))
        
        res=AuthService.forgot_password(serializer.validated_data)
        return get_response(200,True, None, None) 

class RefreshTokenView(APIView):
    """
    API View to handle refresh access token.
    """
    @swagger_auto_schema(
        tags=['user'],
        operation_summary=_("API to Refresh token"),
        operation_id=_("Refresh Token"),
        request_body=RefreshTokenSerializer,
        responses={
            200: 'Token refresh successful',
            400: 'Token refresh Failed'
        }
    )
    def post(self, request):
        """
        `POST` API to handle refresh access token.

        ---
        URL:
            <BASE_URL>/api/v1/user/auth/refresh/
        ---
        Request:
            RefreshTokenSerializer
        ---
        Response:
            boolean
        ---
        """
        serializer = RefreshTokenSerializer(data=request.data)
        if not serializer.is_valid():
            raise BusinessException(
                "TOKEN_INVALID", serializer.errors.values()
            )

        res = AuthService.refresh_token(serializer.data['token'])
        return get_response(200, res)



class EditProfileView(APIView):
    """
    API View to handle edit profile.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    @swagger_auto_schema(
        tags=['user'],
        operation_summary=_("API to Edit profile"),
        operation_id=_("Edit Profile"),
        request_body=EditProfileSerializer,
        responses={
            200: 'Profile update successful',
            400: 'Profile update Failed'
        }
    )
    def put(self,request):
       
        """
        `PUT` API to handle edit profile.

        ---
        URL:
            <BASE_URL>/api/v1/user/auth/edit-profile/
        ---
        Request:
            EditProfileSerializer
        ---
        Response:
            UserSerializer
        ---
        """
        serializer =EditProfileSerializer(data=request.data,context={'request':request})    
    
        if not serializer.is_valid():
            raise BusinessException(
                "EDIT_PROFILE_FAILED", serializer.errors.values()
            )
        
        res=AuthService.edit_profile(request.user,serializer.validated_data)
        user_data=UserSerializer(res).data
        return get_response(200, user_data)    
        


class DeleteProfileView(APIView):
    """
    API View to handle user profile deletion.
    """
    @swagger_auto_schema(
        tags=['user'],
        operation_summary=_("API to delete user profile"),
        operation_id=_("Delete Profile"),
        responses={
            200: 'Profile deleted successfully',
            400: 'Profile deletion Failed'
        }
    )
    def delete(self, request):
        """
        `DELETE` API to handle user profile deletion.

        ---
        URL:    
            <BASE_URL>/api/v1/user/auth/delete-profile/
        ---
        Request:
            None
        ---
        Response:
            boolean
        ---
        """
        res = AuthService.delete_profile(request.user.id)
        return get_response(200, res)
    

