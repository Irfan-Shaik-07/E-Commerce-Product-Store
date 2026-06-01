from django.db import models
from homepage.models import Product

class ProductView(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    view_count = models.PositiveIntegerField(default=0)
    last_viewed = models.DateTimeField(auto_now=True)
    
    @classmethod
    def track_view(cls, product):
        obj, created = cls.objects.get_or_create(product=product)
        obj.view_count += 1
        obj.save()

    def __str__(self):
        return f"{self.product.name} viewed {self.view_count} times"
