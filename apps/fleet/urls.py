from django.urls import path
from . import views

urlpatterns = [
    path('vehicles/', views.VehicleListCreateView.as_view(), name='vehicle-list'),
    path('geofences/', views.GeofenceZoneListCreateView.as_view(), name='geofence-list'),
    path('routes/', views.RouteListCreateView.as_view(), name='route-list'),
    path('location/', views.LocationTrackingCreateView.as_view(), name='location-create'),
    path('location/<int:courier_id>/', views.CourierLocationListView.as_view(), name='courier-locations'),
]
