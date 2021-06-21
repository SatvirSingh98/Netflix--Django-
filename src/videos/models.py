from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    video_id = models.CharField(max_length=150)
    active = models.BooleanField(default=True)

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


class VideoProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Published Video'
        verbose_name_plural = 'Published Videos'

    def __str__(self):
        return self.title
