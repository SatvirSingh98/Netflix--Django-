from django.contrib import admin

from .models import Video, VideoProxy


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    '''Admin View for Video'''

    list_display = ('__str__', 'id', 'state', 'video_id', 'is_published', 'get_playlist_ids')
    search_fields = ('title',)
    list_filter = ('active', 'state')
    readonly_fields = ('publish_timestamp', 'get_playlist_ids')


@admin.register(VideoProxy)
class VideoProxyAdmin(admin.ModelAdmin):
    '''Admin View for VideoProxy'''

    list_display = ('__str__', 'id', 'video_id')
    search_fields = ('title',)

    def get_queryset(self, request):
        return VideoProxy.objects.filter(active=True)
