from django.db import models
from orders.models import Order

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='Success')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.status}"
