from django.contrib import admin
from .models import CustomerProfile, StorageRequest, StorageItem, RequestStatusHistory

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'loyalty_points', 'total_orders', 'total_spent']
    search_fields = ['user__username', 'user__email']

@admin.register(StorageRequest)
class StorageRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'courier', 'status', 'grand_total', 'is_paid', 'created_at']
    list_filter = ['status', 'is_paid', 'is_geofence_valid']
    search_fields = ['customer__username', 'pickup_address', 'qr_code_data']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(StorageItem)
class StorageItemAdmin(admin.ModelAdmin):
    list_display = ['storage_request', 'name', 'quantity', 'is_fragile']

@admin.register(RequestStatusHistory)
class RequestStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['storage_request', 'from_status', 'to_status', 'changed_by', 'created_at']
