import json

from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views import static
from django.views.decorators.http import require_POST

from .conf import settings
from .forms import RevisionForm
from .hooks import hookset
from .models import MediaFile, Page

try:
    from account.decorators import login_required
except ImportError:
    from django.contrib.auth.decorators import login_required


def index(request, binder, *args, **kwargs):
    wiki = binder.lookup(*args, **kwargs)
    return redirect(binder.page_url(wiki, "WikiIndex"))


def page(request, slug, binder, *args, **kwargs):
    wiki = binder.lookup(*args, **kwargs)
    try:
        if wiki:
            page = wiki.pages.get(slug=slug)
        else:
            page = Page.objects.get(slug=slug)
        if not hookset.can_view_page(page, request.user):
            raise Http404()
        rev = page.revisions.latest()
        return render(request, "pinax/wiki/page.html", {"revision": rev, "can_edit": hookset.can_edit_page(page, request.user)})
    except Page.DoesNotExist:
        return redirect(binder.edit_url(wiki, slug))


@login_required
def edit(request, slug, binder, *args, **kwargs):
    wiki = binder.lookup(*args, **kwargs)
    try:
        if wiki:
            page = wiki.pages.get(slug=slug)
        else:
            page = Page.objects.get(slug=slug)
        rev = page.revisions.latest()
        if not hookset.can_edit_page(page, request.user):
            return HttpResponseForbidden()
    except Page.DoesNotExist:
        page = Page(wiki=wiki, slug=slug)
        rev = None
        if not hookset.can_edit_page(page, request.user):
            raise Http404()
    if request.method == "POST":
        form = RevisionForm(request.POST, revision=rev)
        if form.is_valid():
            if page.pk is None:
                page.save()
            revision = form.save(commit=False)
            revision.page = page
            revision.created_by = request.user
            revision.created_ip = request.META.get(settings.PINAX_WIKI_IP_ADDRESS_META_FIELD, "REMOTE_ADDR")
            revision.parse()
            revision.save()
            return redirect(binder.page_url(wiki, slug))
    else:
        form = RevisionForm(revision=rev)

    return render(request, "pinax/wiki/edit.html", {
        "form": form,
        "page": page,
        "revision": rev,
        "can_delete": hookset.can_delete_page(page, request.user)
    })


def file_download(request, pk, filename):
    media_file = get_object_or_404(MediaFile, pk=pk, filename=filename)
    if getattr(settings, "DOCUMENTS_USE_X_ACCEL_REDIRECT", False):
        response = HttpResponse()
        response["X-Accel-Redirect"] = media_file.file.url
        # delete content-type to allow Gondor to determine the filetype and
        # we definitely don't want Django's crappy default :-)
        del response["content-type"]
    else:
        response = static.serve(request, media_file.file.name, document_root=settings.MEDIA_ROOT)
    return response


@require_POST
@login_required
def file_upload(request):
    uploads = []
    for f in request.FILES.getlist("files"):
        media_file = request.user.media_files.create(file=f, filename=f.name)
        uploads.append(media_file)
    return HttpResponse(json.dumps({
        "uploads": [
            {"filename": m.filename, "download_url": m.download_url()}
            for m in uploads
        ]
    }), content_type="application/json")
