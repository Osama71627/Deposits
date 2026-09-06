from rest_framework import generics, permissions, filters
from .models import Employee, AttendanceRecord, LeaveRequest, Payroll
from .serializers import EmployeeSerializer, AttendanceRecordSerializer, LeaveRequestSerializer, PayrollSerializer

class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    search_fields = ['user__username', 'employee_id']
    permission_classes = [permissions.IsAdminUser]

class EmployeeDetailView(generics.RetrieveUpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class AttendanceRecordListCreateView(generics.ListCreateAPIView):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    filterset_fields = ['employee', 'date', 'status']

class LeaveRequestListCreateView(generics.ListCreateAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    filterset_fields = ['status', 'leave_type']

class PayrollListCreateView(generics.ListCreateAPIView):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    filterset_fields = ['month', 'year', 'status']
