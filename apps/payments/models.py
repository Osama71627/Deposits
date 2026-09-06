from django.db import models
from django.conf import settings
from apps.common.models import BaseModel

class PaymentGateway(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    config = models.JSONField(default=dict, help_text='API keys and configuration')
    supported_currencies = models.JSONField(default=list)
    fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Payment(BaseModel):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
        ('CANCELLED', 'Cancelled'),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    storage_request = models.ForeignKey('customers.StorageRequest', on_delete=models.SET_NULL, null=True, blank=True)
    invoice = models.ForeignKey('accounting.Invoice', on_delete=models.SET_NULL, null=True, blank=True)
    gateway = models.ForeignKey(PaymentGateway, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='SAR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=255, blank=True)
    gateway_reference = models.CharField(max_length=255, blank=True)
    gateway_response = models.JSONField(default=dict, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment #{self.id} - {self.amount} {self.currency}"

class POSDevice(BaseModel):
    device_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=50)
    location = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    last_heartbeat = models.DateTimeField(null=True, blank=True)
    config = models.JSONField(default=dict, blank=True)
    assigned_warehouse = models.ForeignKey('warehouse.Warehouse', on_delete=models.SET_NULL, null=True, blank=True)

class POSTransaction(BaseModel):
    pos_device = models.ForeignKey(POSDevice, on_delete=models.CASCADE, related_name='transactions')
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='pos_transaction')
    receipt_number = models.CharField(max_length=100, unique=True)
    terminal_id = models.CharField(max_length=100, blank=True)
    card_type = models.CharField(max_length=50, blank=True)
    card_last_four = models.CharField(max_length=4, blank=True)
    approval_code = models.CharField(max_length=100, blank=True)
    pos_response = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('APPROVED', 'Approved'),
        ('DECLINED', 'Declined'),
        ('FAILED', 'Failed'),
        ('VOID', 'Void'),
    ])

class Refund(BaseModel):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='refunds')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField()
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    gateway_reference = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('PROCESSED', 'Processed'),
        ('FAILED', 'Failed'),
    ], default='PENDING')
    processed_at = models.DateTimeField(null=True, blank=True)
