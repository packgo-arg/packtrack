from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Client, Provider, Package, Status, Driver, State


class DriverInline(admin.TabularInline):
    model = Driver
    icon_name = 'airline_seat_recline_normal'
    readonly_fields = ['id', 'created_at']
    extra = 1

    def get_status(self, obj):
        return obj.get_driver_display()


class ClientAdmin(admin.ModelAdmin):
    icon_name = 'mood'
    readonly_fields = ['id', 'created_at']
    list_display = ['client_name','created_at']


class ProvAdmin(admin.ModelAdmin):
    icon_name = 'drive_eta'
    readonly_fields = ['id', 'created_at']
    list_display = ['prov_name','id', 'created_at']

    inlines = (DriverInline,)


class PkgAdmin(admin.ModelAdmin):
    icon_name = 'mail_outline'
    readonly_fields = ['id', 'created_at']
    list_display = ['pkg_name','id','created_at']


class StatusAdmin(admin.ModelAdmin):
    icon_name = 'check_box'
    readonly_fields = ['id', 'created_at']
    list_display = ['status_name','id','status_desc','created_at']


class StateAdmin(admin.ModelAdmin):
    icon_name = 'emoji_transportation'
    readonly_fields = ['id', 'created_at']
    list_display = ['city', 'province', 'latitude', 'longitude', 'created_at']


admin.site.register(Client, ClientAdmin)
admin.site.register(Provider, ProvAdmin)
admin.site.register(Package, PkgAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(State, LeafletGeoAdmin)