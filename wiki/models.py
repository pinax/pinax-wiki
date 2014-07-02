import os
import re
import uuid

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .conf import settings
from .utils import binders_map, object_slug


MEDIA_RE = re.compile(r"w/file-download/(\d+)/")


class Wiki(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def latest_edits(self):
        return Revision.objects.filter(page__wiki=self).order_by("-created_at")

    class Meta:
        unique_together = [("content_type", "object_id")]


class Page(models.Model):
    wiki = models.ForeignKey(Wiki, related_name="pages", null=True)
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
    page = models.ForeignKey(Page, related_name="revisions")
    content = models.TextField(help_text="Use markdown to mark up your text")
    content_html = models.TextField()
    message = models.TextField(blank=True, help_text="Leave a helpful message about your change")
    created_ip = models.IPAddressField()
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, related_name="revisions_created")
    media = models.ManyToManyField("MediaFile", blank=True, related_name="revisions")

    def parse(self):
        self.content_html = settings.WIKI_PARSE(self.page.wiki, self.content)

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

    user = models.ForeignKey(User, related_name="media_files")
    created = models.DateTimeField(editable=False, default=timezone.now)
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to=uuid_filename)

    def download_url(self):
        return reverse("wiki_file_download", args=[self.pk, os.path.basename(self.filename)])

    def __unicode__(self):
        return self.filename
