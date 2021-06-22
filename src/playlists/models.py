from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from core.db.models import PublishStateOptions
from core.db.receivers import publish_state_pre_save, slugify_pre_save
from videos.models import Video


class PlaylistQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(state=PublishStateOptions.PUBLISH, publish_timestamp__lte=now)


class PlaylistManager(models.Manager):
    def get_queryset(self):
        return PlaylistQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class Playlist(models.Model):
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    state = models.CharField(max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PlaylistManager()

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        if self.active:
            return 'Yes'
        return 'No'


pre_save.connect(publish_state_pre_save, sender=Playlist)
pre_save.connect(slugify_pre_save, sender=Playlist)
