from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role, UserDevice, UserSession, AuditLog

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'user_type', 'status', 'is_verified', 'is_online', 'last_activity']
    list_filter = ['user_type', 'status', 'is_verified', 'is_online']
    search_fields = ['username', 'email', 'phone', 'national_id']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'status', 'phone', 'national_id', 'avatar', 'date_of_birth', 'is_verified', 'is_online', 'last_activity', 'fcm_token', 'roles', 'metadata')}),
    )

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']

@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'device_type', 'is_active', 'created_at']

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_active', 'ip_address', 'created_at']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'entity_type', 'entity_id', 'created_at']
    list_filter = ['action', 'entity_type']
    search_fields = ['user__username', 'action', 'entity_id']
