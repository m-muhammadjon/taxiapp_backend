from django.contrib import admin
from django.contrib.gis import admin as geo_admin

from .models import Car, Driver, Order, Location, CarType, OrderNotificationDriver


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    pass


@admin.register(Driver)
class DriverAdmin(geo_admin.OSMGeoAdmin):
    list_display = ('user', 'car', 'type', 'plate_number', 'last_location')
    list_filter = ('car',)


admin.site.register(CarType)
admin.site.register(OrderNotificationDriver)


@admin.register(Order)
class OrderAdmin(geo_admin.OSMGeoAdmin):
    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass
