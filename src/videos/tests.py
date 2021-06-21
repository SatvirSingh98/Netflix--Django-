from django.test import TestCase

from .models import Video, VideoProxy


class TestVideoModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data1 = Video.objects.create(title='django-tutorial')
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
