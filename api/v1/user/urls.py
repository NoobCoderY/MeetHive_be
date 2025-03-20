from django.urls import path
from . import views


urlpatterns = [
    path('auth/login/', views.LoginView.as_view(), name="login_user"),
    path('auth/signup/', views.SignupView.as_view(), name="user_signup"),
    path('auth/verify/', views.UserVerifyView.as_view(), name="verify_user"),
    path(
        'auth/update-password/<str:token>/',
        views.UpdatePasswordView.as_view(), name="update_password"
    ),
    path(
        'auth/forgot-password/',
        views.ForgotPasswordView.as_view(), name="forgot-password"
    ),

    path('auth/refresh/', views.RefreshTokenView.as_view(), name="refresh_token"),
    path('auth/edit-profile/', views.EditProfileView.as_view(), name="edit_profile"),
    path('auth/delete-profile/', views.DeleteProfileView.as_view(), name="delete_profile"),

    path(
        'onboarding/<str:user>/',
        views.UserOnboardingView.as_view(), name="user_onboarding"
    ),

    path(
        'feedback/',
        views.FeedbackView.as_view(), name="user_feedback"
    ),

    path(
        'support/',
        views.SupportView.as_view(), name="user_support"
    )

]
