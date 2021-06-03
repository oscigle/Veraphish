from django.contrib import admin
from .models import Survey, Question, Answer, TrainingCampaign, TrainingCampaign, TrainingItem


class SurveyAdmin(admin.ModelAdmin):
    fields = ['survey_name', 'answer_key', 'score_key', 'date']
    readonly_fields = ('date',)
    
class QuestionAdmin(admin.ModelAdmin):
    fields = ['survey', 'text']

class AnswerAdmin(admin.ModelAdmin):
    fields = ['question', 'text', 'valid']
    
class TrainingCampaignAdmin(admin.ModelAdmin):
    fields = ['training_name', 'target_group_name', 'survey_template_name', 'status', 'date' ]
    readonly_fields = ('date',)

class TrainingItemsAdmin(admin.ModelAdmin):
    fields = ['trainingcampaign', 'slug', 'first_name', 'last_name', 'email', 'position', 'phishing_status', 'survey_results', 'score']
    
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(TrainingCampaign, TrainingCampaignAdmin)
admin.site.register(TrainingItem, TrainingItemsAdmin)
