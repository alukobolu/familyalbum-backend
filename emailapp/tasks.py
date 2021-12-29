from __future__ import absolute_import,unicode_literals
# from emailapp.views import send_mass_email
from familyalbum.celery import app
from accounts.models import Account
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings



# Send to one user 
@app.task(name='send_news_letter_individual', bind=True)
def send_news_letter_individual(self,subject,message, receiver, user):
    print("started")
    try:
        html_template = 'newsletter.html'
        current_site = settings.DOMAIN_FRONTEND

        html_message = render_to_string(html_template, {
        'user':user, 'message':message, 'domain':current_site,
        })

        msg = EmailMessage(subject, html_message,  to=[receiver])
        msg.content_subtype = 'html' # this is required because there is no plain text email message
        msg.send()
        print("Sent to "+receiver)
    except:
        print("Error while sending message")
    return 


# Send to all users
@app.task(name='send_news_letter_mass', bind=True)
def send_news_letter_mass(self,subject,message):
    try:
        users = Account.objects.all()

        for user in users:
            html_template = 'newsletter.html'
            current_site = settings.DOMAIN_FRONTEND

            html_message = render_to_string(html_template, {
            'user':user.fullname, 'message':message, 'domain':current_site,
            })

            msg = EmailMessage(subject, html_message,  to=[user.email])
            msg.content_subtype = 'html' # this is required because there is no plain text email message
            msg.send()
            print("sent to "+user.email)
        return 
    except:
        print("Error while sending message")
        return