#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Views for SETA_gophish app

import csv
from io import TextIOWrapper
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from .forms import CreationGroupForm, CreationTemplateForm, CreationLandingPageForm, CreationSMTPProfileForm, CreationCampaignForm 
from .modules.DjangoSETAmodules import *


def index(request):

    ''' Main page view.
    
    Show general info if not authenticated or
    main menus for phishing or surveys. '''
    
    return render(request, 'SETA_gophish/index.html')


@login_required
def create_group(request):

    ''' Pishing group of users creation
    
    Create a new group of users to be phished or trained
    
    Input file format: CSV delimited by comma, no headers, 
    one line per user, four fields (First Name, Last Name, 
    Email, Position). '''
    
    if request.method == 'POST':
        context = {'error_msg': 'ERROR, form not filled in properly'}
        form = CreationGroupForm(request.POST, request.FILES)
        if form.is_valid():
            group_name = form.cleaned_data['group_name']
            file = TextIOWrapper(request.FILES['your_file'].file, encoding=request.encoding)
            args = [group_name, file]
            group, msg = create_group_(args)
            if msg == 'OK':
                context = {'group_name': group_name}
            else:
                context = {'error_msg': msg}
    else:
        form = CreationGroupForm()
        context = {'form': form}
    return render(request, 'SETA_gophish/create_group.html', context)


@login_required
def list_groups(request):    

    ''' List Gophish user groups
    
    Print target groups and high level details. '''

    groups, msg = list_groups_()
    if msg == 'OK':
        context = {'groups': groups}
    else:
        context = {'error_msg': msg}    
    return render(request, 'SETA_gophish/list_groups.html', context)


@login_required
def get_detail_group(request, group_id):

    ''' Get Gophish user group detail
    
    Retrieve user group details. '''

    group, msg = get_detail_group_(group_id)
    if msg == 'OK':
        context = {'group': group}
    else:
        context = {'error_msg': msg}    
    return render(request, 'SETA_gophish/details_group.html', context)


@login_required
def remove_group(request, group_id):

    ''' Remove Gophish user group detail
    '''
    
    msg = remove_group_(group_id)
    if msg == 'OK':
        context = {'group': group_id}
    else:
        context = {'error_msg': msg}    
    return render(request, 'SETA_gophish/remove_group.html', context)


@login_required
def create_email_template(request):

    ''' Gophish email template creation 
    
    Create a new template email for phishing campaigns. '''
    
    if request.method == 'POST':
        context = {'error_msg': 'ERROR, form not filled in properly'}
        form = CreationTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            template_name = form.cleaned_data['template_name']
            email_subject = form.cleaned_data['email_subject']
            file = TextIOWrapper(request.FILES['your_file'].file, encoding=request.encoding)
            args = [template_name, email_subject, file]
            template, msg = create_email_template_(args)
            if msg == 'OK':
                context = {'template': template}
            else:
                context = {'error_msg': msg}
    else:
        form = CreationTemplateForm()
        context = {'form': form}
    return render(request, 'SETA_gophish/create_email_template.html', context)


@login_required
def list_templates(request):    

    ''' Gophish list email templates 
    
    List email templates for phishing campaigns. '''

    templates, msg = list_email_templates_()
    if msg == 'OK':
        context = {'templates': templates}
    else:
        context = {'error_msg': msg}
    return render(request, 'SETA_gophish/list_templates.html', context)
    

@login_required
def get_detail_template(request, template_id):

    ''' Get Gophish email template detail
    
    Retrieve email template properties. '''
    
    template, msg = get_detail_email_template_(template_id)
    if msg == 'OK':
        context = {'template': template}
    else:
        context = {'error_msg': msg}    
    return render(request, 'SETA_gophish/details_template.html', context)
    
    
@login_required
def remove_template(request, template_id):
    
    ''' Remove Gophish email template
    '''
    
    msg = remove_email_template_(template_id)
    if msg == 'OK':
        context = {'template': template_id}
    else:
        context = {'error_msg': msg}    
    return render(request, 'SETA_gophish/remove_template.html', context)
    

@login_required
def create_landing_page(request):

    ''' Gophish landing page template creation
    
    Create a new landing page for phishing campaigns. '''    

    if request.method == 'POST':
        context = {'error_msg': 'ERROR, form not filled in properly'}
        form = CreationLandingPageForm(request.POST, request.FILES)
        if form.is_valid():
            template_name = form.cleaned_data['template_name']
            file = TextIOWrapper(request.FILES['your_file'].file, encoding=request.encoding)
            capturing_credentials = form.cleaned_data['capturing_credentials']
            redirect_url = form.cleaned_data['redirect_url']
            args = [template_name, file, capturing_credentials, redirect_url]
            landing_page, msg = create_landing_page_template_(args)
            if msg == 'OK':
                context = {'landing_page': landing_page}
            else:
                context = {'error_msg': msg}
    else:
        form = CreationLandingPageForm()
        context = {'form': form}
    return render(request, 'SETA_gophish/create_landing_page.html', context)
    
 
@login_required
def list_landing_pages(request):    

    ''' Gophish list landing pages
    
    List landing pages for phishing campaigns. '''

    landing_pages, msg = list_landing_page_templates_()
    if msg == 'OK':
        context = {'landing_pages': landing_pages}
    else:
        context = {'error_msg': msg}
    return render(request, 'SETA_gophish/list_landing_pages.html', context)
    
    
@login_required
def get_detail_landing_page(request, landing_page_id):

    ''' Get Gophish landing page detail
    
    Retrieve landing page properties. '''

    landing_page, msg = get_landing_page_template_(landing_page_id)
    if msg == 'OK':
        context = {'landing_page': landing_page}
    else:
        context = {'error_msg': msg}
    return render(request, 'SETA_gophish/details_landing_page.html', context)
    

@login_required
def remove_landing_page(request, landing_page_id):

    ''' Remove Gophish landing page template
    '''
    
    landing_page_id, msg = remove_landing_page_template_(landing_page_id)
    if msg == 'OK':
        context = {'landing_page_id': landing_page_id}
    else:
        context = {'error_msg': msg}    
    return render(request, 'SETA_gophish/remove_landing_page.html', context)
    

@login_required
def create_profile(request):

    ''' Gophish SMTP sending profile creation 
    
    Create a new email profile for phishing campaigns. '''

    if request.method == 'POST':
        context = {'error_msg': 'ERROR, form not filled in properly'}
        form = CreationSMTPProfileForm(request.POST)
        if form.is_valid():
            profile_name = form.cleaned_data['profile_name']
            smtp_host = form.cleaned_data['smtp_host']
            smtp_username = form.cleaned_data['smtp_username']
            smtp_pass = form.cleaned_data['smtp_pass']
            from_username = form.cleaned_data['from_username']
            from_email_address = form.cleaned_data['from_email_address']
            ignore_errs = form.cleaned_data['ignore_errs']
                               
            args = [profile_name, smtp_host, smtp_username, smtp_pass, from_username, from_email_address, ignore_errs]
            profile, msg = create_sending_profile_(args)
            if msg == 'OK':
                context = {'profile': profile}
            else:
                context = {'error_msg': msg}
    else:
        form = CreationSMTPProfileForm()
        context = {'form': form}
    return render(request, 'SETA_gophish/create_sending_profile.html', context)
    
@login_required
def list_profiles(request):

    ''' Gophish list sending SMTP profiles
    
    List SMTP profiles for phishing campaigns '''
    
    profiles, msg = list_sending_profile_templates_()
    if msg == 'OK':
        context = {'profiles': profiles}
    else:
        context = {'error_msg': msg}
    return render(request, 'SETA_gophish/list_profiles.html', context)


@login_required
def get_detail_profile(request, profile_id):

    ''' Get Gophish SMTP sending profile detail
    
    Retrieve sending profile properties. '''
    
    profile, msg = get_smtp_sending_profile_(profile_id)
    if msg == 'OK':
        context = {'profile': profile}
    else:
        context = {'error_msg': msg}
    return render(request, 'SETA_gophish/details_profile.html', context)
    

@login_required
def remove_profile(request, profile_id):

    ''' Remove Gophish SMTP sending profile template     
    '''     
    
    profile_id, msg = remove_smtp_sending_profile_(profile_id)
    if msg == 'OK':
        context = {'profile_id': profile_id}
    else:
        context = {'error_msg': msg}    
    return render(request, 'SETA_gophish/remove_profile.html', context)

    
@login_required
def create_campaign(request):

    ''' Gophish phishing campaign creation 
    
    Create a new phishing campaign. '''

    if request.method == 'POST':
        context = {'error_msg': 'ERROR, form not filled in properly'}
        form = CreationCampaignForm(request.POST)
        if form.is_valid():
            campaign_name = form.cleaned_data['campaign_name']
            target_group_name = form.cleaned_data['target_group_name']
            email_template_name = form.cleaned_data['email_template_name']
            landing_page_name = form.cleaned_data['landing_page_name']
            smtp_profile_name = form.cleaned_data['smtp_profile_name']
            phishing_url = form.cleaned_data['phishing_url']
            launch_date = form.cleaned_data['launch_date']    #format: dd/mm/yyyy@hh:mm (15 chars)
            
            if launch_date !='':
                args = [campaign_name, target_group_name, email_template_name, landing_page_name, smtp_profile_name, phishing_url, launch_date] 
            else:
                args = [campaign_name, target_group_name, email_template_name, landing_page_name, smtp_profile_name, phishing_url]
                
            campaign, msg = create_campaign_(args)
            if msg == 'OK':
                context = {'campaign': campaign}
            else:
                context = {'error_msg': msg}
    else:
        form = CreationCampaignForm()
        context = {'form': form}
    return render(request, 'SETA_gophish/create_campaign.html', context)


@login_required
def list_campaigns(request):
    
    ''' Gophish list phishing campaigns
    
    List existing phishing campaigns. '''
    
    campaigns, msg = list_campaigns_()
    
    #reformat dates
    for campaign in campaigns.campaigns:
        campaign.created_date = campaign.created_date[0:16]
        campaign.launch_date = campaign.created_date[0:16]
    
    if msg == 'OK':
        context = {'campaigns': campaigns}
    else:
        context = {'error_msg': msg}
    return render(request, 'SETA_gophish/list_campaigns.html', context)


@login_required
def get_detail_campaign(request, campaign_id):

    ''' Get Gophish phishing campaign details
    
    Retrieve phishing campaign properties. '''

    summary, details, msg = get_campaign_details_(campaign_id)
    
    if msg == 'OK':
        summary.created_date = summary.created_date[0:16]
        summary.launch_date = summary.created_date[0:16]
        context = {'summary': summary, 'details': details}
    else:
        context = {'error_msg': msg}
    return render(request, 'SETA_gophish/details_campaign.html', context)
    
    
@login_required
def end_campaign(request, campaign_id):

    ''' End Gophish campaign
    
    Set the campaign to COMPLETED without removing it from database. '''      

    summary, msg = end_campaign_(campaign_id)
    if msg == 'OK':
        context = {'summary': summary}
    else:
        context = {'error_msg': msg}    
    return render(request, 'SETA_gophish/end_campaign.html', context)
    
    
@login_required
def remove_campaign(request, campaign_id):
    
    ''' Remove Gophish campaign
    ''' 
    
    summary, msg = remove_campaign_(campaign_id)
    if msg == 'OK':
        context = {'summary': summary}
    else:
        context = {'error_msg': msg}    
    return render(request, 'SETA_gophish/remove_campaign.html', context)

    
@login_required
def download_campaign_stats(request, campaign_id):
    
    ''' Download campaign stats
    
    Download in CSV file the main stats 
    
    'Campaign ID', 'Name', 'Created date', 'Launch date', 'Status', 'Email template',
    'Landing page', 'SMTP profile', 'Phishing URL', 'Totals','Sent', 'Opened', 
    'Clicked', 'Submitted data', 'Errors'
    
    ''' 
    
    
    try:
        summary, details, msg = get_campaign_details_(campaign_id)
        if msg != 'OK':
            raise Http404('File download not available')
    except:
        raise Http404('File download not available')
    
    now = datetime.now().strftime("%d%m%Y_%H%M%S")
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = ('attachment; filename="Campaign_{}_stats_{}.csv"'.format(summary.name, now))

    writer = csv.writer(response)
    writer.writerow(['General Phishing Campaign Information'])
    writer.writerow(['Campaign ID', 'Name', 'Created date', 'Launch date', 'Status', 'Email template', \
        'Landing page', 'SMTP profile', 'Phishing URL', 'Totals','Sent', 'Opened', 'Clicked', 'Submitted data', 'Errors'])
    writer.writerow([summary.id, summary.name, summary.created_date, summary.launch_date, summary.status, details.template.name, \
        details.page.name, details.smtp.name, details.url, summary.stats.total, summary.stats.sent, \
        summary.stats.opened, summary.stats.clicked, summary.stats.submitted_data, summary.stats.error])
        
    return response
    
    
@login_required
def download_campaign_users(request, campaign_id):
    
    ''' Download campaign stats
    
    Download in CSV file the user campaign stats 
    
    'User ID', 'First Name', 'Last Name', 'Email', 'Position', 'Status'
    
    '''
    
    try:
        summary, details, msg = get_campaign_details_(campaign_id)
        if msg != 'OK':
            raise Http404('File download not available')
    except:
        raise Http404('File download not available')
    
    now = datetime.now().strftime("%d%m%Y_%H%M%S")
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = ('attachment; filename="Campaign_{}_user_stats_{}.csv"'.format(summary.name, now))

    writer = csv.writer(response)
    writer.writerow(['User ID', 'First Name', 'Last Name', 'Email', 'Position', 'Status'])
    for result in details.results:
        writer.writerow([result.id, result.first_name, result.last_name, result.email, result.position, result.status])
    
    return response
    
    
def show_license(request):
    
    ''' Show license
    
    Static view with MIT license. '''
    
    return render(request, 'SETA_gophish/license.html')
    
    

def show_contact(request):
    
    ''' Show contact
    
    Author details of contact. '''
    
    return render(request, 'SETA_gophish/contact.html')
    


def show_about(request):
    
    ''' Show about
    
    Site and author details. '''
    
    return render(request, 'SETA_gophish/about.html')
    
    

def show_help(request):
    
    ''' Show help
    
    Basic guidance about the web application. '''
    
    return render(request, 'SETA_gophish/help.html')
