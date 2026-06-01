from django.db import models

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.PositiveIntegerField()
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.code} ({self.discount_percentage}% Off)"
