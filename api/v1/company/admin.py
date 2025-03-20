from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """
    Django admin UI interface for Company model
    """
    list_display = ('id', 'name', 'status')
    search_fields = ('name',)
    ordering = ('created_at',)


@admin.register(CompanyUser)
class CompanyUserAdmin(admin.ModelAdmin):
    """
    Django admin UI interface for CompanyUser model
    """
    list_display = ('user', 'company')
    search_fields = ('user__first_name', 'user__last_name',
                     'user__email', 'company__name')
    ordering = ('created_at',)


@admin.register(CompanyRole)
class CompanyRoleAdmin(admin.ModelAdmin):
    """
    Django admin UI interface for CompanyRole model
    """
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('created_at',)


@admin.register(CompanyMonthlyUsage)
class CompanyMonthlyUsageAdmin(admin.ModelAdmin):
    """
    Django admin UI interface for Company's monthly usage
    """
    list_display = (
        'company', 'month', 'year',
        'transcription_duration', 'summaries_count'
    )
    search_fields = ('company', 'month', 'year')
    ordering = ('-year', '-month')
