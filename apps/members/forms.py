from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    

class Registerform(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistration(UserCreationForm):
# password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = (
            'name','lastname', 'email', 'phone',
            'age', 'gender', 'city', 'address', 'cnic', 'company',
            'role', 'user_img',
        )

class UserRegistrationChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = (
            'name','lastname', 'email', 'phone',
            'age', 'gender', 'city', 'address', 'cnic', 'company',
            'role', 'user_img',
        )

