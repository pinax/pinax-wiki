from .conf import settings


def binders_map():
    return {
        x.bind_to_model_name: x
        for x in settings.PINAX_WIKI_BINDERS
    }


def object_slug(wiki):
    if wiki:
        slug = wiki.content_type.model
    else:
        slug = "default"
    return slug
