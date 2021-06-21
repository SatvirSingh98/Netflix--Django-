from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Video(models.Model):
    class VideoStateOptions(models.TextChoices):
        PUBLISH = 'PU', 'Publish'
        DRAFT = 'DR', 'Draft'

    title = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    video_id = models.CharField(max_length=150, unique=True)
    active = models.BooleanField(default=True)
    state = models.CharField(max_length=2, choices=VideoStateOptions.choices, default=VideoStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Videos'
        verbose_name_plural = 'All Videos'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.state == self.VideoStateOptions.PUBLISH and self.publish_timestamp is None:
            self.publish_timestamp = timezone.now()
        elif self.state == self.VideoStateOptions.DRAFT:
            self.publish_timestamp = None
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def is_published(self):
        if self.active:
            return 'Yes'
        return 'No'


class VideoProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Published Video'
        verbose_name_plural = 'Published Videos'

    def __str__(self):
        return self.title
