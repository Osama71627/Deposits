from django.contrib import admin
from .models import PaymentGateway, Payment, POSDevice, POSTransaction, Refund

@admin.register(PaymentGateway)
class PaymentGatewayAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active', 'fee_percentage']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['customer', 'amount', 'currency', 'status', 'payment_method', 'paid_at']
    list_filter = ['status', 'payment_method']

@admin.register(POSDevice)
class POSDeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'device_type', 'is_active', 'last_heartbeat']

@admin.register(POSTransaction)
class POSTransactionAdmin(admin.ModelAdmin):
    list_display = ['pos_device', 'payment', 'receipt_number', 'card_type', 'status']

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['payment', 'amount', 'reason', 'status', 'processed_at']
