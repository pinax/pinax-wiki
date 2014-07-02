from django.core.urlresolvers import reverse

from django.contrib.contenttypes.models import ContentType

from .models import Wiki


class Binder(object):

    bind_to_model = None

    @property
    def bind_to_model_name(self):
        return self.bind_to_model._meta.model_name

    @property
    def index_url_name(self):
        return "{0}_wiki_index".format(self.bind_to_model_name)

    @property
    def page_url_name(self):
        return "{0}_wiki_page".format(self.bind_to_model_name)

    @property
    def edit_url_name(self):
        return "{0}_wiki_edit".format(self.bind_to_model_name)

    def get_object(self, **kwargs):
        return self.bind_to_model._default_manager.get(**{
            self.slug_name: kwargs.get(self.slug_name)
        })

    def lookup(self, *args, **kwargs):
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
        return r""

    def lookup(self, *args, **kwargs):
        return None

    @property
    def index_url_name(self):
        return "wiki_index"

    @property
    def page_url_name(self):
        return "wiki_page"

    @property
    def edit_url_name(self):
        return "wiki_edit"

    def page_url(self, wiki, slug):
        return reverse("wiki_page", kwargs={"slug": slug})

    def page_edit_url(self, wiki, slug):
        return reverse("wiki_edit", kwargs={"slug": slug})
