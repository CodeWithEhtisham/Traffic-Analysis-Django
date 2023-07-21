from django.urls import path

from .views import Login,Register


urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('register', Register.as_view(), name='register'),
]