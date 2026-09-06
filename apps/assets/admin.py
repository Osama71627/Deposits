from django.contrib import admin
from .models import AssetCategory, Asset, AssetAssignment, MaintenanceRecord

@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'parent']
    search_fields = ['name', 'code']

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['name', 'asset_tag', 'category', 'status', 'assigned_to', 'current_value']
    list_filter = ['status', 'category']
    search_fields = ['name', 'asset_tag', 'serial_number']

@admin.register(AssetAssignment)
class AssetAssignmentAdmin(admin.ModelAdmin):
    list_display = ['asset', 'assigned_to', 'assigned_by', 'assigned_at', 'returned_at']

@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ['asset', 'maintenance_type', 'status', 'cost', 'started_at', 'completed_at']
