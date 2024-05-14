from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from LostAndFound import settings
from items.models import Item, ItemFile


class History(LoginRequiredMixin, generic.ListView):
    template_name = "common_user/history.html"
    context_object_name = "items"

    def get_queryset(self):
        items = Item.objects.filter(user=self.request.user)
        for item in items:
            item.files = list(ItemFile.objects.filter(item=item.id))

        return items

    def get_context_data(self, **kwargs):
        context = super(History, self).get_context_data(**kwargs)
        context['s3_url'] = settings.AWS_S3_CUSTOM_DOMAIN
        return context
