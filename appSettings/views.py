from typing import Set
from django.conf import settings
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Setting 

class SettingsView(APIView):
    def get(self,request,format=None):
        context ={}
        try:
            instance = Setting.objects.all()
            for f in instance :
                context[f.name] = f.value
            return Response(context,status=200)
        except:
            return Response(status=404)

    def post(self,request,format=None):
        settings = request.data['settings']
        bad_settings = []
        for setting in settings:
            try:
                new_settings  = Setting.objects.create(name=setting['NAME'],value=setting['VALUE'])
                new_settings.save()
            except:
                bad_settings.append(setting)
        if len(bad_settings)>0:
            return Response({"INVALID_SETTINGS":bad_settings},status=200)
        else:      
            return  Response(status=200)
