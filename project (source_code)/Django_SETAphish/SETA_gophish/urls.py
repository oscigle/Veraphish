from django.urls import include, path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name='index'),
    
    path('groups/create_group', views.create_group, name='create_group'),
    path('groups/list', views.list_groups, name='list_groups'),
    path('groups/details/<int:group_id>/', views.get_detail_group, name='get_detail_group'),
    path('groups/remove/<int:group_id>', views.remove_group, name='remove_group'),
    
    path('templates/create_template', views.create_email_template, name='create_template'),
    path('templates/list', views.list_templates, name='list_templates'),
    path('templates/details/<int:template_id>/', views.get_detail_template, name='get_detail_template'),
    path('templates/remove/<int:template_id>', views.remove_template, name='remove_template'),
    
    path('landings/create_landing_page', views.create_landing_page, name='create_landing_page'),
    path('landings/list', views.list_landing_pages, name='list_landing_pages'),
    path('landings/details/<int:landing_page_id>/', views.get_detail_landing_page, name='get_detail_landing_page'),
    path('landings/remove/<int:landing_page_id>', views.remove_landing_page, name='remove_landing_page'),
    
    path('profiles/create_profile', views.create_profile, name='create_profile'),
    path('profiles/list', views.list_profiles, name='list_profiles'),
    path('profiles/details/<int:profile_id>/', views.get_detail_profile, name='get_detail_profile'),
    path('profiles/remove/<int:profile_id>', views.remove_profile, name='remove_profile'),
    
    path('campaigns/create_campaign', views.create_campaign, name='create_campaign'),
    path('campaigns/list', views.list_campaigns, name='list_campaigns'),
    path('campaigns/details/<int:campaign_id>/', views.get_detail_campaign, name='get_detail_campaign'),
    path('campaigns/finish/<int:campaign_id>', views.end_campaign, name='end_campaign'),
    path('campaigns/remove/<int:campaign_id>', views.remove_campaign, name='remove_campaign'),
    path('campaigns/download_stats/<int:campaign_id>', views.download_campaign_stats, name='download_campaign_stats'),
    path('campaigns/download_users/<int:campaign_id>', views.download_campaign_users, name='download_campaign_users'),
    
    path('license', views.show_license, name='show_license'),
    path('contact', views.show_contact, name='show_contact'),
    path('about', views.show_about, name='show_about'),
    path('help', views.show_help, name='show_help')
    
]
