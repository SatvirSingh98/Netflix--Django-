from django.test import TestCase

from .models import Video


class TestVideoModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data1 = Video.objects.create(title='django-tutorial')

    def test_video_model_return(self):
        """
        Test Video model return name
        """
        data1 = self.data1
        self.assertIsInstance(data1, Video)
        self.assertEqual(str(data1), 'django-tutorial')
