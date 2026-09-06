from rest_framework import serializers
from .models import CustomerProfile, StorageRequest, StorageItem, RequestStatusHistory

class StorageItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageItem
        fields = '__all__'

class StorageRequestSerializer(serializers.ModelSerializer):
    items = StorageItemSerializer(many=True, read_only=True)

    class Meta:
        model = StorageRequest
        fields = '__all__'
        read_only_fields = ['id', 'customer', 'qr_code', 'qr_code_data', 'pickup_code', 'delivery_code', 'total_amount', 'vat_amount', 'grand_total', 'is_paid', 'paid_at', 'picked_up_at', 'stored_at', 'returned_at', 'completed_at', 'cancelled_at', 'created_at', 'updated_at']

class CreateStorageRequestSerializer(serializers.ModelSerializer):
    items = StorageItemSerializer(many=True)

    class Meta:
        model = StorageRequest
        fields = ['pickup_latitude', 'pickup_longitude', 'pickup_address', 'description', 'item_count', 'estimated_weight', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        request = StorageRequest.objects.create(**validated_data)
        for item_data in items_data:
            StorageItem.objects.create(storage_request=request, **item_data)
        return request

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = '__all__'
