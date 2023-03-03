from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from django.views import View
from django.views.generic import TemplateView
from .models import CustomUser
from .forms import LoginForm,Registerform
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.contrib.auth.models import User

# Create your views here.
class Login(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.filter(username=username,password=password)
            # user authenticate check 
            if user.exists():
                return render(request,'index.html')
        return render(request,'login.html',{'form':form})

class Register(View):
    def get(self,request):
        return render(request,'register.html')
    def post(self,request):
        form = Registerform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(username,email,password)
            user = CustomUser.objects.create(user=User.objects.create(username=username,email=email,password=password))
            return render(request, 'login.html')