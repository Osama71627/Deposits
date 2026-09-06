from rest_framework import serializers
from .models import ChartOfAccount, JournalEntry, JournalEntryLine, Invoice, InvoiceLine, Transaction, AccountReceivable, AccountPayable

class ChartOfAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartOfAccount
        fields = '__all__'

class JournalEntrySerializer(serializers.ModelSerializer):
    lines = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = JournalEntry
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class AccountReceivableSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountReceivable
        fields = '__all__'

class AccountPayableSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountPayable
        fields = '__all__'
