import os

from django.conf.urls import url

from .conf import settings
from .views import edit, file_download, file_upload, index, page

app_name = "pinax_wiki"

urlpatterns = [
    url(r"^file-download/(\d+)/([^/]+)$", file_download, name="file_download"),
    url(r"^file-upload/$", file_upload, name="file_upload")
]

for binder in settings.PINAX_WIKI_BINDERS:
    urlpatterns += [
        url(os.path.join(binder.root, r"$"), index, {"binder": binder}, name=binder.index_url_name),
        url(os.path.join(binder.root, r"(?P<slug>[^/]+)/$"), page, {"binder": binder}, name=binder.page_url_name),
        url(os.path.join(binder.root, r"(?P<slug>[^/]+)/edit/$"), edit, {"binder": binder}, name=binder.edit_url_name),
    ]
