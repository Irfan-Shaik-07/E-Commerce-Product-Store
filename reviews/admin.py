from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user_name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user_name', 'comment', 'product__name')
