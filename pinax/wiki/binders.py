from django.core.urlresolvers import reverse

from django.contrib.contenttypes.models import ContentType


class Binder(object):

    bind_to_model = None

    @property
    def bind_to_model_name(self):
        return self.bind_to_model._meta.model_name

    @property
    def index_url_name(self):
        return "{0}_pinax_wiki_index".format(self.bind_to_model_name)

    @property
    def page_url_name(self):
        return "{0}_pinax_wiki_page".format(self.bind_to_model_name)

    @property
    def edit_url_name(self):
        return "{0}_pinax_wiki_edit".format(self.bind_to_model_name)

    def get_object(self, **kwargs):
        return self.bind_to_model._default_manager.get(**{
            self.slug_name: kwargs.get(self.slug_name)
        })

    def lookup(self, *args, **kwargs):
        from .models import Wiki
        obj = self.get_object(**kwargs)
        return Wiki.objects.get(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk
        )


class DefaultBinder(Binder):

    @property
    def bind_to_model_name(self):
        return "default"

    @property
    def root(self):
        return r"^wiki"

    def lookup(self, *args, **kwargs):
        return None

    @property
    def index_url_name(self):
        return "pinax_wiki_index"

    @property
    def page_url_name(self):
        return "pinax_wiki_page"

    @property
    def edit_url_name(self):
        return "pinax_wiki_edit"

    def edit_url(self, wiki, slug):
        return reverse(self.edit_url_name, kwargs={"slug": slug})

    def page_url(self, wiki, slug):
        return reverse(self.page_url_name, kwargs={"slug": slug})

    def page_edit_url(self, wiki, slug):
        return reverse(self.edit_url_name, kwargs={"slug": slug})
