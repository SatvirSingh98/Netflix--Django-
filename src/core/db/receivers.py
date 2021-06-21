from django.utils import timezone
from django.utils.text import slugify

from .models import PublishStateOptions


def publish_state_pre_save(sender, instance, *args, **kwargs):
    if instance.state == PublishStateOptions.PUBLISH and instance.publish_timestamp is None:
        instance.publish_timestamp = timezone.now()
    elif instance.state == PublishStateOptions.DRAFT:
        instance.publish_timestamp = None


def slugify_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        instance.slug = slugify(instance.title)
