*********************
VeraPhish README file
*********************

0. INTRODUCTION

VeraPish is a web app developed by Óscar Iglesias (osc.iglesias@gmail.com) 
in the context of an Universitary Information Security Master of Science 
End of Degree project at UNIR (unir.net) in Spain.

Based on Django framework (https://www.djangoproject.com/) and leveraging on 
python Gophish API (https://docs.getgophish.com/python-api-client/), it is 
designed to be a SETA (Security Education Training Tool) for improving 
Engineering Social Attacks awareness, focusing on Phishing campaigns.

The application has two main components:

Phishing Module. Will allow to handle through GoPhish API all phishing 
campaigns end-to-end. From creating a target group of users, to define 
emails, templates and landing pages, SMTP profiles, and more.

Training Module. Assess the theoretical social engineering awareness 
of employees through dead easy to configure training surveys, getting 
a couple of customizable global scores of effectiveness on the way.

Check INSTALLATION section for further configuration details.

*********************

1. LICENSE

License terms ans conditions
MIT License

Copyright (c) 2021 Óscar Iglesias Touceda (osc.iglesias@gmail.com)

Permission is hereby granted, free of charge, to any person obtaining 
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the 
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be 
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

*********************

2. INSTALLATION

In order to set up all to have everything up and running in a test 
environment, this is the checklist to follow. The deployment in 
production is out of scope of the following instructions.

1. Install Gophish (https://docs.getgophish.com/user-guide/installation)
as per instructions in the website.

2. Set up the config.json file for Gophish as per your needs 
checking the information in the link above. Example of file in folder docs 
in here.

3. Once Gophish is up and running, open the URL in your browser and change 
the API key as indicated here 
(https://docs.getgophish.com/user-guide/documentation/changing-user-settings). 
You will not need to get access to GoPhish directly anymore, but do copy 
the key since you will use it for VeraPhish configuration.

4. Install python (https://www.python.org/downloads/) in case you do 
not have it yet on your system.

5. Install the GoPhish API for python as per instructions in here
(https://docs.getgophish.com/python-api-client/).

6. Install the Django framework (https://docs.djangoproject.com/en/3.1/topics/install/).

7. Place VeraPhish files package in a place reachable for your Python 
and Django installation.

9. Configure cfg files for both apps (phishing and surveys), in the /modules/config/ 
folder (SETAphish.cfg and SETAsurvey.cfg respectively). There are examples for everything 
in /docs here, and you will have to use the Gophish API key you wrote down in #3 
so that all match.

10. All views in the app are only for admins (login required), except: main page 
which is dynamic, static views (help, about, license, contact), and the make survey link 
(so that users can be trained without logging in). Hence, you will need to create 
a superuser before starting to use the app (executing "python manage.py createsuperuser")
in the main directory of the app. Alternatively, you could uncomment the Register link in 
the login view, but it is not very recommendable since anyone could create their own users while 
answering surveys.

11. Execute "python manage.py runserver" from a terminal in the main app directory, and you are 
good to go with some testing (again, this tutorial is not intended to show how to set up a 
production environment/server. You will have to take care of SSL certificates, spam filtering 
when sending phishing emails..., etc).

12. Logical testing steps would be: within the Pishing section of the web app, create at 
least an user group, an email template page, a landing page, an SMTP profile and a phishing 
campaign. Later on you can go to the Survey section and create a survey template, and a training 
survey based on the phishing campaign created earlier, or on the target group itself 
(first option will leverage on phishing results to build the A-score indicator, 
which will not be available otherwise).
Example files where needed are in folder /docs, but I think using the webapp is quite 
self-explanatory.  

13. Database handling: all Gophish objects (user groups, email and landing page templates, 
SMTP profiles and phishing campaigns), are stored within Gophish database, whereas Survey templates,
Trainings launched and related User answer objects, are contained in Django database. Even though 
all actions can be performed from the app itself, Django database objects can be manipulated 
directly from the admin panel, which can be useful for testing
(e.g. in "http://127.0.0.1:8000/admin/" if you ran the server straight with "python manage.py runserver").

That should be all. Let me know if anything is unclear or I am missing something. 
Perhaps is worth mentioning I made all the development and testing in a 
windows 10 workstation.

*********************

3. ABOUT ME

I am an Electrical engineer working for many years in telecommunication operators. 
Lately, as a Cybersecurity Product Manager in Vodafone Spain. You can check my 
LinkedIn profile (https://www.linkedin.com/in/osciglesias/?locale=en_US) or email me in here 
(osc.iglesias@gmail.com).

Perfectly aware of the fact that I am not an outstanding developer, but I thought companies 
could take advantage of this web application easily. Also perhaps someone else wants to 
build anything much better on top of that, so I decided to license it 
as MIT (free to use and modify).

Will be more than happy to hear from you in case you use my contribution 
or leverage on it somehow, through any of the above commented channels.

Enjoy it and take care!

Óscar Iglesias.
