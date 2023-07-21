from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(default=False, max_length=13)
    age = models.IntegerField(null=True, blank=True)
    
    male = 'Male'
    female = 'Female'

    type_gender = (
        (male, 'Male'),
        (female, 'Female'),
    )
    
    gender = models.CharField(max_length=10, choices=type_gender)
    city = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    cnic = models.CharField(max_length=20, null=True, blank=True)
    company = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=35)
    user_img = models.ImageField(upload_to='staff_images', null=True, blank=True)
    date_joined = models.DateField(_('date joined'), auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    @property
    def get_absolute_image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.user_img.url)
