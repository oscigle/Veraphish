#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Custom auxiliar modules for SETA_gophish app

import sys
import csv
import configparser
import time
import os
from datetime import datetime
from gophish import Gophish
from gophish.models import (Campaign, Group, Page, SMTP, Template, User)


def initialize_connector():

    ''' Gophish API connector
    
    Get SETAphish.cfg file and read parameters. Check file in /config 
    for details and examples. '''
    
    global api
    config = configparser.ConfigParser()
    thisfolder = os.path.dirname(os.path.abspath(__file__))
    cfgfile = os.path.join(thisfolder, 'config', 'SETAphish.cfg')
    
    try:
        config.read(cfgfile)
    except Exception as e:
        return('ERROR: Config file not found')
    
    api_key = config.get('MAIN','api_key')
    host_url = config.get('MAIN','host_url')
    verify = config.get('MAIN','verify')
    api = Gophish(api_key, host_url, verify=eval(verify))

    return


def create_group_(args):

    ''' Pishing group of users creation
    
    Create a new group of users to be phished or trained
    input file format: CSV delimited by comma, no headers, 
    one line per user, four fields (First Name, Last Name, 
    Email, Position)
    
    Input: list with Group name, CSV File 
    Return: object reference (Gophish Group) if applies or None, 
    and message indicating OK or specific error (string). '''

    msg = initialize_connector()
    if msg is not None:
        return(None, msg)
    
    name, file = args
    users = []
    fields = ['First Name', 'Last Name', 'Email', 'Position']
    
    try:
        reader = csv.DictReader(file, fields)
        for row in reader:
            if row:
                users.append(create_user(row))                
        group = Group(name=name, targets=users)

    except(FileNotFoundError):
        msg = ('ERROR: no such file: {}'.format(filename))
        return(None, msg)
        
    try:
        group = api.groups.post(group)
        return(group, 'OK')
        
    except:
        return(None, 'ERROR: failed to create target group (possible duplicate or file format is wrong)')


def create_user(row):

    ''' Gophish User creation
    
    Convert list item into gophish user type.
    
    Input: CSV line
    Return: reference to new gophish User object. '''

    return (User(first_name=row['First Name'], last_name=row['Last Name'],
                 email=row['Email'], position=row['Position']))
    

def list_groups_():
    
    ''' List Gophish user groups
    
    Print target groups and high level details
    
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
        
        
def remove_group_(id):

    ''' Remove Gophish user group detail
     
    Input: GroupId in Gophish database
    Return: message indicating OK or specific error (string). '''
    
    msg = initialize_connector()
    if msg is not None:
        return(msg)
    
    try:
        group = api.groups.delete(group_id=id)
        return('OK')
        
    except:
        return('ERROR:  failed to remove the target group {}. Generic error or non existent'.format(id))		


def create_email_template_(args):
    
    ''' Gophish email template creation 
    
    Create a new template email for phishing campaigns

    Input: list with template name (string), email subject (string), file template (html)
    Return: reference to template objectif applies or None, 
    and message indicating OK or specific error (string). '''
    
    msg = initialize_connector()
    if msg is not None:
        return(None, msg)
    
    template_name, email_subject, file = args
    
    try:
        html = file.read()        
        template = Template(name=template_name, subject=email_subject, html=html)

    except(FileNotFoundError):
        return(None, 'ERROR: no such file {}'.format(filename))

    try:
        template = api.templates.post(template)
    except:
        #possible source code bug
        return(None, 'ERROR: failed to create email template (possible duplicate)\n')

    return(template, 'OK')
    

def list_email_templates_():

    ''' Gophish list email templates 
    
    List email templates for phishing campaigns

    Input: None
    Return: list of Email template objects or None, 
    and message indicating OK or specific error (string). '''

    msg = initialize_connector()
    if msg is not None:
        return(None, msg)
    
    try:
        templates = api.templates.get()
        return(templates,'OK')
    
    except:
        return(None, 'ERROR: failed to retrieve templates')


def get_detail_email_template_(id):

    ''' Get Gophish email template detail
    
    Retrieve email template properties
    
    Input: TemplateId in Gophish database
    Return: object reference if applies or None, 
    and message indicating OK or specific error (string). '''
    
    msg = initialize_connector()
    if msg is not None:
        return(None, msg)
    
    try:
        template = api.templates.get(template_id=id)     
        return(template, 'OK')
        
    except:
        return(None, 'ERROR: failed to retrieve email template {}. Generic error or non existent\n'.format(id))		
        

def remove_email_template_(id):

    ''' Remove Gophish email template
     
    Input: TemplateId in Gophish database
    Return: message indicating OK or specific error (string). '''
    
    msg = initialize_connector()
    if msg is not None:
        return(msg)
    
    try:
        template = api.templates.delete(template_id=id)
        return('OK')
        
    except:
        return('ERROR:  failed to remove the email template ID {}. Generic error or non existent\n'.format(id))		


def create_landing_page_template_(args):

    ''' Gophish landing page template creation 
    
    Create a new landing page for phishing campaigns

    Input: list with template name (string), file template (html), 
    capturing credentials [0 (no capture), 1 (yes) or 2 (also capture pass)],
    redirect_URL (string url)
    Return: reference to template object if applies or None, 
    and message indicating OK or specific error (string). '''
    
    msg = initialize_connector()
    if msg is not None:
        return(None, msg)
    
    template_name, file, capturing, redirect_url = args
    
    capture_credentials = False
    capture_passwords = False
    if capturing in ["1","2"]:
        capture_credentials = True
        if capturing == "2":
            capture_passwords = True
    
    try:
        html = file.read()    
        landing_page = Page(name=template_name, html=html, capture_credentials = capture_credentials, \
        capture_passwords = capture_passwords, redirect_url = redirect_url)
    
    except(FileNotFoundError):
        return(None,'ERROR: no such file {}\n'.format(filename))

    try:
        page = api.pages.post(landing_page)
        return(page, 'OK')
    
    except:
        return(None, 'ERROR: failed to create landing page template (possible name duplicate)\n')


def list_landing_page_templates_():

    ''' Gophish list landing pages
    
    List landing pages for phishing campaigns

    Input: None
    Return: list of landing page template objects or None, 
    and message indicating OK or specific error (string). '''
    
    msg = initialize_connector()
    if msg is not None:
        return(None, msg)
    
    try:
        landing_pages = api.pages.get()
        return(landing_pages,'OK')
    
    except:
        return(None, 'ERROR:  failed to retrieve templates')


def get_landing_page_template_(id):

    ''' Get Gophish landing page detail
    
    Retrieve landing page properties
    
    Input: Landing page Id in Gophish database
    Return: object reference if applies or None, 
    and message indicating OK or specific error (string). '''
    
    msg = initialize_connector()
    if msg is not None:
        return(None, msg)
    
    try:
        page = api.pages.get(page_id=id)
        return(page, 'OK')
        
    except:
        return(None, 'ERROR: failed to retrieve landing page template {}. Generic error or non existent\n'.format(id))		


def remove_landing_page_template_(id):
    
    ''' Remove Gophish landing page template
     
    Input: landing page template Id in Gophish database
    Return: template Id (string) and message indicating OK or specific error (string). '''    
    
    msg = initialize_connector()
    if msg is not None:
        return(None, msg)
    
    try:
        page = api.pages.delete(page_id=id)
        return(id, 'OK')
        
    except:
        return(None, 'ERROR:  failed to remove the landing page template ID {}. Generic error or non existent\n'.format(id))


def create_sending_profile_(args):

    ''' Gophish SMTP sending profile creation 
    
    Create a new email profile for phishing campaigns

    Input: list with 
    <PROFILE_NAME>: string with a given name for profile 
    <HOST> example: smtp.gmail.com 
    <SMTP_USERNAME> example: john.doe@gmail.com 
    <SMTP_PASS> self-explanatory 
    <FROM_USERNAME> example: John Doe 
    <FROM_EMAIL_ADDRESS> example: john.doe@gmail.com
    <IGNORE CERT ERRORS (0 or 1): ignore SSL errors (1) or not (0)
    
    Return: reference to template object if applies or None, 
    and message indicating OK or specific error (string). '''
    
    msg = initialize_connector()
    if msg is not None:
        return(None, msg)
    
    profile_name, host, smtp_username, smtp_pass, from_username, from_email_address, ignore_errs = args
    
    #by default assume SSL self-signed certificate
    if ignore_errs == '0':
        ignore_errs = False
    else: 
        ignore_errs = True
        
    smtp = SMTP(name=profile_name, host=host, from_address = from_username+' <'+from_email_address+'>',
                username=smtp_username, password=smtp_pass, ignore_cert_errors=ignore_errs)
        
    try:
        smtp = api.smtp.post(smtp)
        return(smtp, 'OK')

    except:
        return(None, 'ERROR: failed to create sender profile (possible duplicate name or invalid email)\n')


def list_sending_profile_templates_():
    
    ''' Gophish list sending SMTP profiles
    
    List SMTP profiles for phishing campaigns

    Input: None
    Return: list of SMTP profile objects or None, 
    and message indicating OK or specific error (string). '''
    
    msg = initialize_connector()
    if msg is not None:
        return(None, msg)
    
    try:
        sending_profiles = api.smtp.get()
        return(sending_profiles, 'OK')
    
    except:
        return(None, 'ERROR:  failed to retrieve SMTP profiles\n')


def get_smtp_sending_profile_(id):

    ''' Get Gophish SMTP sending profile detail
    
    Retrieve sending profile properties
    
    Input: Profile Id in Gophish database
    Return: object reference if applies or None, 
    and message indicating OK or specific error (string). '''
    
    msg = initialize_connector()
    if msg is not None:
        return(None, msg)
    
    try:
        profile = api.smtp.get(smtp_id=id)
        return(profile, 'OK')
        
    except:
        return(None, 'ERROR:  failed to retrieve landing page template {}. Generic error or non existent\n'.format(id))		
        

def remove_smtp_sending_profile_(id):
    
    ''' Remove Gophish SMTP sending profile template
     
    Input: profile Id in Gophish database
    Return: profile Id (string) or None, and message indicating OK or specific error (string). '''      

    msg = initialize_connector()
    if msg is not None:
        return(None, msg)
    
    try:
        profile = api.smtp.delete(smtp_id=id)
        return(id, 'OK')
        
    except:
        return(None, 'ERROR:  failed to remove the SMTP sending profile ID {}. Generic error or non existent\n'.format(id))


def create_campaign_(args):

    ''' Gophish phishing campaign creation 
    
    Create a new phishing campaign

    Input: list with 
    <CAMPAIGN_NAME> name for the new object campaign 
    <GROUP_NAME> user group name selected for the campaign
    <EMAIL_NAME> email template name selected for the campaign
    <LANDING_PAGE_NAME> landing page name selected for the campaign
    <SMTP_PROFILE_NAME> sending profile name selected
    <PHISH_URL> URL to send phished users for typing credentials
    <LAUNCH_TIME> optional. Format: dd/mm/yyyy@hh:mm for scheduled 
    launching or blank for inmediate

    Return: reference to campaign object if applies or None, 
    and message indicating OK or specific error (string). '''
    
    msg = initialize_connector()
    if msg is not None:
        return(None, msg)
    
    launch_time = 'now'
    
    if len(args) == 7:
        campaign_name, group_name, email_name, page_name, profile_name, phishing_url, launch_time = args
    else:
        campaign_name, group_name, email_name, page_name, profile_name, phishing_url = args
    
    groups = [Group(name=group_name)]
    page = Page(name=page_name)
    template = Template(name=email_name)
    smtp = SMTP(name=profile_name)
    
    #checking date format and vigency
    
    if launch_time == 'now':

        campaign = Campaign(
        name=campaign_name, 
        groups=groups, 
        page=page,
        template=template, 
        smtp=smtp,
        url=phishing_url,
        )

    else:    

        try:
            start_timestamp = datetime.strptime(launch_time, '%d/%m/%Y@%H:%M')        
        except ValueError:
            return(None, 'ERROR: failed to convert timestamp (possible missformat?)\n')

        if start_timestamp > datetime.now():
                launch_date = start_timestamp.isoformat()+'Z'
        else:
            return(None, 'ERROR: Launching campaign time provided is in the past!\n')
        
        campaign = Campaign(
            name=campaign_name, 
            groups=groups, 
            page=page,
            template=template, 
            smtp=smtp,
            url=phishing_url,
            launch_date=launch_date
            )
                
    try:
        #duplicated campaign names allowed in here
        new_campaign = api.campaigns.post(campaign)
        return(new_campaign, 'OK')

    except:
        return(None, 'ERROR: failed to create Campaign (possible non-existent objects?)\n')


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
        for campaign in campaigns.campaigns:
            pass
        return(campaigns, 'OK')
        
    except:
        return(None, 'ERROR:  failed to retrieve phishing campaigns\n')


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


def end_campaign_(id):
    
    ''' End Gophish campaign
    
    Set the campaign to COMPLETED without removing it from database
    
    Input: Campaign Id in Gophish database
    Return: Campaign sumary or None, and message indicating OK or specific error (string). '''      

    msg = initialize_connector()
    if msg is not None:
        return(None, msg)

    #cancelled campaigns are not accesible. Cancellable status are all but Completed.
    try:
        summary = api.campaigns.summary(campaign_id=id)
        if summary.status == 'Completed':
            return(None, 'ERROR: selected campaign status ({}) can not be completed\n'.format(summary.status))
        else:
            api.campaigns.complete(campaign_id=id)
        return(summary, 'OK')
            
    except:
        return(None, 'ERROR: failed to retrieve phishing campaign details or ID non-existent\n')


def remove_campaign_(id):

    ''' Remove Gophish campaign
     
    Input: Campaign Id in Gophish database
    Return: Campaign sumary or None, and message indicating OK or specific error (string). '''      
    
    msg = initialize_connector()
    if msg is not None:
        return(None, msg)

    try:
        summary = api.campaigns.summary(campaign_id=id)
        api.campaigns.delete(campaign_id=id)
        # print('Success: phishing campaign {} ({}) removed'.format(summary.id, summary.name))
        return(summary, 'OK')
            
    except:
        return(None, 'ERROR: failed to remove phishing campaign or non-existent\n')
