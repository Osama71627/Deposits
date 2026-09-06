from rest_framework import generics, permissions, filters
from .models import Vehicle, GeofenceZone, Route, LocationTracking
from .serializers import VehicleSerializer, GeofenceZoneSerializer, RouteSerializer, LocationTrackingSerializer

class VehicleListCreateView(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filterset_fields = ['vehicle_type', 'status']

class GeofenceZoneListCreateView(generics.ListCreateAPIView):
    queryset = GeofenceZone.objects.filter(is_active=True)
    serializer_class = GeofenceZoneSerializer

class RouteListCreateView(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

class LocationTrackingCreateView(generics.CreateAPIView):
    queryset = LocationTracking.objects.all()
    serializer_class = LocationTrackingSerializer

    def perform_create(self, serializer):
        serializer.save(courier=self.request.user)

class CourierLocationListView(generics.ListAPIView):
    serializer_class = LocationTrackingSerializer

    def get_queryset(self):
        return LocationTracking.objects.filter(courier_id=self.kwargs['courier_id'])[:100]
