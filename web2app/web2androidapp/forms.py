from urllib import request
from django import forms
from .models import AppDetails,UserBasicInfo

class AppDetailsForm(forms.ModelForm):
    class Meta:
        model = AppDetails
        fields = ['app_image','app_name','url']
        
class UserBasicInfoForm(forms.ModelForm):
    class Meta:
        model = UserBasicInfo
        exclude = ['user','created_at','updated_at']
        widgets = {
            "email": forms.TextInput(attrs={'class':'form-control'}),
            "first_name": forms.TextInput(attrs={'class':'form-control'}),
            "last_name": forms.TextInput(attrs={'class':'form-control'}),
            "phone": forms.TextInput(attrs={'class':'form-control'}),
            "position": forms.TextInput(attrs={'class':'form-control'}),
            "website": forms.TextInput(attrs={'class':'form-control'}),
            "about": forms.TextInput(attrs={'class':'form-control'}),
                   }
