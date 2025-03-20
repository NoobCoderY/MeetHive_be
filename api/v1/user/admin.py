from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Django admin UI interface for User model
    """
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'email')
    ordering = ('created_at',)


@admin.register(UserOnboarding)
class UserOnboardingAdmin(admin.ModelAdmin):
    """
    Django admin UI interface for UserOnboarding model
    """
    list_display = ('id', 'user',)
    search_fields = (
        'user', 'profession', 'interests'
    )
    ordering = ('created_at',)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """
    Django admin UI interface for AuditLog model
    """
    list_display = ('user', 'company', 'project', 'task', 'created_at')
    search_fields = ('user', 'company', 'project', 'task')
    ordering = ('-created_at',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Django admin UI interface for Feedback model
    """
    list_display = ('user', 'feedback', 'reaction',)
    search_fields = ('user', 'feedback')
    ordering = ('-created_at',)
