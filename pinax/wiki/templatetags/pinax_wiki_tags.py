from django import template
from django.contrib.contenttypes.models import ContentType

from ..models import Wiki

register = template.Library()


@register.assignment_tag
def wiki_for(obj):
    return Wiki.objects.get(
        object_id=obj.pk,
        content_type=ContentType.objects.get_for_model(obj)
    )
