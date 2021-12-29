from rest_framework import serializers
from .models import Account
import re 	#This is for the username validator 


#Register a user
class RegisterSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={'input_type' : 'password'}, write_only=True)
    fullname = serializers.CharField(required=True)


    class Meta:
        model = Account
        fields = ['fullname', 'email','username', 'password', 'password2','phonenumber' ]
        extra_kwarg = {
            'password' : {'write_only' : True}
        }

    def save(self):
        account = Account (email=self.validated_data['email'], username=self.validated_data['username'], fullname=self.validated_data['fullname'], phonenumber=self.validated_data['phonenumber'])
        password = self.validated_data['password']    
        password2 = self.validated_data['password2']   
        username = self.validated_data['username']
        fullname = self.validated_data['fullname']
        phonenumber = self.validated_data['phonenumber']
    
        #Add validations before saving
        if (len(fullname) >50):                                                                                                             #Make sure that fullname is not more than 50
            raise serializers.ValidationError({'fullname' : 'Fullname cannot be more than 50 characters.'})

        if (len(username) < 3) or (len(username) >15):
            raise serializers.ValidationError({'username' : 'Username must be between 3 to 15 characters.'})                                #Make sure that username is between 3 - 15 characters

        if not re.match(r'^[.A-Za-z0-9_-]+$', username):
            raise serializers.ValidationError({'username' : 'Username must only contain [A-Z], [a-z], [0-9], [_-.]characters.'})            #Make sure that username diesnt have irregular characters

        if not re.match(r'^[0-9]', phonenumber):
            raise serializers.ValidationError({'Phone_Number' : 'Phone must only contain [0-9] characters.'})            #Make sure that username diesnt have irregular characters

        if password != password2:
            raise serializers.ValidationError({'password' : 'Passwords do not match.'})                                                     #Make sure that passwords match

        account.set_password(password)
        account.save()
        return account






#Check user with username
class AccountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Account
        fields = ['id','username', 'email', 'fullname', 'profile_image' ]

    # This is to update user details 
    def update(self, instance, validated_data):
    
        if Account.objects.filter(email=self.validated_data['email']).exists() ==True:
            pass
        else:
            instance.email_verified = False
        

        instance.username           = self.validated_data['username']
        instance.email              = self.validated_data['email']
        instance.fullname           = self.validated_data['fullname']
        if self.validated_data.get('profile_image'):
            instance.profile_image      = self.validated_data['profile_image']
        
        #Username validations before saving
        username = instance.username
        profile_image = instance.profile_image
        


        if (len(username) < 3) or (len(username) >15):
            raise serializers.ValidationError({'username' : 'Username must be between 3 to 15 characters.'})

        if not re.match(r'^[.A-Za-z0-9_-]+$', username):
            raise serializers.ValidationError({'username' : 'Username must only contain [A-Z], [a-z], [0-9], [_-.]characters.'})
        
        if profile_image is None:
            raise serializers.ValidationError({'profile_image' : 'Profile image is required.'})
        
        # Save the instance 
        instance.save()
        return instance