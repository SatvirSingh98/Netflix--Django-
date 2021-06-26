from django.test import TestCase

from apps.categories.models import Category
from apps.playlists.models import Playlist


class TestCategoryModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category_1 = Category.objects.create(title='Comedy')
        cls.category_2 = Category.objects.create(title='Horror', active=False)
        cls.playlist_1 = Playlist.objects.create(title='Test title', category=cls.category_1)

    def test_category_model_return(self):
        """
        Test Category model return name
        """
        self.assertEqual(str(self.category_1), 'Comedy')
        self.assertEqual(str(self.category_2), 'Horror')

    def test_category_related_playlist(self):
        """
        Test category related playlist
        """
        qs = self.category_1.playlists.all()
        self.assertEqual(qs.count(), 1)
