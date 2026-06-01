from django.db import models
from orders.models import Order

class ShippingInfo(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping_info')
    tracking_number = models.CharField(max_length=100, unique=True)
    carrier = models.CharField(max_length=50, default='ShopNova Express')
    status = models.CharField(max_length=100, default='In Transit')
    estimated_delivery = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Shipping Info for Order #{self.order.id} - Tracking: {self.tracking_number}"
