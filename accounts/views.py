from django.db.models.query_utils import Q
from django.shortcuts import render, get_object_or_404,redirect

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


from . import serializers
from .models import Account,SocialLogin,WaitList,Feedback

#For authentication
from django.contrib.auth import authenticate,logout

#For gmail login
from django.contrib.auth.decorators import login_required

#For email verification
from rest_framework.decorators import api_view, permission_classes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage, message
from django.conf import settings
from .tasks import celery_verify_email

class check_user(APIView):
    def get(self,request,user):
        data ={}
        try:
            if Account.objects.filter(Q(username=user)|Q(email=user)).exists() == True:
                account = Account.objects.get(Q(username=user)|Q(email=user))
                result = True
                data["username"]     = account.username
                data["fullname"]     = account.fullname
                data['profile_image']  = str(account.profile_image.url)
            else:
                result = False
            data["result"]     = result
        except:
            data["Error"]     = "Sorry something when wrong"
        return Response(data=data)

# Create your views here.
class user_view(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        data = {}
        # check if user exist 
        user =  get_object_or_404(Account, email=request.user)
        serializer = serializers.AccountSerializer(user)

        data = serializer.data
        data['email_verified'] = user.email_verified

        data['profile_image'] = data['profile_image']
        if user.plan != None:
            data['plan'] = user.plan.space_size
            data['plan_desc'] = user.plan.desc
            data['amount'] = user.plan.amount
        else:
            data['plan'] = None
            data['plan_desc'] = None
            data['amount'] = None
        return Response(data, status=status.HTTP_200_OK)


     #for Updating user 
    def put(self, request):
        data = {}
        user =  get_object_or_404(Account, email=request.user)

        serializer = serializers.AccountSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data['email_verified'] = user.email_verified
            if user.plan != None:
                data['plan'] = user.plan.space_size
                data['plan_desc'] = user.plan.desc
                data['amount'] = user.plan.amount
            else:
                data['plan'] = None
                data['plan_desc'] = None
                data['amount'] = None
            data['profile_image'] = data['profile_image']
            data['success'] = "Success"

        else:
            data = serializer.errors   
        return Response(data,  status=status.HTTP_200_OK)



#Register users
class register_view(APIView):
    statusCode = None
    data = {}

    #The post request
    def post(self, request):
        data = {}                                                           #This is all the data that is been passed to the api Eg. Contex variables
        statusCode = ''                                                     #This is the status code for the request
        # current_site = get_current_site(request)
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            data['success'] = "Successfully registered."
            data['fullname'] = account.fullname
            data['username'] = account.username
            data['email'] = account.email
            statusCode = status.HTTP_200_OK 
        else:
            data = serializer.errors

        return Response(data)






#Login view for validation
class login_view(APIView):
    data = {}
    
    def post(self, request):
        credentials = request.data['username']
        password = request.data['password']
        # print(credentials)

        # Check if username or email exist 
        if Account.objects.filter(email=credentials).exists()==True:
            account_cred =  Account.objects.get(email=credentials) 	

        elif Account.objects.filter(username=credentials).exists()==True:
            account_cred =  Account.objects.get(username=credentials) 	

        else:
            account_cred = None
            self.data['error'] = "Username/Email not found"


        # If it does, it means the password doesnt match 
        if account_cred:
            # Check if username and passowrd match
            userAuth = authenticate(username=account_cred, password=password) 

            if userAuth is not None:					 		
                self.data['error'] = False
            else:
                self.data['error'] = "Incorrect password"



        return Response(self.data)


# Login with google 
@login_required(login_url=settings.DOMAIN_FRONTEND+"/home")
def googleLogin_view(request):

    context = {}
    newuser = "false"

    form = SocialLogin()
    form.user = request.user
    form.save()

    account =  Account.objects.get(email=request.user) 	

    if not account.email_verified:
        if account.first_name == None or account.last_name == None:
            splited_email = account.email.split('@')
            account.fullname = splited_email[0]
        else:
            account.fullname = account.first_name+" "+account.last_name
        account.registration = "google"
        account.save()
        newuser = "true"


    auth =  SocialLogin.objects.filter(user=request.user).order_by('-id').first()
    account.email_verified = True
    account.save()

    username = str(auth.user.username)
    token = str(auth.token)
    logout(request)

    return redirect(settings.DOMAIN_FRONTEND+"/accounts/login/"+username+"/"+token+"?newuser="+newuser)



#Email verification

#The browsable API link (Only for logged in users)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_email_view(request):
    data = {}
    if request.user.email_verified is not True:
        current_site = get_current_site(request)
        send_email_verification(request, request.user, mail_subject="Verify your "+current_site.domain+" account.")
        data['success'] = "Verification email has been sent to " + request.user.email
    else:
        data['success'] = "Your email has been verified already"
        data['verified'] = True

    return Response(data)




@api_view(['POST'])
def welcome_email_view(request):
    data = {}
    account =  get_object_or_404(Account, email=request.data['email'])
    if account.email_verified is not True:
        send_email_verification(request, account, mail_subject="Welcome to Family Album ")
    else:
        data['verified'] = True
    data['success'] = "Success"
    return Response(data)


   
   


#The send email function
def send_email_verification(request, account, mail_subject):

    current_site = settings.DOMAIN_FRONTEND
    mail_subject = mail_subject
    to_email = account.email
    html_template = 'email.html'

    html_message = render_to_string(html_template, {
    'user':account, 'domain':current_site,
    'uid': urlsafe_base64_encode(force_bytes(account.pk)),
    'token': account_activation_token.make_token(account),
    })
    celery_verify_email.apply_async(args=(mail_subject, html_message,to_email))




#The email verification view
@api_view(['GET'])
def activate(request, uidb64, token):
    data = {}
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except:
        user = None
        data['error'] = "Activation link is invalid!"
        return Response(data)

    if user.email_verified:
        data['success'] = "Your email has been verified already."
        data['verified'] = True
    else:
        if user is not None and account_activation_token.check_token(user, token):
            user.email_verified = True
            user.save()
            # login(request, user)
            data['success'] = "Thank you for verifying your email. Now you can login your account."
        else:
            data['error'] = "Activation link is invalid!"

    return Response(data)
@api_view(['POST'])
def setting_password(request):
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    if password == confirm_password:
        user = request.user
        user.set_password(password)
        user.save()
        data ={}
        data['success'] = "Successfully set password"
        return Response(data=data)
    else:
        data ={}
        data['error'] = "Passwords do not match"
        return Response(data=data)

class WaitLists(APIView):
    data = {}
    
    def post(self, request):
        try:
            email = request.POST['email']
            WaitList.objects.create(email=email,joined =False)
            data ={}
            data['result'] = "Successfully joined waitlist"
            return Response(data=data)
        except:
            data ={}
            data['result'] = "email exist"
            return Response(data=data)

class Feedbacks(APIView):
    data = {}
    
    def post(self, request):
        try:
            email = request.POST['email']
            message =request.POST['message']
            name = request.POST['name']
            Feedback.objects.create(email=email,name=name,message=message)
            data ={}
            data['result'] = "Successfully sent feedback"
            return Response(data=data)
        except:
            data ={}
            data['result'] = "An error occured"
            return Response(data=data)