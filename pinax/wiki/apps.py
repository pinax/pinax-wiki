import importlib

from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "pinax.wiki"
    label = "pinax_wiki"
    verbose_name = _("Pinax Wiki")

    def ready(self):
        importlib.import_module("pinax.wiki.receivers")
