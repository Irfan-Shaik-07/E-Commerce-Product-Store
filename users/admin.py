from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'notifications_enabled')
    list_filter = ('notifications_enabled',)
    search_fields = ('user__username', 'user__email')
