from rest_framework import serializers
from .models import Files,Albums

import re 	#This is for the username validator 


class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ['file']

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Albums
        fields = ['album_image']


class RenameAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Albums
        fields = ['name']

    def validate_folder_name(self, name):
        special_characters = "/\|*<>?;"
        if any(c in special_characters for c in name):
            raise serializers.ValidationError({"name": "name fields didn't match."})
        return name