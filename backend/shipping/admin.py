from django.contrib import admin
from .models import ShippingAddress, ShippingZone


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'city', 'phone', 'is_default', 'created_at']
    list_filter = ['city', 'country', 'is_default']
    search_fields = ['user__username', 'full_name', 'phone', 'address']


@admin.register(ShippingZone)
class ShippingZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'shipping_fee', 'estimated_days', 'is_active']
    list_filter = ['is_active']
