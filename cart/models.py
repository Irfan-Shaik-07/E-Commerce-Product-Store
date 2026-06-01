from django.db import models
from django.contrib.auth.models import User
from homepage.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.user:
            return f"Cart of user {self.user.username}"
        return f"Guest Cart {self.session_id}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_price(self):
        return self.product.price * self.quantity
        
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
