from django.contrib import admin
from .models import ProductView

@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    list_display = ('product', 'view_count', 'last_viewed')
    search_fields = ('product__name',)
