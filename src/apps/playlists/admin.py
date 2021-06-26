from django.contrib import admin

from .models import (MovieProxy, Playlist, PlaylistItem, TVShowProxy,
                     TVShowSeasonProxy)


class PlaylistItemInline(admin.TabularInline):
    extra = 0
    model = PlaylistItem


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    inlines = [PlaylistItemInline]

    def get_queryset(self, request):
        return Playlist.objects.filter(type=Playlist.PlaylistTypeChoices.PLAYLIST)


class TVShowSeasonProxyInline(admin.TabularInline):
    extra = 0
    model = TVShowSeasonProxy
    fields = ('order', 'title', 'state')


@admin.register(TVShowProxy)
class TVShowProxyAdmin(admin.ModelAdmin):
    inlines = [TVShowSeasonProxyInline]
    fields = ('title', 'state', 'description', 'video', 'slug')

    def get_queryset(self, request):
        return TVShowProxy.objects.all()


class SeasonEpisodeProxyInline(admin.TabularInline):
    extra = 0
    model = PlaylistItem


@admin.register(TVShowSeasonProxy)
class TVShowSeasonProxyAdmin(admin.ModelAdmin):
    inlines = [SeasonEpisodeProxyInline]
    list_display = ('__str__', 'parent')

    def get_queryset(self, request):
        return TVShowSeasonProxy.objects.all()


@admin.register(MovieProxy)
class MovieProxyAdmin(admin.ModelAdmin):
    fields = ('title', 'state', 'description', 'video', 'slug')

    def get_queryset(self, request):
        return MovieProxy.objects.all()
