from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from apps.categories.models import Category
from apps.tags.models import TaggedItem
from apps.videos.models import Video
from core.db.models import PublishStateOptions
from core.db.receivers import publish_state_pre_save, slugify_pre_save


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
    class PlaylistTypeChoices(models.TextChoices):
        MOVIE = 'movie', 'Movie'
        SHOW = 'tv show', 'TV Show'
        SEASON = 'season', 'Season'
        PLAYLIST = 'playlist', 'Playlist'

    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='playlists')
    order = models.IntegerField(default=1)
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True,
                              blank=True, related_name='playlist_featured')

    # info: m2m fields does not give info about when the individual videos were added and for what.
    # del: videos = models.ManyToManyField(Video, blank=True, related_name='playlist_item')
    videos = models.ManyToManyField(Video, blank=True, related_name='playlist_item', through='PlaylistItem')

    type = models.CharField(max_length=8, choices=PlaylistTypeChoices.choices, default=PlaylistTypeChoices.PLAYLIST)
    title = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    state = models.CharField(max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = GenericRelation(TaggedItem, related_query_name='playlist')

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


# imp: This model will give info about relation between playlist and videos.
# imp: It will return playlist queryset and not video queryset.
class PlaylistItem(models.Model):
    # info: Actual fields have to corresspond correctly.
    # info: Both the m2m field and model class must be fk(s) here.
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-timestamp']


class TVShowProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=True, type=Playlist.PlaylistTypeChoices.SHOW)


class TVShowProxy(Playlist):

    objects = TVShowProxyManager()

    class Meta:
        proxy = True
        verbose_name = 'TV Show'
        verbose_name_plural = 'TV Shows'

    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistTypeChoices.SHOW
        super().save(*args, **kwargs)


class TVShowSeasonProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=False, type=Playlist.PlaylistTypeChoices.SEASON)


class TVShowSeasonProxy(Playlist):

    objects = TVShowSeasonProxyManager()

    class Meta:
        proxy = True
        verbose_name = 'Season'
        verbose_name_plural = 'Seasons'

    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistTypeChoices.SEASON
        super().save(*args, **kwargs)


class MovieProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(type=Playlist.PlaylistTypeChoices.MOVIE)


class MovieProxy(Playlist):

    objects = MovieProxyManager()

    class Meta:
        proxy = True
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistTypeChoices.MOVIE
        super().save(*args, **kwargs)
