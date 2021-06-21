from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from .models import Video, VideoProxy


class TestVideoModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data1 = Video.objects.create(title='django-tutorial', video_id='video')
        cls.data2 = VideoProxy.objects.create(title='django-tutorial')

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
        data1.state = Video.VideoStateOptions.PUBLISH
        data1.save()
        data1.publish_timestamp = timezone.now()
        condition = Video.objects.filter(publish_timestamp__lte=data1.publish_timestamp).exists()
        self.assertTrue(condition)

    def test_video_publish_timestamp_if_draft(self):
        """
        Test Video model publish_timestamp
        """
        data1 = self.data1
        data1.state = Video.VideoStateOptions.DRAFT
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
