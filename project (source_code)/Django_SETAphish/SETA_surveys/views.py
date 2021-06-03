from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .forms import CreationSurveyForm, CreationGroupTrainingForm, CreationCampaignTrainingForm
from .models import Survey, Question, Answer
from .modules.DjangoSETAsurveys import *

from io import TextIOWrapper
from datetime import datetime
import csv


def index2(request):

    ''' Index SETAsurvey
    
    Shows main page for Surveys section of the app. '''

    return render(request, 'SETA_gophish/index2.html')

    
@login_required
def create_survey(request):

    ''' Create survey
    
    Form for survey template creation. '''

    if request.method == 'POST':
        context = {'error_msg': 'ERROR, form not filled in properly'}
        form = CreationSurveyForm(request.POST, request.FILES)
        if form.is_valid():
            survey_name = form.cleaned_data['survey_name']
            file = TextIOWrapper(request.FILES['your_file'].file, encoding=request.encoding)
            args = [survey_name, file]
            questions, answers, answer_key, score_key, msg = create_survey_(args)
            if msg == 'OK':
                context = {'survey_name' : survey_name, 'questions': len(questions)}
                
                # save items
                try:
                    survey = Survey(survey_name=survey_name, answer_key=answer_key, score_key=score_key)
                    survey.save()
                               
                    for i in range(len(questions)):
                        survey=Survey.objects.get(survey_name=survey_name)
                        question=Question(text=questions[i], survey=survey)
                        question.save()                
                        
                        for j in range(len(answers[i])):
                            answer=Answer(text=answers[i][j][1], question=question)
                            if answers[i][j][0]=='T':
                                answer.valid=True
                            answer.save()
                except:
                    context = {'error_msg': 'ERROR while processing survey. Survey name already used?'}
            else:
                context = {'error_msg': msg}
    else:
        form = CreationSurveyForm()
        context = {'form': form}
    return render(request, 'SETA_surveys/create_survey.html', context)


@login_required
def list_surveys(request):
    
    ''' List surveys
    
    List of survey templates. '''

    surveys, msg = list_surveys_()
    if len(surveys)>0:
        context = {'surveys': surveys}
    else:
        context = {'error_msg': msg}
    return render(request, 'SETA_surveys/list_surveys.html', context)
    

@login_required
def get_detail_survey(request, survey_id):

    ''' Get detail survey
    
    Get and print questions and answers for 
    a given survey ID template. '''

    survey, questions, answers, msg = get_detail_survey_(survey_id)
    
    if msg == 'OK':
        context = {'survey':survey, 'questions':questions, 'answers':answers}
    else:
        context = {'error_msg': 'ERROR, survey ID not found in database'} 
        
    return render(request, 'SETA_surveys/details_survey.html', context)

    
@login_required
def remove_survey(request, survey_id):
    
    ''' Remove survey
    
    Remove a given survey ID from database 
    (survey, questions and answers). '''
        
    survey, msg = remove_survey_(survey_id)
    
    if msg == 'OK':
        context = {'survey' : survey}
    else:
        context = {'error_msg': msg} 
        
    return render(request, 'SETA_surveys/remove_survey.html', context)
    
    
@login_required
def create_training(request):

    ''' Create training
    
    Show menu for training creation. '''

    return render(request,'SETA_surveys/create_training_menu.html')
    
    
@login_required
def create_group_training(request):
    
    ''' Create group training
    
    Show form for training creation based 
    on a Gophish target group. '''
    
    if request.method == 'POST':
        context = {'error_msg': 'ERROR, form not filled in properly'}
        form = CreationGroupTrainingForm(request.POST)
        if form.is_valid():
            training_name = form.cleaned_data['training_name']
            target_group_name = form.cleaned_data['target_group_name']
            survey_template_name = form.cleaned_data['survey_template_name']
              
            # validate, create training campaign and send emails.
            
            training, msg = create_group_training_(training_name, target_group_name, survey_template_name)
            
            if msg == 'OK':
                context = {'training': training}
            else:
                context = {'error_msg': msg}
    else:
        form = CreationGroupTrainingForm()
        context = {'form': form}
    return render(request, 'SETA_surveys/create_group_training.html', context)
    
    
@login_required
def create_campaign_training(request):

    ''' Create campaign training
    
    Show form for training creation based 
    on a Gophish campaign. '''
    
    if request.method == 'POST':
        context = {'error_msg': 'ERROR, form not filled in properly'}
        form = CreationCampaignTrainingForm(request.POST)
        if form.is_valid():
            training_name = form.cleaned_data['training_name']
            target_campaign_name = form.cleaned_data['target_campaign_name']
            survey_template_name = form.cleaned_data['survey_template_name']
              
            # validate, create training campaign and send emails.
            
            training, msg = create_campaign_training_(training_name, target_campaign_name, survey_template_name)
            
            if msg == 'OK':
                context = {'training': training}
            else:
                context = {'error_msg': msg}
    else:
        form = CreationCampaignTrainingForm()
        context = {'form': form}
    return render(request, 'SETA_surveys/create_campaign_training.html', context)


def make_survey(request, the_slug):

    ''' Make survey
    
    Show form for filling in the training survey
    for a particular user. '''

    item, survey_id, msg = find_training_(the_slug)
    
    if msg == 'OK':
        survey, questions, answers, msg = get_detail_survey_(survey_id)

        if msg == 'OK' and request.method == 'POST':
            score = store_results_(request.POST, item, survey, questions, answers)
            context = {'score':int(score), 'questions':questions, 'answers':answers}
        
        else:   #not POST
            if msg == 'OK':
                context = {'survey':survey, 'questions':questions, 'answers':answers, 'slug':the_slug}
            else:
                context = {'error_msg': 'ERROR, survey ID not found in database'} 
        
    else:   #error retrieving slug info
        error_msg = msg
        context = {'error_msg': error_msg} 
    
    return render(request, 'SETA_surveys/make_survey.html', context)

    
@login_required
def list_trainings(request):

    ''' List trainings
    
    Show ongoing trainings and statistics. '''
    
    trainings, T_scores, A_scores, msg = list_trainings_()
    if len(trainings)>0:
        training_set = zip(trainings, T_scores, A_scores)
        context = {'training_set': training_set}
    else:
        context = {'error_msg': msg}
    return render(request, 'SETA_surveys/list_trainings.html', context)
    
    
@login_required
def end_training(request, training_id):
    
    ''' End training
    
    Finish a given training by training ID. '''
    
    training, msg = end_training_(training_id)
    if msg=='OK':
        context = {'training': training}
    else:
        context = {'error_msg': msg}
    return render(request, 'SETA_surveys/end_training.html', context)
    

@login_required
def remove_training(request, training_id):

    ''' Remove training
    
    Remove a given training ID from database 
    (training, training items). '''
    
    name, msg = remove_training_(training_id)
    if msg=='OK':
        context = {'training': name}
    else:
        context = {'error_msg': msg}
    return render(request, 'SETA_surveys/remove_training.html', context)
    
    
@login_required
def get_detail_training(request, training_id):

    ''' Get detail training
    
    Get and print training main stats and users stats. 
    Allow user stats download '''
    
    training, users, msg = get_detail_training_(training_id)
    if msg=='OK':
        context = {'training': training, 'users' : users}
    else:
        context = {'error_msg': msg}
    return render(request, 'SETA_surveys/details_training.html', context)
    
    
@login_required
def download_training_stats(request, training_id):

    ''' Download training stats
    
    Download training user statistics. '''

    try:
        training, users, msg = get_detail_training_(training_id)
        if msg != 'OK':
            raise Http404('File download not available')
    except:
        raise Http404('File download not available')
    
    now = datetime.now().strftime("%d%m%Y_%H%M%S")
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = ('attachment; filename="Training_{}_stats_{}.csv"'.format(training.training_name, now))

    writer = csv.writer(response)
    writer.writerow(['Training ID', 'Training Name', 'Survey_template_name', 'Created date', \
        'First Name', 'Last name', 'Email', 'Slug', 'Position', 'Phishing Status', 'Survey results', 'Score'])
    
    for user in users:
        writer.writerow([training.id, training.training_name, training.survey_template_name, training.date, \
            user.first_name, user.last_name, user.email, user.slug,  \
            user.position, user.phishing_status, user.survey_results, user.score])            
            
    return response
