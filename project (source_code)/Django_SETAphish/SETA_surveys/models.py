from django.db import models


class Survey(models.Model):

    ''' Survey model
    
    Main object for representing the survey training template
    
    Survey name: self-explanatory
    Answer key: coded string with answers 
    true (1) or false (0) for the survey template 
    Score key: same as above but for the scoring
    Date: creation date
    
    '''

    survey_name = models.CharField(max_length=50, unique=True)
    answer_key = models.CharField(max_length=250)
    score_key = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)
    
class Question(models.Model):

    ''' Question model
    
    One component linked to Survey model. Many to one relation.
    
    Survey: foreign key
    Text: question sentence
    
    '''

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    
class Answer(models.Model):
    
    ''' Answer model
    
    One component linked to Survey model and Question model. 
    Many to one relation with the latter.
    
    Question: foreign key
    Text: answer sentence
    Valid: answer is True or False
    
    '''
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    valid = models.BooleanField(default=False)
    
class TrainingCampaign(models.Model):
    
    ''' Training campaign
    
    Main object for representing the survey training campaigns
    
    Training name: self-explanatory
    Target group name: Name of group or campaign in GoPhish
    Number of users: number of items in above
    Survey template name: survey template used 
    for this particular campaign
    Date: creation date
    Status: ACTIVE or COMPLETED
    Source: CAMPAIGN or GROUP (related to Target group name)
    
    '''
    
    STATUS_CHOICES = ( 
    ("ACTIVE", "ACTIVE"), 
    ("COMPLETED", "COMPLETED"), 
    )    
    
    TRAINING_CHOICES = ( 
    ("CAMPAIGN", "CAMPAIGN"), 
    ("GROUP", "GROUP"), 
    )

    training_name = models.CharField(max_length=50, unique=True)
    target_group_name = models.CharField(max_length=50)     #group_name or campaign_name
    number_of_users = models.IntegerField(blank=True)
    survey_template_name = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=9) #status_choices
    source = models.CharField(max_length=8) #training_choices

class TrainingItem(models.Model):

    ''' Training Item
    
    Main object for representing the survey training 
    user interaction in a given campaign. Many to one relation 
    with TrainingCampaign
    
    Training campaign: foreign key
    Slug: random string to add to base url for survey
    First name: User name
    Last name: User name
    Email: User email 
    Position: User position in the company
    Phishing status: Default NA, or phishing status in the campaign 
    source of the users to train
    Survey results: Answer key for the user in the survey
    Score: points obtained in the survey (0-100)
    
    '''
    

    trainingcampaign = models.ForeignKey(TrainingCampaign, on_delete=models.CASCADE)
    slug = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    phishing_status = models.CharField(max_length=50, default='NA') #Options: Campaign created, Email Sent, Email opened, Clicked Link, Submitted Data
    survey_results = models.CharField(max_length=50, default='NA')  #answer_key format
    score = models.CharField(max_length=50, default='NA')           #0-100
