from django.db import models
from django.contrib.auth.models import User
from homepage.models import Product

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        if self.user:
            return f"Wishlist: {self.user.username} - {self.product.name}"
        return f"Wishlist: Guest {self.session_id} - {self.product.name}"
