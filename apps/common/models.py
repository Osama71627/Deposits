from django.db import models
from django.utils import timezone
import uuid

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UUIDModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True

class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True

class BaseModel(TimeStampedModel, UUIDModel, SoftDeleteModel):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.uuid)

class Address(models.Model):
    ADDRESS_TYPES = [
        ('HOME', 'Home'),
        ('WORK', 'Work'),
        ('OTHER', 'Other'),
    ]
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='HOME')
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='Saudi Arabia')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        abstract = True

class Media(BaseModel):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    original_filename = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=100)
    file_size = models.BigIntegerField(default=0)

    class Meta:
        verbose_name = 'Media'
        verbose_name_plural = 'Media'
