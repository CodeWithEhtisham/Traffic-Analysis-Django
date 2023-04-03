from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UserRegisterationForm(UserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = (
            'user_name', 'last_name', 'address', 'cnic', 'phone',
            'email', 'user_img'
        )

class UserRegisterationChangeForm(UserChangeForm):
    
    class Meta: 
        model = CustomUser
        fields = (
            'user_name', 'last_name', 'address', 'cnic', 'phone',
            'email', 'user_img'
        )
