from django.db import models
from accounts.models import Account
from albums.models import Albums,Files
import uuid #For unique characters
# Create your models here.

class Posts(models.Model):
    post_id         =       models.UUIDField(default=uuid.uuid4, editable=False,unique=True, null=True)
    user            =       models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    type            =       models.CharField(max_length=5,)# TEXT / IMAGE / VIDEO / AUDIO /
    album           =       models.ForeignKey(Albums, on_delete=models.CASCADE,null=True)
    content_file    =       models.ForeignKey(Files, on_delete=models.CASCADE,null=True)
    content_text    =       models.CharField(max_length=1350,null=True)
  
    deleted         =       models.BooleanField(default=False)
    favourite       =       models.BooleanField(default=False)
    date_created    =       models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.album.name +" - "+ self.user.username


class Comments(models.Model):
    comment_id      =       models.UUIDField(default=uuid.uuid4, editable=False,unique=True, null=True)
    root_id         =       models.ForeignKey("self",on_delete=models.CASCADE,null=True)
    post            =       models.ForeignKey(Posts, on_delete=models.CASCADE,null=True)
    user            =       models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    
    type            =       models.CharField(max_length=5,)# TEXT / IMAGE / VIDEO / AUDIO /
    content_file    =       models.ForeignKey(Files, on_delete=models.CASCADE,null=True)
    content_text    =       models.CharField(max_length=1350,null=True)
  
    deleted         =       models.BooleanField(default=False)
    favourite       =       models.BooleanField(default=False)
    date_created    =       models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.post.album.name +" - "+ self.user.username

class DeletedFeeds(models.Model):
    user             =       models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    post             =       models.ForeignKey(Posts,on_delete=models.CASCADE,null=True)
    comment          =       models.ForeignKey(Comments,on_delete=models.CASCADE,null=True)
    time             =       models.DateTimeField(auto_now_add=True,null=True)
    permanent_delete =       models.BooleanField(default=False)
    

    def __str__(self):
        return  str(self.user.username) 
