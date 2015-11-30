import pkg_resources


default_app_config = "pinax.wiki.apps.AppConfig"
__version__ = pkg_resources.get_distribution("pinax-wiki").version
