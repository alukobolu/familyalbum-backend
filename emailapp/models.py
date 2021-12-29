from django.db import models
# Create your models here.

class EmailMessageModel(models.Model):
    title       =  models.CharField(max_length=1000)
    body         =  models.CharField(max_length=10000)
    receiver     =   models.CharField(max_length=10000)
    time         =  models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.title