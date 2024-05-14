from django.contrib import admin
from .models import Item, ItemFile, Location


class FileInLine(admin.TabularInline):
    model = ItemFile
    extra = 0


class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'user', 'status', 'tag')
    list_filter = ('user', 'status', 'tag')
    date_hierarchy = 'date'
    search_fields = ('item_name', )

    inlines = [FileInLine]

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')

admin.site.register(Item, ItemAdmin)
admin.site.register(Location, LocationAdmin)
