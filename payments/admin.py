from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'transaction_id', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('transaction_id', 'order__name')
