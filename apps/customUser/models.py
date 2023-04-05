from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone

# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')
    user_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True,blank=True)
    cnic = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    address = models.TextField(max_length=200, null=True, blank=True)
    user_img = models.ImageField(upload_to='User_Images', null=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    ojects = CustomUserManager()

    def __str__(self):
        return self.user_name

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    class Meta:
        verbose_name_plural = '1.User&Accounts'