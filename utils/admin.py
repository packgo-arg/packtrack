from django.contrib import admin
from tasks.lib.pg_library import jsonForApi
import requests
import os
from .models import *

class DriverInline(admin.TabularInline):
    model = Driver
    readonly_fields = ['id', 'created_at']
    extra = 1

    def get_status(self, obj):
        return obj.get_driver_display()

class ClientAdmin(admin.ModelAdmin):

    readonly_fields = ['id', 'created_at']
    list_display = ['client_name','created_at']

class ProvAdmin(admin.ModelAdmin):

    readonly_fields = ['id', 'created_at']
    list_display = ['prov_name','id', 'created_at']

    inlines = (DriverInline,)

class PkgAdmin(admin.ModelAdmin):

    readonly_fields = ['id', 'created_at']
    list_display = ['pkg_name','id','created_at']

class StatusAdmin(admin.ModelAdmin):

    readonly_fields = ['id', 'created_at']
    list_display = ['status_name','id','status_desc','created_at']

class StateAdmin(admin.ModelAdmin):

    readonly_fields = ['id', 'created_at']
    list_display = ['city', 'province', 'latitude', 'longitude', 'created_at']


admin.site.register(Client, ClientAdmin)
admin.site.register(Provider, ProvAdmin)
admin.site.register(Package, PkgAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(State, StateAdmin)