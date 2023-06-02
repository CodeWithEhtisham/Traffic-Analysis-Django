from django.db import models

# Create your models here.
class Sites(models.Model):
    site_id = models.AutoField(primary_key=True)
    site_name = models.CharField(max_length=20, null=True)
    site_address = models.CharField(max_length=20, null=True)
    site_img = models.ImageField(upload_to='main_site_img', null=True)
    site_cord = models.CharField(max_length=200, null=True, blank=True)
    