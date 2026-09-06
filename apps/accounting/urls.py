from django.urls import path
from . import views

urlpatterns = [
    path('chart-of-accounts/', views.ChartOfAccountListCreateView.as_view(), name='chart-of-accounts'),
    path('journal-entries/', views.JournalEntryListCreateView.as_view(), name='journal-entries'),
    path('invoices/', views.InvoiceListCreateView.as_view(), name='invoice-list'),
    path('invoices/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice-detail'),
    path('transactions/', views.TransactionListCreateView.as_view(), name='transaction-list'),
    path('receivables/', views.AccountReceivableListView.as_view(), name='receivable-list'),
    path('payables/', views.AccountPayableListView.as_view(), name='payable-list'),
]
