from django.db import models
from django.conf import settings
from apps.common.models import BaseModel

class Notification(BaseModel):
    NOTIFICATION_TYPES = [
        ('ORDER_STATUS', 'Order Status Update'),
        ('ASSIGNMENT', 'New Assignment'),
        ('PAYMENT', 'Payment Update'),
        ('SYSTEM', 'System Notification'),
        ('PROMOTION', 'Promotional'),
        ('ALERT', 'Alert'),
    ]

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    body = models.TextField()
    data = models.JSONField(default=dict, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    deep_link = models.CharField(max_length=500, blank=True)
    image_url = models.URLField(blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
        ]

    def __str__(self):
        return f"{self.notification_type} - {self.title}"

class PushDevice(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='push_devices')
    device_id = models.CharField(max_length=255)
    platform = models.CharField(max_length=20, choices=[
        ('ANDROID', 'Android'),
        ('IOS', 'iOS'),
        ('WEB', 'Web'),
    ])
    fcm_token = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['user', 'device_id']

class EmailTemplate(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    subject = models.CharField(max_length=255)
    template_body = models.TextField()
    variables = models.JSONField(default=list, help_text='List of available variables')

class SMSTemplate(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    template_body = models.TextField()
    variables = models.JSONField(default=list)
