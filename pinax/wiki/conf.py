from __future__ import absolute_import

import importlib

from django.conf import settings  # noqa
from django.core.exceptions import ImproperlyConfigured

from appconf import AppConf


def load_path_attr(path):
    i = path.rfind(".")
    module, attr = path[:i], path[i + 1:]
    try:
        mod = importlib.import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured("Error importing {0}: '{1}'".format(module, e))
    try:
        attr = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured("Module '{0}' does not define a '{1}'".format(module, attr))
    return attr


class WikiAppConf(AppConf):

    BINDERS = [
        "pinax.wiki.binders.DefaultBinder"
    ]
    IP_ADDRESS_META_FIELD = "HTTP_X_FORWARDED_FOR"
    HOOKSET = "pinax.wiki.hooks.WikiDefaultHookset"
    PARSE = "pinax.wiki.parsers.creole_parse"

    class Meta:
        prefix = "pinax_wiki"

    def configure_binders(self, value):
        binders = []
        for val in value:
            binders.append(load_path_attr(val)())
        return binders

    def configure_hookset(self, value):
        return load_path_attr(value)()

    def configure_parse(self, value):
        return load_path_attr(value)
