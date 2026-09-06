from django.contrib import admin
from .models import Vehicle, GeofenceZone, Route, LocationTracking

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['vehicle_type', 'plate_number', 'model', 'status', 'assigned_courier']
    list_filter = ['vehicle_type', 'status']

@admin.register(GeofenceZone)
class GeofenceZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_name', 'radius_meters', 'is_active', 'start_date', 'end_date']

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['name', 'vehicle', 'courier', 'status', 'started_at', 'completed_at']

@admin.register(LocationTracking)
class LocationTrackingAdmin(admin.ModelAdmin):
    list_display = ['courier', 'latitude', 'longitude', 'speed', 'is_within_geofence', 'created_at']
    list_filter = ['is_within_geofence']
