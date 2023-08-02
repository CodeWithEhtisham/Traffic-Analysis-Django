from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from django.views import View
from django.views.generic import TemplateView
from .forms import LoginForm,Registerform
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.core.files.storage import default_storage
from django.contrib import messages
from django.contrib.auth.models import User
from .models import CustomUser
from .forms import UserRegistration
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
import logging

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user:
            if user is not None and user.is_active and user.is_staff:
                login(request, user)

                return redirect('index')
            
            elif user is not None and user.is_active == True:
                print(user)
                try:
                    # req_user = CustomUser.objects.get(id=user.id)
                    # user_uid = req_user.id
                    # user_company = req_user.company
                    login(request, user)
                    return redirect('index')

                except:
                    return HttpResponse('Your Account is not Active Yet')
            else:
                return HttpResponse('Your Account is not Active Yet')  
        else:
            return HttpResponse('Please Register before login')              
    else:
        return render(request, 'login.html')

    
    

class UserRegister(CreateView):
    model = CustomUser
    form_class = UserRegistration
    success_url = reverse_lazy('register')
    template_name = 'register.html'

    def form_valid(self, form):
        print('Form Valid')
        users = form.save()
        image = form.cleaned_data['user_img']
        path = default_storage.save(image.name, image)
        users.image_path = path
        users.save()
        response = super().form_valid(form)
        messages.success(self.request, 'Registerd Successfully You will be Contacted Soon.')
        return redirect(self.success_url)        


class Logout(View):
    def get(self,request):
        return render(request,'login.html')
    

