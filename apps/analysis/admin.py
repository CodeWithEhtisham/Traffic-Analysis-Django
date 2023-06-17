from django.contrib import admin
from .models import Stream
# Register your models here.
class StreamAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'stream_id', 'stream_url', 'start_time', 'end_time')
    list_filter = ('start_time', 'end_time')


admin.site.register(Stream, StreamAdmin)