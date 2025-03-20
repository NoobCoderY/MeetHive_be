from django.urls import path, include

urlpatterns = [
    path('v1/user/', include('api.v1.user.urls')),
    path('v1/company/', include('api.v1.company.urls')),
    path('v1/project/', include('api.v1.project.urls')),
]
