from django.contrib import admin

from .models import Video, VideoProxy

admin.site.register(Video)
admin.site.register(VideoProxy)
