from django.conf.urls import include, url

urlpatterns = [
    url(r"^", include("pinax.wiki.urls", namespace="pinax_wiki")),
]
