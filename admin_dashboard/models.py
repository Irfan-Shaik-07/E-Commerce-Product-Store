from django.db import models
from django.contrib.auth.models import User

class AdminActivityLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]
    action_type = models.CharField(max_length=10, choices=ACTION_CHOICES)
    action_details = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else 'System/Anonymous'
        return f"{self.action_type} - {username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
