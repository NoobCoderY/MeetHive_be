from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectView.as_view(), name="project_view"),
    path('get/<str:pk>/', views.ProjectIDView.as_view(),
         name="get_project_view"),

    path(
        'transcription/', views.TranscriptionView.as_view(),
        name="transcription_view"
    ),
    path('summary/', views.SummaryView.as_view(), name='summary_view'),
    path(
        'transcription/<str:pk>/', views.TranscriptionIDView.as_view(),
        name="transcription_id_view"
    ),
    path('transcription/upload',views.UploadTranscriptionView.as_view(), name='upload_transcription_view'),
    path('transcription/signed-url',views.GenerateSignedUrlView.as_view(), name='generate_signed_url'),
    path('summary/<str:pk>/', views.SummaryIdView.as_view(), name='summary_id_view'),
    path('search/', views.SearchView.as_view(), name='search_view')
]
