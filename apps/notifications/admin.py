from django.contrib import admin
from .models import Notification, PushDevice, EmailTemplate, SMSTemplate

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'notification_type', 'title', 'is_read', 'is_sent', 'created_at']
    list_filter = ['notification_type', 'is_read', 'is_sent']

@admin.register(PushDevice)
class PushDeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'platform', 'is_active']

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject']

@admin.register(SMSTemplate)
class SMSTemplateAdmin(admin.ModelAdmin):
    list_display = ['name']
