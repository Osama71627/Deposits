from django.urls import path
from . import views

urlpatterns = [
    path('warehouses/', views.WarehouseListCreateView.as_view(), name='warehouse-list'),
    path('warehouses/<int:pk>/', views.WarehouseDetailView.as_view(), name='warehouse-detail'),
    path('zones/', views.ZoneListCreateView.as_view(), name='zone-list'),
    path('shelves/', views.ShelfListCreateView.as_view(), name='shelf-list'),
    path('boxes/', views.BoxListCreateView.as_view(), name='box-list'),
    path('stored-items/', views.StoredItemListCreateView.as_view(), name='stored-item-list'),
    path('find-item/<str:qr>/', views.FindItemView.as_view(), name='find-item'),
]
