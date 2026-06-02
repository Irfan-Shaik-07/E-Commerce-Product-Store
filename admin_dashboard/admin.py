from django.contrib import admin
from .models import AdminActivityLog

@admin.register(AdminActivityLog)
class AdminActivityLogAdmin(admin.ModelAdmin):
    list_display = ('action_type', 'action_details', 'user', 'timestamp')
    list_filter = ('action_type', 'timestamp')
    search_fields = ('action_details', 'user__username')
    readonly_fields = ('timestamp',)
