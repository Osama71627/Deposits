from django.contrib import admin
from .models import ChartOfAccount, JournalEntry, JournalEntryLine, Invoice, InvoiceLine, Transaction, AccountReceivable, AccountPayable, ZATCAInvoice

@admin.register(ChartOfAccount)
class ChartOfAccountAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'account_type', 'balance', 'is_active']
    list_filter = ['account_type', 'is_active']
    search_fields = ['code', 'name']

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['entry_number', 'date', 'description', 'is_posted', 'total_debit', 'total_credit']

@admin.register(JournalEntryLine)
class JournalEntryLineAdmin(admin.ModelAdmin):
    list_display = ['journal_entry', 'account', 'debit', 'credit']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'customer', 'total_amount', 'vat_amount', 'status', 'issue_date']
    list_filter = ['status']
    search_fields = ['invoice_number', 'customer__username']

@admin.register(InvoiceLine)
class InvoiceLineAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'description', 'quantity', 'unit_price', 'line_total']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_type', 'amount', 'payment_method', 'settlement_status', 'created_at']

@admin.register(AccountReceivable)
class AccountReceivableAdmin(admin.ModelAdmin):
    list_display = ['customer', 'total_amount', 'paid_amount', 'due_date', 'status']

@admin.register(AccountPayable)
class AccountPayableAdmin(admin.ModelAdmin):
    list_display = ['vendor_name', 'total_amount', 'paid_amount', 'due_date', 'status']

@admin.register(ZATCAInvoice)
class ZATCAInvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'zatca_uuid', 'status', 'submitted_at']
