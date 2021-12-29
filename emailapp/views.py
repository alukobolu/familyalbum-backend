from django.http import request
from emailapp import admin
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from .tasks import send_news_letter_individual ,send_news_letter_mass
from . import forms
from django.contrib.auth.decorators import login_required

from accounts.models import Account


# Create your views here.
#The send email function
def subscribtion_error(email,fullname,amount,card_type,last4, mail_subject):
    current_site = settings.DOMAIN_FRONTEND
    mail_subject = mail_subject
    to_email = email
    html_template = 'subscriptionError.html'

    html_message = render_to_string(html_template, {
        'fullname':fullname,'amount':amount,'card_type':card_type,'last4':last4, 'domain':current_site,
    })

    message = EmailMessage(mail_subject, html_message,  to=[to_email])
    message.content_subtype = 'html' # this is required because there is no plain text email message
    return message.send(fail_silently=False)

    
# Create your views here.
#The send email function
def send_email_recieve_inbox(email,fullname, mail_subject):
    current_site = settings.DOMAIN_FRONTEND
    mail_subject = mail_subject
    to_email = email
    html_template = 'recieveInboxEmail.html'

    html_message = render_to_string(html_template, {
        'fullname':fullname, 'domain':current_site,
    })

    message = EmailMessage(mail_subject, html_message,  to=[to_email])
    message.content_subtype = 'html' # this is required because there is no plain text email message
    return message.send(fail_silently=False)

    
# Create your views here.
#The send email function

def send_email_upload(account, mail_subject):
    current_site = settings.DOMAIN_FRONTEND
    mail_subject = mail_subject
    to_email = account.email
    html_template = 'uploadEmail.html'

    html_message = render_to_string(html_template, {
    'user':account, 'domain':current_site,
    })

    message = EmailMessage(mail_subject, html_message,  to=[to_email])
    message.content_subtype = 'html' # this is required because there is no plain text email message
    message.send()

#The send email function for Shared folder
def send_email_sharedFolder(account, mail_subject, joinedUser, folderName):
    current_site = settings.DOMAIN_FRONTEND
    mail_subject = mail_subject
    to_email = account.email
    html_template = 'sharedFolder.html'

    html_message = render_to_string(html_template, {
    'user':account, 'domain':current_site, 'joinedUser' : joinedUser,  'folderName' : folderName, 
    })
  
    message = EmailMessage(mail_subject, html_message,  to=[to_email])
    message.content_subtype = 'html' # this is required because there is no plain text email message
    message.send()


@login_required(login_url="http://cloudiby.com/")
def send_email_view(request):
    context = {}
    context['username'] = request.user

    # If logged in user is not admin, redirect to cloudiby
    if not request.user.is_admin:
        return redirect("https://cloudiby.com/")

    # If its post request
    if request.method == 'POST':
        subject = request.POST['title']
        message = request.POST['body']
        receiver = request.POST['receiver']
        form = forms.CreateEmail(request.POST)
        text_content = message
        html_content = message
        if form.is_valid():
            try:
                # if it is sent to one particular user 
                if request.POST['receiver'] != "hello@cloudiby.com":
                    msg = EmailMultiAlternatives(subject, text_content, 'Cloudiby <hello@cloudiby.com>', [receiver])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                else:
                    # if we want to send it to all users, we set email to cloudibynet@gmail.com
                    users = Account.objects.all()
                    for user in users:
                        msg = EmailMultiAlternatives(subject, text_content, 'Cloudiby <hello@cloudiby.com>', [user.email])
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()


                instance = form.save(commit=False)
                instance.save()
                context['success'] = "Email successfully sent to "+receiver
            except:
                context['error'] = "Error while sending email"
        else:
            context['error'] = "Error while sending email"
    else:
        form = forms.CreateEmail()
        
    return render(request, 'sendemail.html', context)


@login_required(login_url="http://cloudiby.com/")
def send_email_view(request):
    context = {}
    context['username'] = request.user

    # If logged in user is not admin, redirect to cloudiby
    if not request.user.is_admin:
        return redirect("https://cloudiby.com/")

    # If its post request
    if request.method == 'POST':
        subject = request.POST['title']
        message = request.POST['body']
        receiver = request.POST['receiver']
        form = forms.CreateEmail(request.POST)
        # text_content = message
        # html_content = message


        if form.is_valid():
           
            context['success'] = "Email successfully sent to "+receiver

            # try:
            # if it is sent to one particular user 
            if request.POST['receiver'] != "hello@cloudiby.com":
                try:
                    account = Account.objects.get(email=request.POST['receiver'])
                    user = account.fullname
                except:
                    user = receiver
                    
                send_news_letter_individual.apply_async(args=(subject,message,receiver, user))

               
            else:
                # if we want to send it to all users, we set email to cloudibynet@gmail.com
                send_news_letter_mass.apply_async(args=(subject,message))
                # send_mass_email(message=message, subject=subject)
                


            instance = form.save(commit=False)
            instance.save()
            context['success'] = "Email successfully sent to "+receiver
            # except:
            #     context['error'] = "Error while sending email"
        else:
            context['error'] = "Error while sending email"
    else:
        form = forms.CreateEmail()
        
    return render(request, 'sendemail.html', context) 