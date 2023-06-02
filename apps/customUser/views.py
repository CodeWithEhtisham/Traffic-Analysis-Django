from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from django.views import View
from django.views.generic import TemplateView, CreateView
from .models import CustomUser
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.contrib import messages
from .forms import UserRegisterationForm

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
			else:
				HttpResponse('You are Not Authorized User')
			
		else:
			error = 'Invalid Email or Password'
			return render(request, 'login.html', {'error': error})
	
	
	return render(request, 'login.html',)


def user_logout(request):
	logout(request)
	return render(request, 'login.html')


class UserRegister(CreateView):
	model = CustomUser
	form_class = UserRegisterationForm
	success_url = reverse_lazy('users:register')
	template_name = 'register.html'

	def form_valid(self, form):
		staff = form.save()
		# staff.set_password(form.cleaned_data['password'])
		# staff.save()
		image = form.cleaned_data['user_img']
		path = default_storage.save(''.format(image.name), image)
		staff.image_path = path
		staff.save()
		response = super().form_valid(form)
		messages.success(self.request, 'User Have Been Registerd Successfull You will be Contacted Soon.')
		return redirect(self.success_url)

