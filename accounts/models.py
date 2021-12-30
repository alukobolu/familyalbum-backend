from django.core.mail import message
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid 
from django_resized import ResizedImageField

# from django.conf import settings
# from django.db.models.signals import post_save
# # from django.dispatch import receiver
# from rest_framework.authtoken.models import Token

#This is the folder where profile images are stored
def upload_location(instance, filename):
	file_path = 'profile_image/{user_id}/{image}'.format(user_id=str(instance.id), image=filename)
	return file_path


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')
		

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


# Create your models here.
class Account(AbstractBaseUser):
    email					= models.EmailField(verbose_name="email",  max_length=60, unique=True)
    username				= models.CharField(max_length=30, unique=True)
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    first_name				= models.CharField(max_length=30, null=True, blank=True)
    last_name				= models.CharField(max_length=30, null=True, blank=True)
    fullname				= models.CharField(max_length=50)

    #Custom fields
    email_verified			= models.BooleanField(default=False)    
    phonenumber             = models.CharField(max_length=30, unique=True)
    profile_image           = ResizedImageField(size=[100, 100], upload_to=upload_location,  default="avatar.png", blank=True, null=True,)                                                                 #Verified email
    registration            = models.CharField(max_length=100, default='familyalbum')                                                  #Where user is registering
    user_city               = models.CharField(max_length=100, null=True, blank=True)                                               #User city location
    user_country            = models.CharField(max_length=100, null=True, blank=True)                                               #User country location
    no_files				= models.IntegerField(default=0)                                                                        #Number of files this user have
    is_blocked				= models.CharField(max_length=30, null=True, blank=True)                                                #Suspended this user from using the service
    status  				= models.CharField(max_length=30, null=True, blank=True)



    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
    
    




# For Social Login
class SocialLogin(models.Model):
    user            = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    token           = models.UUIDField(default=uuid.uuid4, editable=False,unique=True, null=True)
    active          = models.BooleanField(default=True)
    time            = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.user.username

class   WaitList(models.Model):
    email       =       models.EmailField(verbose_name="wait_email",  max_length=60, unique=True)
    time        =       models.DateTimeField(auto_now_add=True,null=True)
    joined      =       models.BooleanField(default=False)
    

    def __str__(self):
        return  str(self.email) 

class   Feedback(models.Model):
    email       =       models.EmailField(verbose_name="wait_email",  max_length=60, unique=False)
    name        =       models.CharField(max_length=60,null=True)
    message     =       models.CharField(max_length=6000,null=True)
    time        =       models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return  str(self.email) 