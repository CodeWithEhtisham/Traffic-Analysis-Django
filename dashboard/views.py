from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.contrib.auth.models import User


class Index(TemplateView):
    def get(self,request):
        return render(request,'dashboard/index.html')


class Dashboard(TemplateView):
    def get(self,request):
        return render(request,'dashboard/dashboard.html')

class History(TemplateView):
    def get(self,request):
        return render(request,'dashboard/history.html')

class VideoAnalysis(TemplateView):
    def get(self,request):
        return render(request,'dashboard/video_analysis.html')

class LiveStream(TemplateView):
    def get(self,request):
        return render(request,'dashboard/live_stream.html')