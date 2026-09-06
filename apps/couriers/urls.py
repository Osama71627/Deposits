from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.CourierProfileView.as_view(), name='courier-profile'),
    path('attendance/', views.AttendanceListCreateView.as_view(), name='attendance-list'),
    path('earnings/', views.CourierEarningsListView.as_view(), name='courier-earnings'),
    path('available/', views.AvailableCouriersView.as_view(), name='available-couriers'),
]
