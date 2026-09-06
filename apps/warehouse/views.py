from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Warehouse, Zone, Shelf, Box, StoredItem
from .serializers import WarehouseSerializer, ZoneSerializer, ShelfSerializer, BoxSerializer, StoredItemSerializer

class WarehouseListCreateView(generics.ListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code']

class WarehouseDetailView(generics.RetrieveUpdateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class ZoneListCreateView(generics.ListCreateAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    filterset_fields = ['warehouse', 'zone_type']

class ShelfListCreateView(generics.ListCreateAPIView):
    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer
    filterset_fields = ['zone']

class BoxListCreateView(generics.ListCreateAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    filterset_fields = ['shelf', 'is_full']

class StoredItemListCreateView(generics.ListCreateAPIView):
    queryset = StoredItem.objects.all()
    serializer_class = StoredItemSerializer
    filterset_fields = ['warehouse', 'zone', 'shelf', 'box']
    search_fields = ['item_name', 'storage_request__id']

class FindItemView(generics.RetrieveAPIView):
    queryset = StoredItem.objects.all()
    serializer_class = StoredItemSerializer
    lookup_field = 'storage_request__qr_code_data'
