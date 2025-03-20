from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CompanyView.as_view(), name="company_view"),
    path(
        'usage/', views.CompanyMonthlyUsageView.as_view(),
        name="company_usage_view"
    )
]
