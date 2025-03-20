from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Django admin UI interface for Project model
    """
    list_display = ('name', 'status')
    search_fields = ('name',)
    ordering = ('created_at',)


@admin.register(ProjectRole)
class ProjectAdmin(admin.ModelAdmin):
    """
    Django admin UI interface for ProjectRole model
    """
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(ProjectUser)
class ProjectAdmin(admin.ModelAdmin):
    """
    Django admin UI interface for ProjectUser model
    """
    list_display = ('user', 'project')
    search_fields = ('user', 'project')
    ordering = ('user',)


@admin.register(Transcription)
class TranscriptionAdmin(admin.ModelAdmin):
    """
    Django admin UI interface for Transcription model
    """
    list_display = ('title',)
    search_fields = ('title',)
    ordering = ('updated_at',)


@admin.register(ProjectMeeting)
class ProjectMeetingAdmin(admin.ModelAdmin):
    """
    Django admin UI interface for ProjectMeeting model
    """
    list_display = ('title', 'project')
    search_fields = ('title',)
    ordering = ('updated_at',)


@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    """
    Django admin UI interface for Summary model
    """
    list_display = ('title', 'project')
    search_fields = ('title',)
    ordering = ('updated_at',)
