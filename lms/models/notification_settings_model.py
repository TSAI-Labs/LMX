from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class NotificationSetting(models.Model):
    """
    Model to capture the flag details of notification categories.
    """
    NOTIFICATION_CHOICES = [
        ('IMMEDIATE', 'Notify Immediately'),
        ('DAILY', 'Daily Summary'),
        ('WEEK', 'Weekly Summary'),
        ('OFF', 'Notification Off'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    due_date = models.CharField(max_length=32, choices=NOTIFICATION_CHOICES, default='OFF')
    grading_policies = models.CharField(max_length=32, choices=NOTIFICATION_CHOICES, default='OFF')
    course_content = models.CharField(max_length=32, choices=NOTIFICATION_CHOICES, default='OFF')
    files = models.CharField(max_length=32, choices=NOTIFICATION_CHOICES, default='OFF')
    announcement = models.CharField(max_length=32, choices=NOTIFICATION_CHOICES, default='OFF')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
