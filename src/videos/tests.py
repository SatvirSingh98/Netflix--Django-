from django.http import HttpRequest
from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from playlists.models import Playlist

from .admin import VideoProxyAdmin
from .models import PublishStateOptions, Video, VideoProxy


class TestVideoModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data1 = Video.objects.create(title='django-tutorial', video_id='video')
        cls.data2 = VideoProxy.objects.create(title='django-tutorial')
        cls.data3 = Playlist.objects.create(title='django-tutorial', video=cls.data1)

    def test_video_model_return(self):
        """
        Test Video model return name
        """
        data1 = self.data1
        self.assertIsInstance(data1, Video)
        self.assertEqual(str(data1), 'django-tutorial')

    def test_video_proxy_model_return(self):
        """
        Test VideoProxy model return name
        """
        data1 = self.data1
        data2 = self.data2
        self.assertIsInstance(data2, VideoProxy)
        self.assertEqual(str(data1), str(data2))

    def test_video_publish_timestamp_if_published(self):
        """
        Test Video model publish_timestamp
        """
        data1 = self.data1
        data1.state = PublishStateOptions.PUBLISH
        data1.save()
        data1.publish_timestamp = timezone.now()
        condition = Video.objects.published().exists()
        self.assertTrue(condition)

    def test_video_publish_timestamp_if_draft(self):
        """
        Test Video model publish_timestamp
        """
        data1 = self.data1
        data1.state = PublishStateOptions.DRAFT
        data1.save()
        self.assertEqual(data1.publish_timestamp, None)

    def test_video_is_published(self):
        """
        Test Video model is_published
        """
        data1 = self.data1
        setattr(data1, data1.is_published, 'Yes')
        self.assertEqual(data1.is_published, 'Yes')
        data1.active = False
        setattr(data1, data1.is_published, 'No')
        self.assertEqual(data1.is_published, 'No')

    def test_video_slug_field(self):
        """
        Test Video model slug field
        """
        title_slug = slugify(self.data1.title)
        self.assertEqual(title_slug, self.data1.slug)

    def test_get_playlist_ids(self):
        """
        Test get_playlist_ids for videos
        """
        qs = self.data1.get_playlist_ids()
        self.assertIn(self.data1.id, qs)

    def test_admin_get_queryset(self):
        """
        Test get_queryset for admin
        """
        qs = VideoProxyAdmin.get_queryset(self, request=HttpRequest())
        self.assertEqual(qs.count(), 2)
