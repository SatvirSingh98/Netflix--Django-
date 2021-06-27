import random

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.playlists.models import Playlist

from .models import Rating, RatingChoices

User = get_user_model()


class TestRatingModel(TestCase):
    def create_playlists(self):
        items = []
        self.playlist_count = random.randint(10, 200)
        for i in range(self.playlist_count):
            items.append(Playlist(title=f'show_{i}'))
        Playlist.objects.bulk_create(items)
        self.playlists = Playlist.objects.all()

    def create_users(self):
        items = []
        self.user_count = random.randint(10, 500)
        for i in range(self.user_count):
            items.append(User(username=f'user_{i}'))
        User.objects.bulk_create(items)
        self.users = User.objects.all()

    def create_ratings(self):
        items = []
        self.rating_count = 1_000
        for i in range(self.rating_count):
            user_obj = self.users.order_by('?').first()
            ply_obj = self.playlists.order_by('?').first()
            items.append(Rating(
                user=user_obj,
                value=random.choice(RatingChoices.choices)[0],
                content_object=ply_obj
            ))
        Rating.objects.bulk_create(items)
        self.ratings = Rating.objects.all()

    @classmethod
    def setUpTestData(cls):
        cls.create_users(cls)
        cls.create_playlists(cls)
        cls.create_ratings(cls)

    def test_user_count(self):
        qs = User.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), self.user_count)
        self.assertEqual(self.users.count(), self.user_count)

    def test_playlist_count(self):
        qs = Playlist.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), self.playlist_count)
        self.assertEqual(self.playlists.count(), self.playlist_count)

    def test_rating_count(self):
        qs = Rating.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), self.rating_count)
        self.assertEqual(self.ratings.count(), self.rating_count)

    def test_rating_random_choices(self):
        value_set = set(Rating.objects.values_list('value', flat=True))
        self.assertTrue(len(value_set) > 1)
