from django.urls import path
from . import views

app_name = 'SETA_surveys'

urlpatterns = [
    path('', views.index2, name='index2'),
    
    path('surveys/survey/create_survey', views.create_survey, name='create_survey'),
    path('surveys/survey/list', views.list_surveys, name='list_surveys'),
    path('surveys/survey/details/<int:survey_id>/', views.get_detail_survey, name='get_detail_survey'),
    path('surveys/survey/remove/<int:survey_id>', views.remove_survey, name='remove_survey'),
    
    path('surveys/training/create_training', views.create_training, name='create_training'),
    path('surveys/training/create_group_training', views.create_group_training, name='create_group_training'),
    path('surveys/training/create_campaign_training', views.create_campaign_training, name='create_campaign_training'),
    path('surveys/training/list', views.list_trainings, name='list_trainings'),
    path('surveys/training/finish/<int:training_id>', views.end_training, name='end_training'),
    path('surveys/training/remove/<int:training_id>', views.remove_training, name='remove_training'),
    path('surveys/training/details/<int:training_id>/', views.get_detail_training, name='get_detail_training'),
    path('surveys/training/download_stats/<int:training_id>', views.download_training_stats, name='download_training_stats'),
    
    path('surveys/training/make_survey/<slug:the_slug>', views.make_survey, name='make_survey'),
]
