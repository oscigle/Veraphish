***************************
VeraPhish template examples
***************************

The list of examples within the folder shows both the configuration files 
plus examples ready to use to test the apps.

For the config files, it is important to remove the comments in the filename till '] ' included.

Hereafter describing files by number id.

0: After installation, Gophish basic config.

1 and 2: Examples for setting up config for both the Django app SETAphish (phishing module) + 
SETAsurvey (training module). Notice some fields are the same in both files.

3: Example of target group of users to be fished. Used in Phishing section > Group creation. 
Can add as many users as you want.

4: Example of email template,. Used in Phishing > Email creation. Template rules available at:
https://docs.getgophish.com/user-guide/template-reference

5: Example of landing page. Used in Phishing > Landing page creation. Perhaps you feel like using the Gophish 
template creator directly for further customisation which cannot be done through API.
See reference manual (for Gophish in general, at: https://docs.getgophish.com/user-guide/).

6: Example of training email template. Placed at SETA_surveys/modules. It must include the SURVEY_LINK at least. 
Same for all surveys.

7 and 8: couple of survey templates. Templates can have as much questions as you want, 
and variable number of answers per question. The only thing you have to take care of is:
* Every question has at least one answer.
* For every question, there is at least one true answer.
Take into account that for scoring purposes, the app only take care of True options. 
That means mistakes does not substract points.

T-score only will be shown if number of respondents in % is greater than the threshold in the config file.
A-score will be shown only if the above is true and the source of users for the training was a Phishing campaign.
