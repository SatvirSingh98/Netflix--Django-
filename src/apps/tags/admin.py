from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import TaggedItem


class TaggedItemInline(GenericTabularInline):
    model = TaggedItem
    extra = 0


@admin.register(TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    '''Admin View for TaggedItem'''

    list_display = ('__str__', 'content_type', 'object_id', 'content_object')
    readonly_fields = ('tag', 'content_type', 'object_id', 'content_object')
