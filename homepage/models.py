from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('mobiles', 'Mobiles'),
        ('fashion', 'Fashion'),
        ('electronics', 'Electronics'),
    ]
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.0)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
