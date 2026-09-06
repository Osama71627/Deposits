from django.db import models
from django.conf import settings
from apps.common.models import BaseModel

class Vehicle(BaseModel):
    VEHICLE_TYPES = [
        ('SCOOTER', 'Scooter'),
        ('BIKE', 'Bicycle'),
        ('CAR', 'Car'),
        ('VAN', 'Van'),
        ('TRUCK', 'Truck'),
    ]
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('MAINTENANCE', 'In Maintenance'),
        ('RETIRED', 'Retired'),
    ]
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    plate_number = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    color = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    assigned_courier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_vehicles')
    insurance_expiry = models.DateField(null=True, blank=True)
    registration_expiry = models.DateField(null=True, blank=True)
    last_maintenance_date = models.DateField(null=True, blank=True)
    next_maintenance_date = models.DateField(null=True, blank=True)
    mileage_km = models.IntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_vehicle_type_display()} - {self.plate_number}"

class GeofenceZone(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    radius_meters = models.IntegerField(default=500)
    is_active = models.BooleanField(default=True)
    event_name = models.CharField(max_length=255, blank=True, help_text='Event name like Riyadh Season, Boulevard City')
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Route(BaseModel):
    name = models.CharField(max_length=255)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, related_name='routes')
    courier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='routes')
    start_location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    start_location_lng = models.DecimalField(max_digits=9, decimal_places=6)
    end_location_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    end_location_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    total_distance_km = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=[
        ('PLANNED', 'Planned'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ], default='PLANNED')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

class LocationTracking(BaseModel):
    courier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='location_tracking')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    speed = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text='km/h')
    heading = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='degrees')
    accuracy = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text='meters')
    battery_level = models.IntegerField(null=True, blank=True)
    is_within_geofence = models.BooleanField(default=False)
    geofence_zone = models.ForeignKey(GeofenceZone, on_delete=models.SET_NULL, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['courier', '-created_at']),
        ]
