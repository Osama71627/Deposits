from rest_framework import serializers
from .models import Vehicle, GeofenceZone, Route, LocationTracking

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class GeofenceZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeofenceZone
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class LocationTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationTracking
        fields = '__all__'
