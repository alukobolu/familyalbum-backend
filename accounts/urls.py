from django.urls import path, include
from . import views

app_name = "accounts_api"

urlpatterns = [
    path('user/', views.user_view.as_view(), name='get_user'),                       #Check user api
    path('register', views.register_view.as_view(), name='register_user'),              #Register User
    path('welcome/email/',  views.welcome_email_view, name='welcome_email'),               #send verification email link

    path('login', views.login_view.as_view(), name='login_user'),                       #API login validator

    path('set_password', views.setting_password, name='set_password'),
    path('auth/', include('dj_rest_auth.urls')),
    #path('auth/', include('dj_rest_auth.urls', namespace='djrest_api')),                #dj rest auth login, change password etc
    path('google-login', views.googleLogin_view, name='login_with_google'),              #Login with Google
    path('verify/email/',  views.verify_email_view, name='verify_email'),               #send verification email link
    path('confirm/email/<uidb64>/<token>/',  views.activate, name='activate'),       #Verify the email
    path('check_user/<user>', views.check_user.as_view(), name='check_user'),

    path('wait', views.WaitLists.as_view(), name='wait'),
    path('feedback', views.Feedbacks.as_view(), name='feedback'),





    # URLs that do not require user to be logged in djrest auth.
    # ---------------------------------------------------------------------------
    # login/                  Login Url
    # password/reset/         Reset password
    # password-reset/confirm/<uidb64>/<token>/        Reset password link
    
    # URLs that require a user to be logged in djrest auth.
    # -----------------------------------------------------------------------
    # logout/                 Logout url
    # user/                   Check the user who is logged in
    # password/change/        Change the logged in user password
    # token/verify/           verify token
    # token/refresh/          Refresh the jwt token
                

]