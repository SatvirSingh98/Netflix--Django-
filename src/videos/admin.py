from django.contrib import admin

from .models import Video, VideoProxy


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    '''Admin View for Video'''

    list_display = ('__str__', 'video_id')
    search_fields = ('title',)


@admin.register(VideoProxy)
class VideoProxyAdmin(admin.ModelAdmin):
    '''Admin View for VideoProxy'''

    list_display = ('__str__', 'video_id')
    search_fields = ('title',)

    def get_queryset(self, request):
        return VideoProxy.objects.filter(active=True)
