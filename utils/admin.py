from django.contrib import admin
from .models import *

class ClientAdmin(admin.ModelAdmin):

    readonly_fields = ['id', 'created_at']
    list_display = ['client_name','created_at']

class ProvAdmin(admin.ModelAdmin):

    readonly_fields = ['id', 'created_at']
    list_display = ['prov_name','created_at']

class PkgAdmin(admin.ModelAdmin):

    readonly_fields = ['id', 'created_at']
    list_display = ['pkg_name','created_at']


admin.site.register(Client, ClientAdmin)
admin.site.register(Provider, ProvAdmin)
admin.site.register(Package, PkgAdmin)