from django.db import models
from accounts.models import Account
import uuid #For unique characters


def upload_album_location(instance, filename):
	file_path = 'Album_profile/{user_id}/{file}'.format(user_id=str(instance.user.id), file=filename)
	return file_path
class Albums(models.Model):
    album_id        =       models.UUIDField(default=uuid.uuid4, editable=False,unique=True, null=True)
    name            =       models.CharField(max_length=350,null=True)
    description     =       models.CharField(max_length=350,null=True)
    members         =       models.ManyToManyField(Account, related_name="members",null=True)
    admins          =       models.ManyToManyField(Account, related_name="admin",null=True)
    user            =       models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    private         =       models.BooleanField(default=True)#it can be publicly found 
    album_image     =       models.ImageField( upload_to=upload_album_location,  default="avatar.png", blank=True, null=True,)   
    deleted         =       models.BooleanField(default=False)
    favourite       =       models.BooleanField(default=False)
    shared          =       models.BooleanField(default=False)
    lock            =       models.BooleanField(default=False)#no one can be added
    price           =       models.IntegerField(default=0)
    blacklist       =       models.BooleanField(default=False)
    date_created    =       models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name +" - "+ self.user.username


def upload_location(instance, filename):
	file_path = 'uploads/{user_id}/{file}'.format(user_id=str(instance.user.id), file=filename)
	return file_path


# DocumentFile is where actual files and its informations are stored after it has been uploaded
# Documents actual id is not used in development but doc_id field value is used in place
# Documents are not actually deleted but the its deleted field will be set as true 
# When documents are favourited it will set favourite field to True
class Files(models.Model):
    file_id         =       models.UUIDField(default=uuid.uuid4, editable=False,unique=True, null=True)
    filename        =       models.CharField(max_length=350,null=True)
    file            =       models.FileField(upload_to=upload_location,max_length=22500)
    album           =       models.ManyToManyField(Albums, related_name="Albums",null=True)    
    search_tag      =       models.CharField(max_length=350,null=True)
    user            =       models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    filetype        =       models.CharField(max_length=150,null=True)
    fileSize        =       models.CharField(max_length=150,null=True)
    fileExtension   =       models.CharField(max_length=150,null=True)

    deleted         =       models.BooleanField(default=False)
    favourite       =       models.BooleanField(default=False)

    location        =       models.CharField(max_length=150,null=True)
    user_city       =       models.CharField(max_length=150,null=True)
    user_country    =       models.CharField(max_length=150,null=True)
    user_browser    =       models.CharField(max_length=150,null=True)
     
    price           =       models.IntegerField(default=0) 
    lock            =       models.BooleanField(default=True)
    date_posted     =       models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.filename) +" - " + str(self.user.username)



# To keep track of every document that has been deleted by a user and to enable them to be able to restore deleted files 
# This DeletedList model was created 
# So information of deleted documents can be accessed using the ForeignKey to DocumentFile
class DeletedList(models.Model):
    user             =       models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    file             =       models.ForeignKey(Files,on_delete=models.CASCADE,null=True)
    album            =       models.ForeignKey(Albums,on_delete=models.CASCADE,null=True)
    filetype         =       models.CharField(max_length=500,null=True)
    time             =       models.DateTimeField(auto_now_add=True,null=True)
    permanent_delete =       models.BooleanField(default=False)
    

    def __str__(self):
        return str(self.file.filename) +" - " + str(self.user.username) 


# When a document is favourited , its information would be saved in this FavoriteList Model
# Using ForeignKey to DocumentFile users access documents that has been favourited
class FavoriteList(models.Model):
    user            =       models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    files           =       models.ForeignKey(Files,on_delete=models.CASCADE,null=True)
    album          =       models.ForeignKey(Albums,on_delete=models.CASCADE,null=True)
    filetype        =       models.CharField(max_length=500,null=True)
    time            =       models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return str(self.user.email) 
