from django import forms
from .modules.DjangoSETAmodules import list_groups_, list_email_templates_, list_landing_page_templates_, list_sending_profile_templates_

class CreationGroupForm(forms.Form):

    ''' User group creation form '''

    group_name = forms.CharField(max_length=50)
    your_file = forms.FileField()
    
class CreationTemplateForm(forms.Form):

    ''' Email template creation form '''
    
    template_name = forms.CharField(max_length=50)
    email_subject = forms.CharField(max_length=50)
    your_file = forms.FileField()
    
class CreationLandingPageForm(forms.Form):
    
    ''' Landing page template creation form '''
    
    OPTION_0 = '0'
    OPTION_1 = '1'
    OPTION_2 = '2'
    OPTIONS = (
        (OPTION_0, u"No credentials captured"),
        (OPTION_1, u"Capture user"),
        (OPTION_2, u"Capture user and password")
    )
    
    template_name = forms.CharField(max_length=50)
    capturing_credentials = forms.ChoiceField(choices=OPTIONS)
    your_file = forms.FileField()
    redirect_url = forms.CharField(max_length=50)
    
class CreationSMTPProfileForm(forms.Form):

    ''' SMTP sending profile creation form '''

    OPTION_0 = '1'
    OPTION_1 = '0'
    OPTIONS = (
        (OPTION_0, u"YES (default)"),
        (OPTION_1, u"NO")
    )

    profile_name = forms.CharField(max_length=50)
    smtp_host = forms.CharField(max_length=50)
    smtp_username = forms.CharField(max_length=50)
    smtp_pass = forms.CharField(max_length=50)
    from_username = forms.CharField(max_length=50)
    from_email_address = forms.CharField(max_length=50)
    ignore_errs = forms.ChoiceField(choices=OPTIONS)
    
class CreationCampaignForm(forms.Form):

    ''' Campaign creation form '''
    
    campaign_name = forms.CharField(max_length=50)
    target_group_name = forms.ChoiceField(choices=())
    email_template_name = forms.ChoiceField(choices=())
    landing_page_name = forms.ChoiceField(choices=())
    smtp_profile_name = forms.ChoiceField(choices=())
    phishing_url = forms.CharField(max_length=50)
    launch_date = forms.CharField(required=False, max_length=16)    #format: dd/mm/yyyy@hh:mm (16 chars)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        items, msg = list_groups_()
        choices = []
        for item in items:
            choices.append([item.name, item.name])
        self.fields['target_group_name'].choices = choices
        
        items, msg = list_email_templates_()
        choices = []
        for item in items:
            choices.append([item.name, item.name])
        self.fields['email_template_name'].choices = choices
        
        items, msg = list_landing_page_templates_()
        choices = []
        for item in items:
            choices.append([item.name, item.name])
        self.fields['landing_page_name'].choices = choices
        
        items, msg = list_sending_profile_templates_()
        choices = []
        for item in items:
            choices.append([item.name, item.name])
        self.fields['smtp_profile_name'].choices = choices
