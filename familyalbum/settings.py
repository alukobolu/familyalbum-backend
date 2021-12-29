"""
Django settings for familyalbum project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import decimal
import django_heroku
import dj_database_url
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
if config('DEBUG') == "true":
    DEBUG = True
elif config('DEBUG') == "false":
    DEBUG = False
else:
    DEBUG = False

# SECURITY WARNING: don't run with debug turned on in productio
ALLOWED_HOSTS = ['192.168.43.164','127.0.0.1','192.168.137.209','alukofamilyalbum.herokuapp.com']

#User model
AUTH_USER_MODEL = 'accounts.Account'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #Project Apps
    'accounts',
    'albums',
    'emailapp',
    'appSettings',
    'feeds',

    #Authentication
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    
    #External packages 
    'django_user_agents',              #For meta request 
    'corsheaders',                      #cors headers
    'crispy_forms',                     #crispy forms
    'django_cron',                      #cron jobs
    #s3 packages
    'storages',                         #django-storages

]



SITE_ID = 1

EMAIL_HOST = 'smtp.elasticemail.com'
EMAIL_HOST_USER = "hello@cloudiby.com" #config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD ="18A8EE1E77B9BD16EE1B98110C43E391121C" #config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'Cloudiby <hello@cloudiby.com>'
DEFAULT_FROM_EMAIL = 'Cloudiby <hello@cloudiby.com>'










MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

AUTHENTICATION_BACKENDS = [
    #'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

LOGIN_REDIRECT_URL = '/accounts/google-login'

ROOT_URLCONF = 'familyalbum.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'familyalbum.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':config('NAME'),
        'USER':config('USER'),
        'PASSWORD':config('PASSWORD'),
        'HOST':config('HOST')
    }
}


db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.TokenAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
        
    ],
    #   'DEFAULT_RENDERER_CLASSES': [
    #   'rest_framework.renderers.JSONRenderer',   #This is to remove the usual django render template 
    #   ]
    # 'DEFAULT_AUTHENTICATION_CLASSES': [],
    # 'DEFAULT_PERMISSION_CLASSES': [],
}

# Change password with Dj rest auth 
OLD_PASSWORD_FIELD_ENABLED = True

REST_USE_JWT = True

JWT_AUTH_COOKIE = 'familyalbum-auth'
JWT_AUTH_REFRESH_COOKIE = 'familyalbum-auth-refresh-token'

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=300000),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=180),
}


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


#Algorithm
MAXIMIUM_FREE_TIER = decimal.Decimal(config('MAXIMIUM_FREE_TIER'))

# Crispy Forms 
CRISPY_TEMPLATE_PACK ='bootstrap4'

# # CRONJOBS 
# CRON_CLASSES = [
#     "subscription.cron.MyCronJob",
#     # ...
# ]

#S3 BUCKETS CONFIG

# AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_S3_REGION_NAME = "us-east-2"
# AWS_QUERYSTRING_EXPIRE = 3600

# S3_USE_SIGV4 =True

#STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'




# DOMAINS 
DOMAIN_BACKEND = config('DOMAIN_BACKEND')
DOMAIN_FRONTEND =  config('DOMAIN_FRONTEND')
django_heroku.settings(locals())

FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800

CELERY_RESULT_BACKEND= config('REDIS_TLS_URL')
CELERY_BROKER_URL = config('REDIS_TLS_URL')

DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True