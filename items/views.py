from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.conf import settings

import json

from .forms import ItemForm
from .models import Item, Status, ItemFile, Location, Location_Category


class ReportItemView(generic.CreateView):
    form_class = ItemForm
    template_name = "items/report.html"
    success_url = reverse_lazy('items:report_success')
    is_found = None

    # Used to get the current user in ItemForm.__init__()
    def get_form_kwargs(self):
        kwargs = super(ReportItemView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user, 'is_found': self.is_found})
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not self.is_found:
            return HttpResponseRedirect(settings.LOGIN_URL)

        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()

        if self.request.user.is_authenticated:
            initial['email'] = self.request.user.email

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_found'] = self.is_found
        return context
    
    


class Index(LoginRequiredMixin, generic.ListView):
    template_name = "items/index.html"
    context_object_name = "items"
    is_found = None

    def get_queryset(self):
        # Filter the queryset based on is_found
        items = Item.objects.filter(is_found=self.is_found, status__in=[Status.RESOLVED])
        for item in items:
            item.files = list(ItemFile.objects.filter(item=item.id))

        return items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_found'] = self.is_found
        return context


class Detail(LoginRequiredMixin, generic.DetailView):
    model = Item
    template_name = "items/details.html"
    context_object_name = "item"

    def get_object(self, queryset=None):
        item = Item.objects.get(id=self.kwargs['id'])
        item.files = list(ItemFile.objects.filter(item=item.id))

        return item

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)
        context["can_flag"] = context['item'].status is not Status.FLAGGED or Status.IN_PROGRESS
        context['s3_url'] = settings.AWS_S3_CUSTOM_DOMAIN
        return context


@login_required
def delete(request, id):
    item = get_object_or_404(Item, pk=id)

    # Check if the logged-in user is the owner of the item
    if request.user is None or item.user != request.user:
        return HttpResponseForbidden('You are not allowed to delete this post.')

    if request.method == 'POST':
        if item.is_found:
            return_url = 'items:index_found'
        else:
            return_url = 'items:index_lost'

        item.delete()

        return HttpResponseRedirect(reverse(return_url))  # Redirect to the list view after deletion

    return HttpResponse(reverse("items:details", args=(id,)))


@login_required
def flag(request, id):
    item = get_object_or_404(Item, pk=id)

    if request.user is None:
        return HttpResponseForbidden('You are not allowed to flag this post.')

    if request.method == 'POST':
        item.status = Status.FLAGGED
        item.save(update_fields=['status'])
        return HttpResponseRedirect(reverse('items:index_lost'))

    return HttpResponse(reverse('items:details', args=(id,)))

def getLocations(request):
        data = json.loads(request.body)

        location_categoryID = data["id"]

        possibleLocations = Location.objects.filter(category__id = location_categoryID)

        print(location_categoryID)

        return JsonResponse(list(possibleLocations.values("id", "name")), safe = False)
