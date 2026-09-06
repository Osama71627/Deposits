from django.db import models
from django.conf import settings
from apps.common.models import BaseModel

class AssetCategory(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name_plural = 'Asset Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

class Asset(BaseModel):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('ASSIGNED', 'Assigned'),
        ('IN_MAINTENANCE', 'In Maintenance'),
        ('LOST', 'Lost'),
        ('DAMAGED', 'Damaged'),
        ('RETIRED', 'Retired'),
    ]

    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE, related_name='assets')
    name = models.CharField(max_length=255)
    asset_tag = models.CharField(max_length=100, unique=True, help_text='Company asset tag number')
    serial_number = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_assets')
    assigned_at = models.DateTimeField(null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    warranty_expiry = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='assets/', blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.asset_tag})"

class AssetAssignment(BaseModel):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='assignments')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='asset_assignments')
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='issued_assets')
    assigned_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    condition_at_assignment = models.TextField(blank=True)
    condition_at_return = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-assigned_at']

class MaintenanceRecord(BaseModel):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='maintenance_records')
    maintenance_type = models.CharField(max_length=50, choices=[
        ('ROUTINE', 'Routine'),
        ('REPAIR', 'Repair'),
        ('EMERGENCY', 'Emergency'),
    ])
    description = models.TextField()
    performed_by = models.CharField(max_length=255, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ], default='PENDING')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-started_at']
