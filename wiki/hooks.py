from .conf import settings


class WikiDefaultHookset(object):

    def can_create_page(self, wiki, user):
        return False

    def can_edit_page(self, page, user):
        return False

    def can_delete_page(self, page, user):
        return False

    def can_view_page(self, page, user):
        return False

    def page_url(self, wiki, slug):
        return "/"

    def page_edit_url(self, wiki, slug):
        return "/"


class HookProxy(object):

    def __getattr__(self, attr):
        return getattr(settings.WIKI_HOOKSET, attr)


hookset = HookProxy()
