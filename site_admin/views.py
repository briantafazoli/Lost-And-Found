from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.views import generic

from items.models import Item, Status, ItemFile


class ReviewItems(LoginRequiredMixin, generic.ListView):
    template_name = "site_admin/review.html"
    context_object_name = "items"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_site_admin:
            return HttpResponseForbidden("You are not allowed to access this page.")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        items = Item.objects.filter(status__in=[Status.NEW, Status.FLAGGED, Status.IN_PROGRESS])

        for item in items:
            item.files = list(ItemFile.objects.filter(item=item.id))

        return items


class Detail(LoginRequiredMixin, generic.DetailView):
    model = Item
    template_name = "site_admin/detail.html"
    context_object_name = "item"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_site_admin:
            return HttpResponseForbidden("You are not allowed to access this page.")

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        item = Item.objects.get(id=self.kwargs['id'], status__in=[Status.NEW, Status.FLAGGED, Status.IN_PROGRESS])
        item.files = list(ItemFile.objects.filter(item=item.id))

        if item.status in [Status.NEW, Status.FLAGGED]:
            item.status = Status.IN_PROGRESS
            item.save(update_fields=['status'])

        return item


class Resolve(LoginRequiredMixin, generic.DetailView):
    model = Item
    template_name = "site_admin/resolution_notes.html"
    context_object_name = "item"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_site_admin:
            return HttpResponseForbidden("You are not allowed to access this page.")

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        item = Item.objects.get(id=self.kwargs['id'], status__in=[Status.NEW, Status.FLAGGED, Status.IN_PROGRESS])
        # item.files = list(ItemFile.objects.filter(item=item.id))

        return item


def update(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(settings.LOGIN_URL)
    if not request.user.is_site_admin:
        return HttpResponseForbidden("You are not allowed to access this page.")

    item = get_object_or_404(Item, pk=id, status__in=[Status.NEW, Status.FLAGGED, Status.IN_PROGRESS])

    if request.method == "POST":
        item.status = Status.RESOLVED
        item.resolve_text = request.POST.get("resolve_text", "")
        item.save()

        return HttpResponseRedirect(reverse('site_admin:review'))

    else:
        return HttpResponse(reverse('site_admin:detail'))


def review_redirect(request):
    return HttpResponseRedirect(reverse('site_admin:review'))
