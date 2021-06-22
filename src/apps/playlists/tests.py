from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from apps.videos.models import Video

from .models import Playlist, PublishStateOptions


class TestPlaylistModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data1 = Video.objects.create(title='django-tutorial', video_id='abc123')
        cls.data2 = Playlist.objects.create(title='django-tutorial', video=cls.data1)

    def test_playlist_model_return(self):
        """
        Test Playlist model return name
        """
        data2 = self.data2
        self.assertIsInstance(data2, Playlist)
        self.assertEqual(str(data2), 'django-tutorial')

    def test_playlist_publish_timestamp_if_published(self):
        """
        Test Playlist model publish_timestamp
        """
        data2 = self.data2
        data2.state = PublishStateOptions.PUBLISH
        data2.save()
        data2.publish_timestamp = timezone.now()
        condition = Playlist.objects.published().exists()
        self.assertTrue(condition)

    def test_playlist_publish_timestamp_if_draft(self):
        """
        Test Playlist model publish_timestamp
        """
        data2 = self.data2
        data2.state = PublishStateOptions.DRAFT
        data2.save()
        self.assertEqual(data2.publish_timestamp, None)

    def test_playlist_is_published(self):
        """
        Test Playlist model is_published
        """
        data2 = self.data2
        setattr(data2, data2.is_published, 'Yes')
        self.assertEqual(data2.is_published, 'Yes')
        data2.active = False
        setattr(data2, data2.is_published, 'No')
        self.assertEqual(data2.is_published, 'No')

    def test_playlist_slug_field(self):
        """
        Test Playlist model slug field
        """
        title_slug = slugify(self.data2.title)
        self.assertEqual(title_slug, self.data2.slug)

    def test_video_playlist(self):
        """
        Test foreign key relation
        """
        qs = self.data1.playlist_set.all()
        self.assertEqual(qs.count(), 1)
