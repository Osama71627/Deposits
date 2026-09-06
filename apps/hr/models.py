from django.db import models
from django.conf import settings
from apps.common.models import BaseModel

class Department(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_departments')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Employee(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='employees')
    job_title = models.CharField(max_length=255)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    bank_account = models.CharField(max_length=50, blank=True)
    emergency_contact = models.CharField(max_length=20, blank=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    health_insurance = models.CharField(max_length=255, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    passport_number = models.CharField(max_length=50, blank=True)
    iqama_number = models.CharField(max_length=50, blank=True)
    iqama_expiry = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"

class AttendanceRecord(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('LATE', 'Late'),
        ('HALF_DAY', 'Half Day'),
        ('ON_LEAVE', 'On Leave'),
    ], default='PRESENT')
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['employee', 'date']
        ordering = ['-date']

class LeaveRequest(BaseModel):
    LEAVE_TYPES = [
        ('ANNUAL', 'Annual Leave'),
        ('SICK', 'Sick Leave'),
        ('EMERGENCY', 'Emergency Leave'),
        ('MATERNITY', 'Maternity Leave'),
        ('PATERNITY', 'Paternity Leave'),
        ('HAJJ', 'Hajj Leave'),
        ('UNPAID', 'Unpaid Leave'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.IntegerField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    rejection_reason = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

class Payroll(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payrolls')
    month = models.IntegerField()
    year = models.IntegerField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overtime = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('PROCESSED', 'Processed'),
        ('PAID', 'Paid'),
    ], default='PENDING')
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['employee', 'month', 'year']
        ordering = ['-year', '-month']
        verbose_name_plural = 'Payroll'
