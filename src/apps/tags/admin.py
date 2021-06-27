from django.contrib import admin

from .models import TaggedItem


@admin.register(TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    '''Admin View for TaggedItem'''

    list_display = ('__str__', 'content_type', 'object_id', 'content_object')
    readonly_fields = ('content_object',)
