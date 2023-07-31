from django.contrib import admin
from .models import Stream
from apps.members.models import CustomUser
# Register your models here.

class StreamAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'stream_id', 'stream_url', 'start_time', 'end_time')
    list_filter = ('start_time', 'end_time')

    filter_horizontal = ('users',)


admin.site.register(Stream, StreamAdmin)

