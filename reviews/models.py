from django.db import models
from homepage.models import Product

class Review(models.Model):
    user_name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review ({self.rating}/5) for {self.product.name} by {self.user_name}"
