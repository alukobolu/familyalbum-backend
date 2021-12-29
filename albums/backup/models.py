from django.db import models
from accounts.models import Account

import uuid #For unique characters

# from inboxes.models import InboxList

# Create your models here.

# UPLOAD_FROM = (
#     ('direct','DIRECT'),
#     ('inbox', 'INBOX'),

# )
class InboxList(models.Model):
    name = models.CharField(max_length=350,null=True) #its fake



def upload_location(instance, filename):
	file_path = 'uploads/{user_id}/{file}'.format(user_id=str(instance.user.id), file=filename)
	return file_path
# DocumentFile is where actual files and its informations are stored after it has been uploaded
# Documents actual id is not used in development but doc_id field value is used in place
# Documents are not actually deleted but the its deleted field will be set as true 
# When documents are favourited it will set favourite field to True
class DocumentFile(models.Model):
    filename        =       models.CharField(max_length=350,null=True)
    user            =       models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    filetype        =       models.CharField(max_length=150,null=True)
    fileSize        =       models.CharField(max_length=150,null=True)
    fileExtension   =       models.CharField(max_length=150,null=True)
    files           =       models.FileField(upload_to=upload_location)
    private         =       models.BooleanField(default=True)
    Uploaded_from   =       models.CharField(max_length=6, default='DIRECT')
    inbox           =       models.ForeignKey(InboxList,on_delete=models.CASCADE,null=True, blank=True)
    time            =       models.DateTimeField(auto_now_add=True)
    doc_id          =       models.UUIDField(default=uuid.uuid4, editable=False,unique=True, null=True)
    deleted         =       models.BooleanField(default=False)
    favourite       =       models.BooleanField(default=False)
    Ip_address      =       models.CharField(max_length=150,null=True, blank=True)
    user_city       =       models.CharField(max_length=150,null=True, blank=True)
    user_country    =       models.CharField(max_length=150,null=True, blank=True)
    user_browser    =       models.CharField(max_length=150,null=True, blank=True)

    def __str__(self):
        return self.filename +" - "+ self.user.username

# When a document is favourited , its information would be saved in this FavoriteList Model
# Using ForeignKey to DocumentFile users access documents that has been favourited
class FavoriteList(models.Model):
    user            =       models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    files           =       models.ForeignKey(DocumentFile,on_delete=models.CASCADE,null=True)
    filetype        =       models.CharField(max_length=50,null=True)
    time            =       models.DateTimeField(auto_now_add=True,null=True)
    Ip_address      =       models.CharField(max_length=150,null=True)
    user_city       =       models.CharField(max_length=150,null=True)
    user_country    =       models.CharField(max_length=150,null=True)
    user_browser    =       models.CharField(max_length=150,null=True)

    def __str__(self):
        return str(self.user.email) + '->' + str(self.files.filename)

# To keep track of every document that has been deleted by a user and to enable them to be able to restore deleted files 
# This DeletedList model was created 
# So information of deleted documents can be accessed using the ForeignKey to DocumentFile
class DeletedList(models.Model):
    user            =       models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    files           =       models.ForeignKey(DocumentFile,on_delete=models.CASCADE,null=True)
    filetype        =       models.CharField(max_length=50,null=True)
    time            =       models.DateTimeField(auto_now_add=True,null=True)
    deleted         =       models.BooleanField(default=False)
    Ip_address      =       models.CharField(max_length=150,null=True)
    user_city       =       models.CharField(max_length=150,null=True)
    user_country    =       models.CharField(max_length=150,null=True)
    user_browser    =       models.CharField(max_length=150,null=True)

    def __str__(self):
        return str(self.user.email) + '->' + str(self.files.filename)

# For Data analysis , to know the exact document viewed by each user and at the exact time 
class DocumentView(models.Model):
    user            =       models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    files           =       models.ForeignKey(DocumentFile,on_delete=models.CASCADE,null=True)
    filetype        =       models.CharField(max_length=50,null=True)
    time            =       models.DateTimeField(null=True)
  
    Ip_address      =       models.CharField(max_length=150,null=True)
    user_city       =       models.CharField(max_length=150,null=True)
    user_country    =       models.CharField(max_length=150,null=True)
    user_browser    =       models.CharField(max_length=150,null=True)

    def __str__(self):
        return self.user.first_name + '->' + self.files.filename