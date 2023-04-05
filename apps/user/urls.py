from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login , name='login'),
    path('register/', views.UserRegister.as_view(), name='register'),
]