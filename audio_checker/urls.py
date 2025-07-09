from django.urls import path
from . import views

app_name = 'audio_checker'

urlpatterns = [
    path('', views.home, name='home'),
    path('analysis/<int:analysis_id>/', views.analysis_detail, name='analysis_detail'),
    path('analysis/<int:analysis_id>/status/', views.check_analysis_status, name='check_analysis_status'),
    path('analysis/<int:analysis_id>/download/', views.download_results, name='download_results'),
    path('analysis/<int:analysis_id>/download-transcript/', views.download_transcript_docx, name='download_transcript_docx'),
    path('list/', views.analysis_list, name='analysis_list'),
] 