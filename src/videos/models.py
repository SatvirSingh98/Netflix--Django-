from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    video_id = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class VideoProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Published Video'
        verbose_name_plural = 'Published Videos'

    def __str__(self):
        return self.title
