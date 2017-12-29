from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save

from .conf import settings
from .models import Wiki


def handle_object_save(sender, **kwargs):
    created = kwargs.pop("created")
    obj = kwargs.pop("instance")
    if created:
        Wiki.objects.create(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk
        )


for binder in settings.PINAX_WIKI_BINDERS:
    if binder.bind_to_model:
        post_save.connect(handle_object_save, sender=binder.bind_to_model)
