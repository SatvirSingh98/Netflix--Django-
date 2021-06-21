from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    video_id = models.CharField(max_length=150)

    def __str__(self):
        return self.title
