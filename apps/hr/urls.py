from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.EmployeeListCreateView.as_view(), name='employee-list'),
    path('employees/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('attendance/', views.AttendanceRecordListCreateView.as_view(), name='attendance-list'),
    path('leaves/', views.LeaveRequestListCreateView.as_view(), name='leave-list'),
    path('payroll/', views.PayrollListCreateView.as_view(), name='payroll-list'),
]
