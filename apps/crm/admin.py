from django.contrib import admin
from .models import CustomerSegment, SupportTicket, TicketMessage, CustomerFeedback, CustomerComplaint

@admin.register(CustomerSegment)
class CustomerSegmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'subject', 'priority', 'status', 'assigned_to', 'created_at']
    list_filter = ['priority', 'status']

@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'sender', 'created_at']

@admin.register(CustomerFeedback)
class CustomerFeedbackAdmin(admin.ModelAdmin):
    list_display = ['customer', 'storage_request', 'rating', 'created_at']

@admin.register(CustomerComplaint)
class CustomerComplaintAdmin(admin.ModelAdmin):
    list_display = ['customer', 'subject', 'status', 'created_at']
