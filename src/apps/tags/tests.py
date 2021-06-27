from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.utils import IntegrityError
from django.test import TestCase

from apps.playlists.models import Playlist

from .models import TaggedItem


class TestTaggedItemModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.playlist = Playlist.objects.create(title='dummy title')
        cls.playlist_2 = Playlist.objects.create(title='dummy title')
        cls.playlist.tags.add(TaggedItem(tag='new-tag'), bulk=False)
        cls.playlist_2.tags.add(TaggedItem(tag='new-tag'), bulk=False)

    def test_content_type_is_not_null(self):
        with self.assertRaises(IntegrityError):
            TaggedItem.objects.create(tag='comedy')

    def test_create_via_content_type(self):
        c_type = ContentType.objects.get(app_label='playlists', model='playlist')
        tag = TaggedItem.objects.create(tag='dummy-tag', content_type=c_type, object_id=self.playlist.id)
        self.assertIsNotNone(tag.pk)
        self.assertEqual(str(tag), 'dummy-tag')

    def test_create_via_model_content_type(self):
        c_type = ContentType.objects.get_for_model(Playlist)
        tag = TaggedItem.objects.create(tag='dummy-tag', content_type=c_type, object_id=self.playlist.id)
        self.assertIsNotNone(tag.pk)

    def test_create_via_app_loader_content_type(self):
        PlaylistClass = apps.get_model(app_label='playlists', model_name='Playlist')
        c_type = ContentType.objects.get_for_model(PlaylistClass)
        tag = TaggedItem.objects.create(tag='dummy-tag', content_type=c_type, object_id=self.playlist.id)
        self.assertIsNotNone(tag.pk)

    def test_related_field(self):
        self.assertEqual(self.playlist.tags.count(), 1)

    def test_related_field_create(self):
        self.playlist.tags.create(tag='another-new-tag')
        self.assertEqual(self.playlist.tags.count(), 2)

    def test_related_field_query_name(self):
        qs = TaggedItem.objects.filter(playlist__title__iexact=self.playlist.title)
        self.assertEqual(qs.count(), 2)

    def test_related_field_via_content_type(self):
        c_type = ContentType.objects.get_for_model(Playlist)
        tag_qs = TaggedItem.objects.filter(content_type=c_type, object_id=self.playlist.id)
        self.assertEqual(tag_qs.count(), 1)

    def test_direct_obj_creation(self):
        obj = self.playlist
        tag = TaggedItem.objects.create(content_object=obj, tag='another1')
        self.assertIsNotNone(tag.pk)
