from django.contrib import admin
from .models import Wishlist

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_id', 'product', 'created_at')
    search_fields = ('product__name', 'session_id')
