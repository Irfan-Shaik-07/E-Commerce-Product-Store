from django.contrib import admin
from .models import ShippingInfo

@admin.register(ShippingInfo)
class ShippingInfoAdmin(admin.ModelAdmin):
    list_display = ('order', 'tracking_number', 'carrier', 'status', 'estimated_delivery')
    list_filter = ('status', 'carrier')
    search_fields = ('tracking_number', 'order__name')
