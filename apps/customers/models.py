from django.db import models
from django.conf import settings
from apps.common.models import BaseModel, Address

class CustomerProfile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_profile')
    loyalty_points = models.IntegerField(default=0)
    total_orders = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    preferred_payment_method = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Customer: {self.user.get_full_name()}"

class StorageRequest(BaseModel):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ASSIGNED', 'Assigned to Courier'),
        ('PICKUP_IN_PROGRESS', 'Pickup In Progress'),
        ('PICKED_UP', 'Picked Up'),
        ('IN_TRANSIT', 'In Transit'),
        ('STORED', 'Stored in Warehouse'),
        ('RETURN_IN_PROGRESS', 'Return In Progress'),
        ('RETURNED', 'Returned to Customer'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='storage_requests')
    courier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    pickup_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    pickup_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    pickup_address = models.TextField()
    dropoff_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    dropoff_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    dropoff_address = models.TextField(blank=True)
    description = models.TextField(blank=True)
    item_count = models.IntegerField(default=1)
    estimated_weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text='kg')
    is_geofence_valid = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True)
    qr_code_data = models.CharField(max_length=255, blank=True)
    pickup_code = models.CharField(max_length=10, blank=True)
    delivery_code = models.CharField(max_length=10, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    stored_at = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['courier', 'status']),
            models.Index(fields=['qr_code_data']),
        ]

    def __str__(self):
        return f"Request #{self.id} - {self.customer.username} - {self.get_status_display()}"

class StorageItem(BaseModel):
    storage_request = models.ForeignKey(StorageRequest, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    quantity = models.IntegerField(default=1)
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text='kg')
    is_fragile = models.BooleanField(default=False)
    requires_refrigeration = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='items/', blank=True)
    notes = models.TextField(blank=True)

class RequestStatusHistory(BaseModel):
    storage_request = models.ForeignKey(StorageRequest, on_delete=models.CASCADE, related_name='status_history')
    from_status = models.CharField(max_length=20)
    to_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Request Status Histories'
