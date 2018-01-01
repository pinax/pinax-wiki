import os
import re
import uuid

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .conf import settings
from .utils import binders_map, object_slug

try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey


MEDIA_RE = re.compile(r"w/file-download/(\d+)/")


class Wiki(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.IntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def latest_edits(self):
        return Revision.objects.filter(page__wiki=self).order_by("-created_at")

    class Meta:
        unique_together = [("content_type", "object_id")]


class Page(models.Model):
    wiki = models.ForeignKey(Wiki, related_name="pages", null=True, on_delete=models.CASCADE)
    slug = models.SlugField()

    def get_absolute_url(self):
        slug = object_slug(self.wiki)
        return binders_map()[slug].page_url(self.wiki, self.slug)

    def get_edit_url(self):
        slug = object_slug(self.wiki)
        return binders_map()[slug].edit_url(self.wiki, self.slug)

    class Meta:
        unique_together = [("wiki", "slug")]


class Revision(models.Model):
    page = models.ForeignKey(Page, related_name="revisions", on_delete=models.CASCADE)
    content = models.TextField(help_text="Use markdown to mark up your text")
    content_html = models.TextField()
    message = models.TextField(blank=True, help_text="Leave a helpful message about your change")
    created_ip = models.GenericIPAddressField()
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="revisions_created", on_delete=models.CASCADE)
    media = models.ManyToManyField("MediaFile", blank=True, related_name="revisions")

    def parse(self):
        self.content_html = settings.PINAX_WIKI_PARSE(self.page.wiki, self.content)

    def process_media(self):
        pks = MEDIA_RE.findall(self.content)
        media = MediaFile.objects.filter(user=self.created_by, pk__in=pks)
        self.media.clear()
        for mf in media:
            self.media.add(mf)

    def save(self, *args, **kwargs):
        super(Revision, self).save(*args, **kwargs)
        self.process_media()

    class Meta:
        get_latest_by = "created_at"


def uuid_filename(instance, filename):
    ext = filename.split(".")[-1]
    filename = "{0}.{1}".format(uuid.uuid4(), ext)
    return os.path.join("revision-files", filename)


class MediaFile(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="media_files", on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False, default=timezone.now)
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to=uuid_filename)

    def download_url(self):
        return reverse("pinax_wiki_file_download", args=[self.pk, os.path.basename(self.filename)])

    def __unicode__(self):
        return self.filename
