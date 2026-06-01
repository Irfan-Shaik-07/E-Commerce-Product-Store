from django.db import models
from django.contrib.auth.models import User

class NotificationManager(models.Manager):
    def create(self, **kwargs):
        user = kwargs.get('user')
        if user and user.is_authenticated:
            try:
                if not user.profile.notifications_enabled:
                    return None
            except Exception:
                pass
        return super().create(**kwargs)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = NotificationManager()

    def __str__(self):
        return f"{self.title} - {self.user.username if self.user else 'All users'}"
