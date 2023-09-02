from urllib import request
from django import forms
from .models import AppDetails

class AppDetailsForm(forms.ModelForm):
    class Meta:
        model = AppDetails
        fields = ['app_image','app_name','url']
