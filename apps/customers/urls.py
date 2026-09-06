from django.urls import path
from . import views

urlpatterns = [
    path('requests/', views.StorageRequestListCreateView.as_view(), name='storage-request-list'),
    path('requests/<int:pk>/', views.StorageRequestDetailView.as_view(), name='storage-request-detail'),
    path('profile/', views.CustomerProfileView.as_view(), name='customer-profile'),
]
