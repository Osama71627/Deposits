from rest_framework import generics, filters
from .models import Asset, AssetCategory, AssetAssignment, MaintenanceRecord
from .serializers import AssetSerializer, AssetCategorySerializer, AssetAssignmentSerializer, MaintenanceRecordSerializer

class AssetCategoryListCreateView(generics.ListCreateAPIView):
    queryset = AssetCategory.objects.all()
    serializer_class = AssetCategorySerializer

class AssetListCreateView(generics.ListCreateAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    filterset_fields = ['status', 'category']
    search_fields = ['name', 'asset_tag', 'serial_number']

class AssetDetailView(generics.RetrieveUpdateAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

class AssetAssignmentListCreateView(generics.ListCreateAPIView):
    queryset = AssetAssignment.objects.all()
    serializer_class = AssetAssignmentSerializer

class MaintenanceRecordListCreateView(generics.ListCreateAPIView):
    queryset = MaintenanceRecord.objects.all()
    serializer_class = MaintenanceRecordSerializer
