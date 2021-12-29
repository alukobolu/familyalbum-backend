from django import forms

from .models import EmailMessageModel 


class CreateEmail(forms.ModelForm):

	class Meta:
		model = EmailMessageModel
		fields = ['title', 'body', 'receiver']