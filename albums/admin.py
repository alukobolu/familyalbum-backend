from django.contrib import admin
from .models import Files,FavoriteList,DeletedList,Albums
# Register your models here.
admin.site.register(Files) 
admin.site.register(FavoriteList) 
admin.site.register(DeletedList) 
admin.site.register(Albums) 