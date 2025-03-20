from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from justagile_be.exceptions import BusinessException
from django.utils.translation import gettext_lazy as _
from api.v1.user.models import User
from api.v1.company.models import CompanyUser


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login which validates user login request

    Attributes:
    - email : (str)
        - Email of the user
    - password : (str)
        - password of the user
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Validates email and password and authenticates the user based on the data provided.

        Attributes:
        - data : (dict)
            - dict object containing email and password

        Returns:
        - user : (User) 
            - The user object if authentication is successful
        """

        email = data.get("email")
        password = data.get("password")
        if email and password:
            user = User.objects.filter(email=email, is_deleted=False).first()
            if user:
                if not user.is_active:
                    raise BusinessException(
                        "USER_INACTIVE", _("User is not active"))
                is_authenticated = check_password(password, user.password)
                if not is_authenticated:
                    raise BusinessException(
                        "LOGIN_FAILED", _("User is not authenticated"))
                return user
            else:
                raise BusinessException(
                    "INVALID_CREDENTIALS", _("Invalid credentials"))
        else:
            raise BusinessException(
                "REQUEST_MISSING", _("Email or password missing"))


class SignupSerializer(serializers.Serializer):
    """
    Serializer for Signup API which validates user signup request

    Attributes:
    - first_name : (str)
        - First name of the user
    - last_name : (str)
        - Last name of the user
    - email : (str)
        - Email of the user
    - password : (str)
        - password of the user
    """

    first_name = serializers.CharField(required=True, error_messages={
                                       'required': _('First name is required.')})
    last_name = serializers.CharField(
        required=False, allow_blank=True, default="")
    email = serializers.EmailField(required=True, error_messages={
        'required': _('Email is required.')})
    password = serializers.CharField(required=True, write_only=True, error_messages={
        'required': _('Password is required.')})

    def validate(self, data):
        data['username'] = data['email']
        user = User.objects.filter(email=data['email']).first()
        if user:
            raise BusinessException("USER_EXIST", _("User already exist"))

        return data


class UserVerifySerializer(serializers.Serializer):
    """
    Serializer for user verify API which validates user signup request

    Attributes:
    - token : (str)
        - Token sent via email after signup
    """
    token = serializers.CharField(
        required=True, error_messages={'required': _('Token is required.')}
    )

    def validate(self, data):
        """
        Validates request data and check if the user with provided token exist or not.

        Attributes:
        - data : (dict)
            - dict object containing token

        Returns:
        - company_user : (CompanyUser)
            - The CompanyUser object if user exists
        """

        if not data.get('token'):
            raise BusinessException(
                "TOKEN_REQUIRED", _("Token is required.")
            )
        company_user = CompanyUser.objects.get_by_token(data['token'])
        if not company_user:
            raise BusinessException(
                "TOKEN_INVALID", _("User with the token does not exist")
            )

        return company_user


class UpdateUserPasswordSerializer(serializers.Serializer):
    """
    Serializer for user password update API

    Attributes:
    - password : (str)
        - New password that need to be updated
    """

    password = serializers.CharField(
        required=True, error_messages={'required': _('Password is required.')}
    )
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, error_messages={
        'required': _('Email is required.')})
    
    def validate(self, data):
        user = User.objects.filter(email=data['email']).first() 
        if not user:
            raise BusinessException(
                "USER_NOT_FOUND", _("User with the email does not exist")
            )
        return user    


class RefreshTokenSerializer(serializers.Serializer):
    """
    Serializer for refresh token API

    Attributes:
    - token : (str)
        - The refersh token to get new access token
    """

    token = serializers.CharField(required=True, error_messages={
                                  'required': _('Token is required.')})





class EditProfileSerializer(serializers.Serializer):
    """
    Serializer for the edit profile API.

    Attributes:
    - first_name: (str) - First name of the user, optional
    - last_name: (str) - Last name of the user, optional
    - email: (str) - Email of the user, optional
    - profile_picture: (ImageField) - Profile picture of the user, optional
    """
    

    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    profile_picture = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_picture']
        
    def validate_email(self, value):
        """
        Check if the provided email is already in use by another user.
        """
        user = User.objects.filter(email=value).first()
        if user and user != self.context['request'].user:
            raise serializers.ValidationError(_('Email already in use.'))
        return value    
