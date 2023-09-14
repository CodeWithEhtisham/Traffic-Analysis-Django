from django.db import models
from apps.members.models import CustomUser
from django.contrib import admin
from django.utils.html import format_html
# class Site(models.Model):
#     name = models.CharField(max_length=255)
#     url = models.CharField(max_length=255)

class Stream(models.Model):
    # site = models.ForeignKey(Site, on_delete=models.CASCADE)
    site_name = models.CharField(max_length=255)
    stream_id = models.CharField(max_length=255)
    users = models.ManyToManyField(CustomUser)
    stream_url = models.CharField(max_length=255)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)

class Image(models.Model):
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=False)
    

class VehicleObject(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    confidence = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    w = models.FloatField()
    h = models.FloatField()
    # count = models.IntegerField()
    total_count_in = models.IntegerField(default=0)
    total_count_out = models.IntegerField(default=0)


class VideoAnalysisModel(models.Model):
    video_name = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    video_path = models.CharField(max_length=255)
    status=models.PositiveSmallIntegerField(default=0)
    excel_path = models.CharField(max_length=255,default=None,null=True)
    short_video_path = models.CharField(max_length=255,default=None,null=True)


class VideoAnalysisObject(models.Model):
    video_analysis = models.ForeignKey(VideoAnalysisModel, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    label = models.CharField(max_length=255)
    confidence = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    w = models.FloatField()
    h = models.FloatField()
    # count = models.IntegerField()
    total_count_in = models.IntegerField(default=0)
    total_count_out = models.IntegerField(default=0)