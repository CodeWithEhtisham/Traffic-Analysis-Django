from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import AccessToken
# Create your models here.
# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         # Normalize the email address
#         email = self.normalize_email(email)
        
#         # Create a new user object
#         user = self.model(email=email, **extra_fields)
        
#         # Set the password
#         user.set_password(password)
        
#         # Save the user object
#         user.save(using=self._db)
        
#         return user

#     def create_superuser(self, email, password, **extra_fields):
#         # Normalize the email address
#         email = self.normalize_email(email)
        
#         # Create a new user object
#         user = self.model(email=email, **extra_fields)
        
#         # Set the password
#         user.set_password(password)
        
#         # Set the user role as admin
#         user.is_superuser = True
        
#         # Save the user object
#         user.save(using=self._db)
        
#         return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, blank=True, null=True)
    email=models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    token = models.CharField(max_length=255, blank=True, null=True)


    # unique emial field
    USERNAME_FIELD = 'username'

    # objects = CustomUserManager()

     # Add related_name to the groups field to avoid clash with default User model
    # Add related_name to the groups and user_permissions fields
    # groups = models.ManyToManyField(
    #     'auth.Group',
    #     related_name='custom_users',
    #     blank=True,
    #     help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    #     verbose_name='groups',
    # )
    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     related_name='custom_users',
    #     blank=True,
    #     help_text='Specific permissions for this user.',
    #     verbose_name='user permissions',
    # )

    # Override the save method to create or update the token when the user is saved
    # Override the save method to create or update the token when the user is saved
    def save(self, *args, **kwargs):
        is_new_user = self.pk is None  # Check if it's a new user being created
        super().save(*args, **kwargs)  # Save the user model first

        if is_new_user:
            self.generate_token()  # Generate a token for new users

    def generate_token(self):
        token = AccessToken.for_user(self)
        self.token = str(token)
        self.save()

