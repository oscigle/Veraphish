#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser
import os
import random
from string import ascii_letters, digits
from itertools import chain

import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from gophish import Gophish
from SETA_surveys.models import Survey, Question, Answer, TrainingCampaign, TrainingItem


def get_random_string(length):

    ''' Create random string
    
    Get a random slug as URI for every single training surveys
    
    Input: lenght (int)
    Output: string '''

    punctuation_symbols = '-_'
    string_characters = ascii_letters + digits + punctuation_symbols
    url_string = ''.join(random.choice(string_characters) for i in range(length))
    return(url_string)


def initialize_connector():

    ''' Gophish API connector
    
    Get SETAphish.cfg file and read parameters. Check file in /config 
    for details and examples. '''
    
    global api
    config = configparser.ConfigParser()
    thisfolder = os.path.dirname(os.path.abspath(__file__))
    cfgfile = os.path.join(thisfolder, 'config', 'SETAsurvey.cfg')
    
    try:
        config.read(cfgfile)
    except Exception as e:
        return('ERROR: Config file not found')
    
    api_key = config.get('MAIN','api_key')
    host_url = config.get('MAIN','host_url')
    verify = config.get('MAIN','verify')
    api = Gophish(api_key, host_url, verify=eval(verify))

    return
    
    
def list_groups_():
    
    ''' List Gophish user groups
    
    Get target groups and high level details
    
    Input: none
    Return: list of Groups if applies or None, 
    and message indicating OK or specific error (string). '''
    
    msg = initialize_connector()
    if msg is not None:
        return(None, msg)
    
    try:
        groups = api.groups.get()
        return(groups, 'OK')
    
    except:
        return(None, 'ERROR: failed to retrieve target groups')
        
        
def list_campaigns_():

    ''' Gophish list phishing campaigns
    
    List existing phishing campaigns 

    Input: None
    Return: list of phishing campaign objects or None, 
    and message indicating OK or specific error (string). '''
    
    msg = initialize_connector()
    if msg is not None:
        return(None, msg)
    
    try:
        campaigns = api.campaigns.summary()
        return(campaigns, 'OK')
        
    except:
        return(None, 'ERROR:  failed to retrieve phishing campaigns\n')
        
        
def get_detail_group_(id):
    
    ''' Get Gophish user group detail
    
    Retrieve group details 
    
    Input: GroupId in Gophish database
    Return: object reference if applies or None, 
    and message indicating OK or specific error (string). '''
    
    msg = initialize_connector()
    if msg is not None:
        return(None, msg)
    
    try:
        group = api.groups.get(group_id=id)
        return(group, 'OK')
       
    except:
        return(None, 'Error:  failed to retrieve target group {}. Generic error or non existent'.format(id))


def get_campaign_details_(id):

    ''' Get Gophish phishing campaign details
    
    Retrieve phishing campaign properties
    
    Input: Campaign Id in Gophish database
    Return: object reference if applies (summary and details) or None, None, 
    and message indicating OK or specific error (string). '''
    
    msg = initialize_connector()
    if msg is not None:
        return(None, None, msg)
    
    try:
        summary = api.campaigns.summary(campaign_id=id)
        details = api.campaigns.get(campaign_id=id)
        return(summary, details, 'OK')
            
    except:
        return(None, None, 'ERROR: failed to retrieve phishing campaign details or ID non-existent\n')


def create_keys(scoring_list):

    ''' Create keys
    
    Create the coded answers key and scoring for the template survey
    
    Answers_key: 1 for true, 0 for false, separated by - within a question and by _ between questions
    Score_key: score for true, 0 for false, separated by - within a question and by _ between questions
    
    '''
    
    answer_key = ''
    score_key = ''
    
    print(scoring_list)
    
    for item in scoring_list:
        
        for score in item:
            if score != 0:
                answer_key=answer_key+'1'+'-'
            else:
                answer_key=answer_key+'0'+'-'
            score_key=score_key+str(score)+'-'
        answer_key = answer_key[:-1]
        score_key = score_key[:-1]
        
        answer_key = answer_key + '_'
        score_key = score_key + '_'
    
    answer_key = answer_key[:-1]
    score_key = score_key[:-1]    
    
    return(answer_key, score_key)
    



def create_survey_scoring(answers):
    
    ''' Create survey scoring
    
    Create a scoring list of lists for the already validated template survey
    '''
    
    scoring_list = []
    
    number_of_questions = len(answers)
    points_per_question = 100 / number_of_questions
    
    for answers_group in answers:
        
        trues_in_question = 0
        for answer in answers_group:
            if 'T' in answer[0]:
                trues_in_question += 1            
    
        scoring_question_list = []
        for answer in answers_group:
            if 'T' in answer[0]:            
                scoring_question_list.append(round(points_per_question / trues_in_question,2))
            else:
                scoring_question_list.append(0.0)
        
        scoring_list.append(scoring_question_list)
    
    return scoring_list


def validate_survey(questions, answers):

    ''' Validate survey template
    
    Create a scoring list of lists for the already validated survey
    
    #checks: 
    #C1: same number of questions than answers´ lists
    #C2: at least two answers items per questions
    #C3: at least one True answer per question
    '''
    
    valid = True
    msg = 'OK'
      
    #C1
    if len(questions) != len(answers):
        msg = ('ERROR: Number of questions {} and set of answers {} does not match for the survey'\
        .format(len(questions),len(answers)))
        valid = False
    
    #C2
    for answers_group in answers:
        if len(answers_group) < 2:
            msg = ('ERROR: Number of answers lower than two for a given survey question')
            valid = False
            break
            
    #C3
    for answers_group in answers:
        one_correct = False
        for answer in answers_group:
            if answer[0] == 'T':
                one_correct = True
                break
        if one_correct == False:
            msg = ('ERROR: There is at least one question with no True answers in the survey')
            valid = False
            
    return(valid, msg)
    

def create_survey_(args):

    ''' Create survey template
    
    Parse CSV training awareness survey file
    
    Input: survey name, file (CSV)
    Returns two lists, questions and answers
    
    Format CSV comma separated: Two fields per line: item and content.
    #Item: Q if question, T if answer true, F if answer false.
    #Content: Question if item Q, possible answer if item was T or F.
    
    '''
    
    name, filename = args
    
    questions = []
    answers = []
    
    try:
        i = -1
        ans_item = []
        valid_format = True
        # with open(filename) as file:
        file = filename.readlines()
        for line in file:
            array = (line.strip().split(','))
            if len(array) != 2:
                valid_format = False
                msg = 'ERROR: Exiting due to missformated file (len)'
                return(None, None, None, None, msg)
                # break
            else:
                item, content = array
                if item == 'Q':
                    i += 1
                    questions.insert(i,content)
                    if len(ans_item) > 0:
                        answers.insert(i-1, ans_item)
                    ans_item = []
                elif item in ['T','F']:
                    ans_item.append([item,content])
                else:
                    valid_format = False
                    msg = ('ERROR: Exiting due to missformated file (item)')
                    return(None, None, None, None, msg)
                    # break
        
        if valid_format and len(ans_item) > 0:
            answers.insert(i, ans_item)
      
        valid, msg = validate_survey(questions, answers)
        if valid:    
            scoring = create_survey_scoring(answers)
        else:
            return(None, None, None, None, msg)
        
        answer_key, score_key = create_keys(scoring)
        
        return(questions, answers, answer_key, score_key, 'OK')
        
    except:
        return(None, None, None, None, 'Unexpected error while processing survey')
        
        
def list_surveys_():

    ''' List Survey templates
    
    Get survey templates and high level details
    
    Input: none
    Return: list of survey templates if applies or None, 
    and message indicating OK or specific error (string). '''

    try:
        all_surveys = Survey.objects.all()
    except:
        msg = 'ERROR: Exiting while retrieving surveys from database or non existent'
        return(None, msg)
    
    if len(all_surveys) > 0:
        msg = 'OK'
    else:
        msg = 'ERROR: There are no survey in database!'
    
    return(all_surveys, msg)


def get_detail_survey_(survey_id):

    ''' Get Survey templates
    
    Get specific template, questions and answers
    
    Input: Survey ID
    Return: survey object, queryset of questions and queryset of answers 
    (or None for the three), and message indicating OK or specific error (string). '''

    msg = 'OK'
    try:
        survey = Survey.objects.get(id=survey_id)
        questions = Question.objects.filter(survey=survey_id)
        
        answers = Answer.objects.none()
        for question in questions:
            partial_answers = Answer.objects.filter(question=question.id)
            answers = list(chain(answers, partial_answers))
        
    except:
        msg = 'ERROR: Exiting while retrieving survey from database or non existent'
        return(None, None, None, msg)
    if len(answers)==0:
        msg = 'ERROR: Exiting while retrieving survey from database or non existent'
        return(None, None, None, msg)
    return(survey, questions, answers, msg)
    

def remove_survey_(survey_id):
    
    ''' Remove survey templates
    
    Remove specific template, survey, questions and answers
    
    Input: survey ID
    Return: survey ID, and message indicating OK or specific error (string). '''    
    
    msg = 'OK'
    try:
        survey = Survey.objects.get(id=survey_id)
        survey.delete()
    except:
        msg = 'ERROR: Exiting while retrieving survey from database or non existent'
    
    return(survey_id, msg)

   
def read_template(filename):
    
    ''' Read email template
    
    Read the email template for sending the URL link for the survey
    
    Input: filename within /modules in the Survey app
    Return: Template object. '''    
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def send_training_emails(email_host, email_template, email_origin, email_subject, email_password, message_template, names, emails, slugs):
    
    ''' Send training emails
    
    Sends all emails with survey link for users to be trained
    
    Inputs (list): email_host, email_template, email_origin, email_subject and email_password, from config file  
    and message_template (constructed), names, emails and slugs from the database for the users included.
    Return: message indicating OK or specific error (string). '''
    
    try:
        # set up the SMTP server
    
        print(email_host, email_template, email_password)
        s = smtplib.SMTP(host=email_host, port=25)
        s.starttls()
        s.login(email_origin, email_password)

        # For each contact, send the email:
        for name, email, slug in zip(names, emails, slugs):
            msg = MIMEMultipart()       # create a message

            # add in the actual person name to the message template
            message = message_template.substitute(PERSON_NAME=name.title(), SURVEY_LINK=slug)

            # setup the parameters of the message
            msg['From']=email_origin
            msg['To']=email
            msg['Subject']=email_subject
            
            # add in the message body
            msg.attach(MIMEText(message, 'plain'))
            
            # send the message via the server set up earlier.
            s.send_message(msg)
            del msg
            
        # Terminate the SMTP session and close the connection
        s.quit()
    except:
        return('ERROR: unexpected error while sending the training emails')
    return('OK')


def create_group_training_(training_name, target_group_id, survey_template_name):

    ''' Create group training
    
    Create a training awareness survey based on a GoPhish target group of users
    
    Inputs (list): training_name, target_group_id, survey_template_name 
    Return: TrainingCampaign object or None, and message indicating 
    OK or specific error (string). '''

    group, msg = get_detail_group_(target_group_id)
    
    if msg == 'OK':
    
        try:
            
            config = configparser.ConfigParser()
            thisfolder = os.path.dirname(os.path.abspath(__file__))
            cfgfile = os.path.join(thisfolder, 'config', 'SETAsurvey.cfg')
            config.read(cfgfile)
            email_filename = config.get('TRAINING', 'email_template')
            email_host = config.get('TRAINING', 'email_host')
            email_origin = config.get('TRAINING', 'email_origin')
            email_password = config.get('TRAINING', 'email_password')
            email_subject = config.get('TRAINING', 'email_subject')
            training_base_url = config.get('TRAINING', 'training_base_url')
            
        except Exception as e:
            return(None, 'ERROR: Config file not found or parameter non existent')
        
        try: 
            training = TrainingCampaign()
            training.training_name = training_name
            training.target_group_name = group.name
            training.number_of_users = len(group.targets)
            training.survey_template_name = survey_template_name
            training.status = 'ACTIVE'
            training.source = 'GROUP'
            training.save()
            
            names = []
            emails = []
            slugs = []
            
            for user in group.targets:
                item = TrainingItem()
                item.trainingcampaign = training
                item.slug = get_random_string(50)
                item.first_name = user.first_name
                item.last_name = user.last_name
                item.email = user.email
                item.position = user.position
                item.save()
        
                names.append(item.first_name)
                emails.append(item.email)
                slugs.append(training_base_url + item.slug)
                
            thisfolder = os.path.dirname(os.path.abspath(__file__))
            
            email_template = os.path.join(thisfolder, email_filename)
            message_template = read_template(email_template)
            
            msg = send_training_emails(email_host, email_template, email_origin, email_subject, \
            email_password, message_template, names, emails, slugs)
            
            
        
        except:
                return(None, 'ERROR: unexpected error while saving the training campaign or campaign name duplicated!')
        
    return(training, msg)
            

def create_campaign_training_(training_name, target_campaign_id, survey_template_name):

    ''' Create campaign training
    
    Create a training awareness survey based on a GoPhish phishing campaign
    
    Inputs (list): training_name, target_campaign_id, survey_template_name 
    Return: TrainingCampaign object or None, and message indicating 
    OK or specific error (string). '''


    summary, details, msg = get_campaign_details_(target_campaign_id)
    
    if msg == 'OK':
        
        try:
            
            config = configparser.ConfigParser()
            thisfolder = os.path.dirname(os.path.abspath(__file__))
            cfgfile = os.path.join(thisfolder, 'config', 'SETAsurvey.cfg')
            config.read(cfgfile)
            email_filename = config.get('TRAINING', 'email_template')
            email_host = config.get('TRAINING', 'email_host')
            email_origin = config.get('TRAINING', 'email_origin')
            email_password = config.get('TRAINING', 'email_password')
            email_subject = config.get('TRAINING', 'email_subject')
            training_base_url = config.get('TRAINING', 'training_base_url')
            
            if msg != 'OK':
                return(None, 'ERROR: unexpected error while saving the training campaign or campaign name duplicated!')

        except Exception as e:
            return(None, 'ERROR: Config file not found or parameter non existent')
        
        
        
        try: 
            training = TrainingCampaign()
            training.training_name = training_name
            training.target_group_name = summary.name
            training.number_of_users = len(details.results)
            training.survey_template_name = survey_template_name
            training.status = 'ACTIVE'
            training.source = 'CAMPAIGN'
            training.save()
            
            names = []
            emails = []
            slugs = []
            
            for result in details.results:
                item = TrainingItem()
                item.trainingcampaign = training
                item.slug = get_random_string(50)
                item.first_name = result.first_name
                item.last_name = result.last_name
                item.email = result.email
                item.position = result.position
                item.phishing_status = result.status.upper()
                item.save()
                
                names.append(item.first_name)
                emails.append(item.email)
                slugs.append(training_base_url + item.slug)
        
            thisfolder = os.path.dirname(os.path.abspath(__file__))
            
            email_template = os.path.join(thisfolder, email_filename)
            message_template = read_template(email_template)
            
            msg = send_training_emails(email_host, email_template, email_origin, email_subject, \
            email_password, message_template, names, emails, slugs)
            
            if msg != 'OK':
                return(None, 'ERROR: unexpected error while saving the training campaign or campaign name duplicated!')
            
        except:
            return(None, 'ERROR: unexpected error while saving the training campaign or campaign name duplicated!')
        
    return(training, msg)
            

def list_trainings_():

    ''' List trainings
    
    List existing training surveys 

    Input: None
    Return: list of T-scores, list of A-scores and message indicating OK or specific error (string). '''
    
    try:
        all_trainings = TrainingCampaign.objects.all()
    except:
        msg = 'ERROR: Exiting while retrieving training campaigns from database or non existent'
        return(None, msg)
    
    if len(all_trainings) > 0:
        msg = 'OK'    
        T_scores, A_scores = calculate_main_scores_(all_trainings)

    else:
        msg = 'ERROR: There are no training campaigns in database!'
    
    return(all_trainings, T_scores, A_scores, msg)


def calculate_main_scores_(all_trainings):

    ''' Calculate training scores
    
    # Calculate Training score and Awareness score for all campaigns in database
    
    Input: Queryset of TrainingCampaigns
    Return: list of T-scores, list of A-scores. '''
    
    rate_answers, pass_training = get_thresholds_()

    T_scores = []
    A_scores = []

    for campaign in all_trainings:
        training, users, msg = get_detail_training_(campaign.id)
        if training is None:
            T_scores.append('ERROR')
            A_scores.append('ERROR')
        else:
            user_cont = 0
            user_unanswered = 0
            t_score = 0
            a_score = 0
            
            cont_training_passed = 0
            cont_phished = 0
            rate_training_passed = 0
            rate_phished = 0
            
            
            for user in users:
                if user.score != 'NA':
                    user_cont += 1
                    t_score = t_score + float(user.score)
                else:
                    user_unanswered += 1
                    
            if user_cont != 0:
                if int(100*(user_cont/len(users))) >= int(rate_answers):
                    t_score = t_score / user_cont
                else:
                    t_score = 'In Progress'
                    a_score = 'In Progress'
            else:
                t_score = 'In Progress'
                a_score = 'In Progress'
            
            if training.source == 'GROUP':
                a_score = 'NA'
            
            if a_score not in ['NA', 'In Progress']:             
                for user in users:
                    if user.score != 'NA':
                        if int(float(user.score)) >= int(pass_training):
                            cont_training_passed += 1

                    if user.phishing_status in ['CLICKED LINK', 'SUBMITTED DATA']:
                        cont_phished += 1

                rate_training_passed = float(100*(cont_training_passed / (len(users)-user_unanswered)))
                rate_phished = float(100*(cont_phished / len(users)))
                
                a_score = rate_training_passed - rate_phished
            
            T_scores.append(str(t_score))
            A_scores.append(str(a_score))

    return(T_scores, A_scores)
    
    
def get_thresholds_():

    ''' Get thresholds
    
    Retrieve params from config file for calculating training scores
    
    Input: None
    Return: rate_answers (0-100), pass_training (0-100). '''
    
    global api
    config = configparser.ConfigParser()
    thisfolder = os.path.dirname(os.path.abspath(__file__))
    cfgfile = os.path.join(thisfolder, 'config', 'SETAsurvey.cfg')
    
    try:
        config.read(cfgfile)
    except Exception as e:
        return(None, None, 'ERROR: Config file not found')
    
    rate_answers = config.get('TRAINING','rate_answers')    # minimum % of answers to show results
    pass_training = config.get('TRAINING','pass_training')  # passing grade for A-score (% training passing - % phished)
    
    return(rate_answers, pass_training)


def end_training_(id):

    ''' End training
    
    Complete training campaign

    Input: Training ID
    Return: TrainingCampaign object, and message indicating OK or specific error (string). '''
    
    msg = 'OK'
    
    try:
        training = TrainingCampaign.objects.get(pk=id)
    except:
        msg = 'ERROR: Exiting while retrieving training campaign from database or non existent'
        return(None, msg)

    if training:
        try:
            training.status='COMPLETED'
            training.save()
        except:
            msg = 'ERROR: Exiting while updating training campaign in database or non existent'
            return(None, msg)
    else:
        msg = 'ERROR: There are no trainingc campaigns in database!'
    
    return(training, msg)
    
    
def remove_training_(id):

    ''' Remove training
    
    Remove training campaign

    Input: Training ID
    Return: TrainingName, and message indicating OK or specific error (string). '''
    
    msg = 'OK'
    
    try:
        training = TrainingCampaign.objects.get(pk=id)
        name = training.training_name
        training.delete()
    except:
        msg = 'ERROR: Exiting while retrieving training campaign from database or non existent'
        return(None, msg)

    return(name, msg)
    
    
def get_detail_training_(training_id):

    ''' Get detail training
        
    Get details of a given training (Training as such and user training status)
    
    Input: Training ID
    Return: Trainingcampaign object, TrainingItem Queryset, 
    and message indicating OK or specific error (string). '''

    try:
        training = TrainingCampaign.objects.get(id=training_id)
        users = TrainingItem.objects.filter(trainingcampaign=training_id)
        
    except:
        msg = 'ERROR: Exiting while retrieving training details from database or non existent'
        return(None, None, msg)
            
    if users:
        msg = 'OK'
    else:
        msg = 'ERROR: There are no training campaigns in database!'
        return(None, None, msg)
    
    return(training, users, msg)
    
    
def find_training_(slug):

    ''' Find training
    
    Gets the right survey from database using the slug link
    
    Input: Slug (string)
    Return: TrainingItem object, survey.id (or None both), 
    and message indicating OK or specific error (string). '''

    try:
        item = TrainingItem.objects.get(slug=slug)
        survey_template_name = item.trainingcampaign.survey_template_name
        survey = Survey.objects.get(survey_name = survey_template_name)
        
        if item.trainingcampaign.status == 'COMPLETED':
            return(None, None, 'ERROR: training campaign already closed!')
        if item.survey_results != 'NA':
            return(None, None, 'ERROR: training link already consumed!')
            
    except:
        return(None, None, 'ERROR: training campaign not found in database for this slug!')
        
    return(item, survey.id, 'OK')
    

# =============================================================================
# calculate score and errors for a survey answered
# =============================================================================

def calculate_score_and_errors_(user_answers, answer_key_converted, score_key_converted):

    ''' Calculate score and errors 
    
    Calculate stats for a single answered survey

    Errors will have '1' where answer differs from answer key, 
    '0' otherwise
    Score will add points if valid answer detected. 
    False errors will not penalize.

    Input: User answers, answers_key_converted, 
    score_key_converted (strings)
    Return: errors (string with 0's and 1's), score (0-100). '''

    errors = ''
    score = 0
    
    for i in range(len(user_answers)):
        if user_answers[i] == answer_key_converted[i]:
            errors = errors + '0'
            if float(score_key_converted[i]) != 0:
                score = score + float(score_key_converted[i])
        else:
            errors = errors + '1'
    
    return(errors, score)  
    

def store_results_(post_dict, item, survey, questions, answers):
    
    ''' Store results 
    
    Save results for a single survey answered

    Store answers and survey score for a given slug survey. 
    
    Input: POST dict of the answered form,
    Item Object, Survey object, questions QuerySet, Answers QuerySet
    
    Input: User answers, answers_key_converted, 
    Return: score (0-100). '''
    
    user_answers = ''
    for i in range(len(answers)):
        if 'answer'+str(i) in post_dict:
            user_answers = user_answers+'1-'
        else:
            user_answers = user_answers+'0-'
    user_answers = user_answers[:-1]
    
    item.survey_results = user_answers
    
    score = ''
    user_answers = user_answers.split('-')
    answer_key_converted = survey.answer_key.replace('_','-').split('-')
    score_key_converted = survey.score_key.replace('_','-').split('-')
    
    errors, score = calculate_score_and_errors_(user_answers, answer_key_converted, score_key_converted)
    
    item.score = score
    item.save() #answers saved
    return(score)
