from django import forms
from .models import CustomUser
import re
from django.core.exceptions import ValidationError
class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_img','first_name', 'last_name', 'email', 'phone_number']

    
    
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name == '':
            raise ValidationError("Enter First Name")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if last_name == '':
            raise ValidationError("Enter Last Name")
        return last_name

    def clean_profile_img(self):
        profile_img = self.cleaned_data.get('profile_img')
        if not profile_img:
            return self.instance.profile_img
        
        return profile_img