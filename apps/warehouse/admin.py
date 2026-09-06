from django.contrib import admin
from .models import Warehouse, Zone, Shelf, Box, StoredItem, InventoryAudit, InventoryAuditItem

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'capacity', 'current_occupancy', 'occupancy_percentage']
    search_fields = ['name', 'code']

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['warehouse', 'name', 'code', 'zone_type', 'capacity', 'current_occupancy']

@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ['zone', 'name', 'code', 'capacity', 'current_occupancy']

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ['shelf', 'name', 'code', 'capacity', 'current_occupancy', 'is_full']

@admin.register(StoredItem)
class StoredItemAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'warehouse', 'zone', 'shelf', 'box', 'stored_at', 'retrieved_at']
    list_filter = ['warehouse', 'zone']
    search_fields = ['item_name', 'storage_request__id']

@admin.register(InventoryAudit)
class InventoryAuditAdmin(admin.ModelAdmin):
    list_display = ['warehouse', 'audit_type', 'status', 'performed_by', 'completed_at']

@admin.register(InventoryAuditItem)
class InventoryAuditItemAdmin(admin.ModelAdmin):
    list_display = ['audit', 'stored_item', 'is_found']
