from django.db import models
from django.conf import settings
from apps.common.models import BaseModel

class Warehouse(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.TextField()
    capacity = models.IntegerField(default=1000, help_text='Maximum items')
    current_occupancy = models.IntegerField(default=0)
    has_refrigeration = models.BooleanField(default=False)
    has_fragile_section = models.BooleanField(default=False)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='managed_warehouses')
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    operating_hours = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def occupancy_percentage(self):
        if self.capacity > 0:
            return (self.current_occupancy / self.capacity) * 100
        return 0

class Zone(BaseModel):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='zones')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    capacity = models.IntegerField(default=200)
    current_occupancy = models.IntegerField(default=0)
    zone_type = models.CharField(max_length=50, choices=[
        ('GENERAL', 'General'),
        ('FRAGILE', 'Fragile'),
        ('REFRIGERATED', 'Refrigerated'),
        ('HIGH_VALUE', 'High Value'),
        ('OVERSIZE', 'Oversize'),
    ], default='GENERAL')

    class Meta:
        unique_together = ['warehouse', 'code']

    def __str__(self):
        return f"{self.warehouse.code} - {self.name}"

class Shelf(BaseModel):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='shelves')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    capacity = models.IntegerField(default=20)
    current_occupancy = models.IntegerField(default=0)
    max_weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text='kg')

    class Meta:
        unique_together = ['zone', 'code']

    def __str__(self):
        return f"{self.zone.warehouse.code} - {self.zone.code} - Shelf {self.code}"

class Box(BaseModel):
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE, related_name='boxes')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    barcode = models.CharField(max_length=255, blank=True)
    capacity = models.IntegerField(default=5)
    current_occupancy = models.IntegerField(default=0)
    is_full = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)

    class Meta:
        unique_together = ['shelf', 'code']

    def __str__(self):
        return f"Box {self.code} ({self.shelf.zone.warehouse.code} - {self.shelf.zone.code} - {self.shelf.code})"

class StoredItem(BaseModel):
    storage_request = models.ForeignKey('customers.StorageRequest', on_delete=models.CASCADE, related_name='stored_items')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stored_items')
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, related_name='stored_items')
    shelf = models.ForeignKey(Shelf, on_delete=models.SET_NULL, null=True, related_name='stored_items')
    box = models.ForeignKey(Box, on_delete=models.SET_NULL, null=True, related_name='stored_items')
    item_name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255, blank=True)
    stored_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='stored_items')
    stored_at = models.DateTimeField(auto_now_add=True)
    retrieved_at = models.DateTimeField(null=True, blank=True)
    retrieved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='retrieved_items')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-stored_at']
        indexes = [
            models.Index(fields=['warehouse', 'zone', 'shelf', 'box']),
            models.Index(fields=['storage_request']),
        ]

    def __str__(self):
        return f"{self.item_name} @ {self.box}"

class InventoryAudit(BaseModel):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='audits')
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    audit_type = models.CharField(max_length=50, choices=[
        ('FULL', 'Full Audit'),
        ('SPOT', 'Spot Check'),
        ('CYCLE', 'Cycle Count'),
    ])
    status = models.CharField(max_length=20, choices=[
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('DISCREPANCY', 'Discrepancy Found'),
    ], default='IN_PROGRESS')
    notes = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

class InventoryAuditItem(BaseModel):
    audit = models.ForeignKey(InventoryAudit, on_delete=models.CASCADE, related_name='items')
    stored_item = models.ForeignKey(StoredItem, on_delete=models.CASCADE)
    expected_location = models.CharField(max_length=255)
    actual_location = models.CharField(max_length=255)
    is_found = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
