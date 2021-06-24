from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from apps.videos.models import Video

from .models import Playlist, PublishStateOptions


class TestPlaylistModel(TestCase):
    def create_show_with_seasons(self):
        the_office = Playlist.objects.create(title='The Office Series')
        Playlist.objects.create(title='The Office Series Season 1', parent=the_office, order=1)
        Playlist.objects.create(title='The Office Series Season 2', parent=the_office, order=2)
        Playlist.objects.create(title='The Office Series Season 3', parent=the_office, order=3)
        self.show = the_office

    def create_videos(self):
        self.video_1 = Video.objects.create(title='django-tutorial', video_id='abc1')
        self.video_2 = Video.objects.create(title='django-tutorial', video_id='abc12')
        self.video_3 = Video.objects.create(title='django-tutorial', video_id='abc123')
        self.video_qs = Video.objects.all()

    @classmethod
    def setUpTestData(cls):
        cls.create_videos(cls)
        cls.create_show_with_seasons(cls)
        cls.playlist_1 = Playlist.objects.create(title='django-tutorial', video=cls.video_1)
        cls.playlist_2 = Playlist.objects.create(title='django-tutorial')
        cls.playlist_2.videos.set(cls.video_qs)
        cls.playlist_2.save()

    def test_playlist_model_return(self):
        """
        Test Playlist model return name
        """
        playlist_1 = self.playlist_1
        self.assertIsInstance(playlist_1, Playlist)
        self.assertEqual(str(playlist_1), 'django-tutorial')

    def test_published_count(self):
        """
        Test count of published playlists
        """
        qs = Playlist.objects.filter(state=PublishStateOptions.PUBLISH)
        self.assertEqual(qs.count(), 0)

    def test_draft_count(self):
        """
        Test count of draft playlists
        """
        qs = Playlist.objects.filter(state=PublishStateOptions.DRAFT)
        self.assertEqual(qs.count(), 6)

    def test_playlist_publish_timestamp_if_published(self):
        """
        Test Playlist model publish_timestamp
        """
        playlist_1 = self.playlist_1
        playlist_1.state = PublishStateOptions.PUBLISH
        playlist_1.save()
        playlist_1.publish_timestamp = timezone.now()
        condition = Playlist.objects.published().exists()
        self.assertTrue(condition)

    def test_playlist_publish_timestamp_if_draft(self):
        """
        Test Playlist model publish_timestamp
        """
        playlist_1 = self.playlist_1
        playlist_1.state = PublishStateOptions.DRAFT
        playlist_1.save()
        self.assertEqual(playlist_1.publish_timestamp, None)

    def test_playlist_is_published(self):
        """
        Test Playlist model is_published
        """
        playlist_1 = self.playlist_1
        setattr(playlist_1, playlist_1.is_published, 'Yes')
        self.assertEqual(playlist_1.is_published, 'Yes')
        playlist_1.active = False
        setattr(playlist_1, playlist_1.is_published, 'No')
        self.assertEqual(playlist_1.is_published, 'No')

    def test_playlist_slug_field(self):
        """
        Test Playlist model slug field
        """
        title_slug = slugify(self.playlist_1.title)
        self.assertEqual(title_slug, self.playlist_1.slug)

    def test_video_playlist(self):
        """
        Test foreign key relation
        """
        qs = self.video_1.playlist_featured.all()
        self.assertEqual(qs.count(), 1)

    def test_playlist_many_to_many_relation(self):
        """
        Test many_to_many key relation
        """
        qs_count = self.playlist_2.videos.count()
        self.assertEqual(qs_count, 3)

    def test_playlist_many_to_many_through_relation(self):
        """
        Test many_to_many 'through' key relation
        """
        video_qs = sorted(self.video_qs.values_list('id', flat=True))
        playlist_video_qs = sorted(self.playlist_2.videos.all().values_list('id', flat=True))
        playlistitem_qs = sorted(self.playlist_2.playlistitem_set.all().values_list('video', flat=True))
        self.assertEqual(video_qs, playlist_video_qs, playlistitem_qs)

    def test_show_has_seasons(self):
        """
        Test to confirm created shows have seasons
        """
        seasons = self.show.playlist_set.all()
        self.assertEqual(seasons.count(), 3)
