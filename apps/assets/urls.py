from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.AssetCategoryListCreateView.as_view(), name='asset-category-list'),
    path('items/', views.AssetListCreateView.as_view(), name='asset-list'),
    path('items/<int:pk>/', views.AssetDetailView.as_view(), name='asset-detail'),
    path('assignments/', views.AssetAssignmentListCreateView.as_view(), name='asset-assignment-list'),
    path('maintenance/', views.MaintenanceRecordListCreateView.as_view(), name='maintenance-list'),
]
