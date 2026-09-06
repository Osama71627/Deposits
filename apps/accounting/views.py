from rest_framework import generics, permissions, filters
from .models import ChartOfAccount, JournalEntry, Invoice, Transaction, AccountReceivable, AccountPayable
from .serializers import ChartOfAccountSerializer, JournalEntrySerializer, InvoiceSerializer, TransactionSerializer, AccountReceivableSerializer, AccountPayableSerializer

class ChartOfAccountListCreateView(generics.ListCreateAPIView):
    queryset = ChartOfAccount.objects.all()
    serializer_class = ChartOfAccountSerializer
    filterset_fields = ['account_type', 'is_active']

class JournalEntryListCreateView(generics.ListCreateAPIView):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAdminUser]

class InvoiceListCreateView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    filterset_fields = ['status']
    search_fields = ['invoice_number']

class InvoiceDetailView(generics.RetrieveUpdateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_fields = ['transaction_type', 'payment_method', 'status']

class AccountReceivableListView(generics.ListAPIView):
    queryset = AccountReceivable.objects.all()
    serializer_class = AccountReceivableSerializer
    filterset_fields = ['status']

class AccountPayableListView(generics.ListAPIView):
    queryset = AccountPayable.objects.all()
    serializer_class = AccountPayableSerializer
    filterset_fields = ['status']
