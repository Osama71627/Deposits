from rest_framework import serializers
from .models import Warehouse, Zone, Shelf, Box, StoredItem

class WarehouseSerializer(serializers.ModelSerializer):
    occupancy_percentage = serializers.ReadOnlyField()

    class Meta:
        model = Warehouse
        fields = '__all__'

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'

class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelf
        fields = '__all__'

class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = '__all__'

class StoredItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoredItem
        fields = '__all__'
