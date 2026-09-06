from django.db import models
from django.conf import settings
from apps.common.models import BaseModel

class DashboardMetric(BaseModel):
    name = models.CharField(max_length=255)
    metric_key = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    previous_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    unit = models.CharField(max_length=50, blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, blank=True, help_text='Hex color')
    chart_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Report(BaseModel):
    REPORT_TYPES = [
        ('DAILY', 'Daily Report'),
        ('WEEKLY', 'Weekly Report'),
        ('MONTHLY', 'Monthly Report'),
        ('QUARTERLY', 'Quarterly Report'),
        ('CUSTOM', 'Custom Report'),
    ]

    name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    parameters = models.JSONField(default=dict, blank=True)
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='reports/', blank=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('GENERATING', 'Generating'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ], default='PENDING')
    generated_at = models.DateTimeField(null=True, blank=True)
    date_from = models.DateField()
    date_to = models.DateField()

    class Meta:
        ordering = ['-created_at']

class KPI(BaseModel):
    name = models.CharField(max_length=255)
    kpi_key = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, choices=[
        ('OPERATIONS', 'Operations'),
        ('FINANCIAL', 'Financial'),
        ('CUSTOMER', 'Customer'),
        ('COURIER', 'Courier'),
        ('WAREHOUSE', 'Warehouse'),
    ])
    target_value = models.DecimalField(max_digits=15, decimal_places=2)
    current_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    unit = models.CharField(max_length=50, blank=True)
    formula = models.TextField(blank=True)
    frequency = models.CharField(max_length=20, choices=[
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
    ], default='DAILY')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
