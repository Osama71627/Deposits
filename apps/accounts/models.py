from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from apps.common.models import TimeStampedModel

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    permissions = models.JSONField(default=dict)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class User(AbstractUser, TimeStampedModel):
    USER_TYPES = [
        ('ADMIN', 'Administrator'),
        ('CUSTOMER', 'Customer'),
        ('COURIER', 'Courier'),
        ('WAREHOUSE', 'Warehouse Employee'),
        ('MANAGER', 'Manager'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('SUSPENDED', 'Suspended'),
        ('BANNED', 'Banned'),
    ]

    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='CUSTOMER')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    phone = PhoneNumberField(unique=True, null=True, blank=True, region='SA')
    national_id = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    last_activity = models.DateTimeField(null=True, blank=True)
    fcm_token = models.TextField(blank=True)
    roles = models.ManyToManyField(Role, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_user_type_display()})"

class UserDevice(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    device_id = models.CharField(max_length=255)
    device_type = models.CharField(max_length=50)
    fcm_token = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['user', 'device_id']

class UserSession(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']

class AuditLog(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    entity_type = models.CharField(max_length=100)
    entity_id = models.CharField(max_length=100, blank=True)
    details = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'action']),
            models.Index(fields=['entity_type', 'entity_id']),
        ]
