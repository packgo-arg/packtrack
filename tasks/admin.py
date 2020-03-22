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

class OrderAdmin(admin.ModelAdmin):

    readonly_fields = ['id', 'created_at']
    #list of fields to display in django admin
    list_display = ['title','created_at']

    #if you want django admin to show the search bar, just add this line
    #search_fields = ['created_at']

    inlines = (OriginItemInline, DestinationItemInline, PackageItemInline,)


admin.site.register(Order, OrderAdmin)


