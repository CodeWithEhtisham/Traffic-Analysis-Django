from django.urls import path

from . import views


urlpatterns = [    
    path('', views.user_login , name='login'),
    path('registeration/', views.UserRegister.as_view(), name='register'),
    # path('profile/<int:user_id>/<str:company>/', views.user_profiles, name='profile_view'),

]