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

class OrderAdmin(admin.ModelAdmin):

    model = Order
    fieldsets = (('TITULO', {'fields': ('id', 'title', 'description',)}),
                 ('TIEMPO', {'fields': ('created_at', 'start_time', 'end_time', 'duration')}),
                 ('CLIENTE', {'fields': ('client', 'request_id',)}),
                 )
    readonly_fields = ['id', 'created_at', 'client', 'request_id']
    #list of fields to display in django admin
    list_display = ['title','created_at']

    #if you want django admin to show the search bar, just add this line
    #search_fields = ['created_at']

    inlines = (OriginItemInline, DestinationItemInline, PackageItemInline, OrderStatusInline,)

admin.site.register(Order, OrderAdmin)


