from django.db import models
from django.conf import settings
from apps.common.models import BaseModel

class ChartOfAccount(BaseModel):
    ACCOUNT_TYPES = [
        ('ASSET', 'Asset'),
        ('LIABILITY', 'Liability'),
        ('EQUITY', 'Equity'),
        ('REVENUE', 'Revenue'),
        ('EXPENSE', 'Expense'),
    ]

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255, blank=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='SAR')
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"

class JournalEntry(BaseModel):
    entry_number = models.CharField(max_length=50, unique=True)
    date = models.DateField()
    description = models.TextField()
    reference_number = models.CharField(max_length=100, blank=True)
    reference_type = models.CharField(max_length=50, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    is_posted = models.BooleanField(default=False)
    posted_at = models.DateTimeField(null=True, blank=True)
    total_debit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_credit = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name_plural = 'Journal Entries'

class JournalEntryLine(BaseModel):
    journal_entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name='lines')
    account = models.ForeignKey(ChartOfAccount, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    debit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=15, decimal_places=2, default=0)

class Invoice(BaseModel):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('ISSUED', 'Issued'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
    ]

    invoice_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invoices')
    storage_request = models.ForeignKey('customers.StorageRequest', on_delete=models.SET_NULL, null=True, blank=True)
    issue_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    vat_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=15)
    vat_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    zatca_qr = models.TextField(blank=True, help_text='ZATCA E-Invoicing QR code')
    zatca_uuid = models.CharField(max_length=100, blank=True)
    zatca_status = models.CharField(max_length=50, blank=True)
    pdf_file = models.FileField(upload_to='invoices/', blank=True)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return f"Invoice #{self.invoice_number}"

class InvoiceLine(BaseModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='lines')
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=15)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)

class Transaction(BaseModel):
    transaction_type = models.CharField(max_length=50, choices=[
        ('SALE', 'Sale'),
        ('REFUND', 'Refund'),
        ('PAYMENT', 'Payment'),
        ('TRANSFER', 'Transfer'),
        ('ADJUSTMENT', 'Adjustment'),
    ])
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    reference_number = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='transactions')
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='processed_transactions')
    settlement_status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('SETTLED', 'Settled'),
        ('FAILED', 'Failed'),
    ], default='PENDING')
    settled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

class AccountReceivable(BaseModel):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receivables')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='receivables')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('PARTIAL', 'Partially Paid'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
        ('WRITTEN_OFF', 'Written Off'),
    ], default='PENDING')

class AccountPayable(BaseModel):
    vendor_name = models.CharField(max_length=255)
    description = models.TextField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('PARTIAL', 'Partially Paid'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
    ], default='PENDING')

class ZATCAInvoice(BaseModel):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, related_name='zatca')
    zatca_uuid = models.CharField(max_length=100, unique=True)
    xml_content = models.TextField()
    qr_code = models.TextField()
    signed_xml = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('SUBMITTED', 'Submitted'),
        ('CLEARED', 'Cleared'),
        ('REPORTED', 'Reported'),
        ('FAILED', 'Failed'),
    ], default='PENDING')
    submitted_at = models.DateTimeField(null=True, blank=True)
    cleared_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
