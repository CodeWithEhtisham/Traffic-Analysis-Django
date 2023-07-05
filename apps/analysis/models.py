from django.db import models

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
    # count = models.IntegerField()
    total_count_in = models.IntegerField()
    total_count_out = models.IntegerField()

class Object(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    confidence = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    w = models.FloatField()
    h = models.FloatField()
