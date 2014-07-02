import os

from django.conf.urls import patterns, url

from .conf import settings


urlpatterns = patterns(
    "wiki.views",
    url(r"^file-download/(\d+)/([^/]+)$", "file_download", name="wiki_file_download"),
    url(r"^file-upload/$", "file_upload", name="wiki_file_upload")
)

for binder in settings.WIKI_BINDERS:
    urlpatterns += patterns(
        "wiki.views",
        url(os.path.join(binder.root, r"$"), "index", {"binder": binder}, name=binder.index_url_name),
        url(os.path.join(binder.root, r"(?P<slug>[^/]+)/$"), "page", {"binder": binder}, name=binder.page_url_name),
        url(os.path.join(binder.root, r"(?P<slug>[^/]+)/edit/$"), "edit", {"binder": binder}, name=binder.edit_url_name),
    )
