from django.contrib import admin

from .models import Playlist, PlaylistItem


class PlaylistItemInline(admin.TabularInline):
    extra = 0
    model = PlaylistItem


@admin.register(Playlist)
class Playlist(admin.ModelAdmin):
    inlines = [PlaylistItemInline]
