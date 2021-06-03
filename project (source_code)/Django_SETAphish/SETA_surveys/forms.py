from django import forms
from .modules.DjangoSETAsurveys import list_groups_, list_surveys_, list_campaigns_

class CreationSurveyForm(forms.Form):

    ''' Survey form
    
    Form for the main object for representing 
    the survey training template
    
    Survey name: self-explanatory
    Your file: CSV with questions and answers
    '''

    survey_name = forms.CharField(max_length=50)
    your_file = forms.FileField()
    

class CreationGroupTrainingForm(forms.Form):

    ''' Group training form
    
    Form for the training campaign based on a GoPhish 
    users target group
    
    Training name: self-explanatory
    Target group name: the identifier in GoPhish database for the group
    Survey template name: choice field with already 
    existing survey templates
    '''

    training_name = forms.CharField(max_length=50)
    target_group_name = forms.ChoiceField(choices=())
    survey_template_name = forms.ChoiceField(choices=())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        items, msg = list_groups_()
        choices = []
        for item in items:
            choices.append([item.id, item.name])
        self.fields['target_group_name'].choices = choices
        
        surveys, msg = list_surveys_()
        choices = []
        for item in surveys:
            choices.append([item.survey_name, item.survey_name])
        self.fields['survey_template_name'].choices = choices
        

class CreationCampaignTrainingForm(forms.Form):

    ''' Campaign training form
    
    Form for the training campaign based on a GoPhish 
    phishing campaign
    
    Training name: self-explanatory
    Target campaign name: the identifier in GoPhish database 
    for the phishing campaign
    Survey template name: choice field with already 
    existing survey templates
    '''

    training_name = forms.CharField(max_length=50)
    target_campaign_name = forms.ChoiceField(choices=())
    survey_template_name = forms.ChoiceField(choices=())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        campaigns, msg = list_campaigns_()
        choices = []
        for item in campaigns.campaigns:
            choices.append([item.id, item.name])
        self.fields['target_campaign_name'].choices = choices
        
        surveys, msg = list_surveys_()
        choices = []
        for item in surveys:
            choices.append([item.survey_name, item.survey_name])
        self.fields['survey_template_name'].choices = choices
