from django.db import models

<<<<<<< HEAD
# Create your models here.
class Sites(models.Model):
    site_id = models.AutoField(primary_key=True)
    site_name = models.CharField(max_length=20, null=True)
    site_address = models.CharField(max_length=20, null=True)
    site_img = models.ImageField(upload_to='main_site_img', null=True)
    site_cord = models.CharField(max_length=200, null=True, blank=True)
    
=======
# class Site(models.Model):
#     name = models.CharField(max_length=255)
#     url = models.CharField(max_length=255)

class Stream(models.Model):
    # site = models.ForeignKey(Site, on_delete=models.CASCADE)
    site_name = models.CharField(max_length=255)
    stream_id = models.CharField(max_length=255)
    stream_url = models.CharField(max_length=255)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)

class Image(models.Model):
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=False)

class Object(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    confidence = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    w = models.FloatField()
    h = models.FloatField()
>>>>>>> 0c617537db299ad2ce2d5921795e8e49d1f7192b
