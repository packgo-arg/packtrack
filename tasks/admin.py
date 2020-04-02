from django.contrib import admin

from .models import *
from utils.models import *

class OriginItemInline(admin.TabularInline):
    model = Origin
    extra = 1

class DestinationItemInline(admin.TabularInline):
    model = Destination
    extra = 1

class PackageItemInline(admin.TabularInline):
    model = OrderPackage
    extra = 1

class OrderStatusInline(admin.TabularInline):
    model = OrderStatus
    readonly_fields = ['st_update']
    extra = 1

    def get_status(self, obj):
        return obj.get_status_display()


class OrderAdmin(admin.ModelAdmin):

    model = Order
    fieldsets = (('TITULO', {
                    'fields': ('id', 'title', 'description')
                    }),
                 ('CLIENTE', {
                     'fields': (('client', 'request_id'),)
                 }),
                 ('TIEMPO', {
                     'fields': ('created_at', ('start_time', 'end_time'), 'duration')
                 }),
                 )
    readonly_fields = ['id', 'created_at', 'client', 'request_id']

    #list of fields to display in django admin
    list_display = ('title','created_at', 'client')

    #if you want django admin to show the search bar, just add this line
    #search_fields = ('client','created_at')
    filter_horizontal = ()
    list_filter = ('client','created_at')
    # inlines
    inlines = (OriginItemInline, DestinationItemInline, PackageItemInline, OrderStatusInline,)


admin.site.register(Order, OrderAdmin)


