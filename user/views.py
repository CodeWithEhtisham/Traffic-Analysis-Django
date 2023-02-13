from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from django.views import View
from django.views.generic import TemplateView

# Create your views here.
class Login(View):
    def get(self,request):
        return render(request,'authentication/login.html')
    def post(self,request):
        return HttpResponse('post')

class Register(View):
    def get(self,request):
        return render(request,'authentication/register.html')
    def post(self,request):
        return HttpResponse('post')