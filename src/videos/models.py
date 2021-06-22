from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from core.db.models import PublishStateOptions
from core.db.receivers import publish_state_pre_save, slugify_pre_save


class VideoQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(state=PublishStateOptions.PUBLISH, publish_timestamp__lte=now)


class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class Video(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    video_id = models.CharField(max_length=150, unique=True)
    active = models.BooleanField(default=True)
    state = models.CharField(max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = VideoManager()

    class Meta:
        verbose_name = 'Videos'
        verbose_name_plural = 'All Videos'

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        if self.active:
            return 'Yes'
        return 'No'

    def get_playlist_ids(self):
        return list(self.playlist_set.all().values_list('id', flat=True))


pre_save.connect(publish_state_pre_save, sender=Video)
pre_save.connect(slugify_pre_save, sender=Video)


class VideoProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Published Video'
        verbose_name_plural = 'Published Videos'

    def __str__(self):
        return self.title
