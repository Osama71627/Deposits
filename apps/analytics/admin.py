from django.contrib import admin
from .models import DashboardMetric, Report, KPI

@admin.register(DashboardMetric)
class DashboardMetricAdmin(admin.ModelAdmin):
    list_display = ['name', 'metric_key', 'value', 'previous_value', 'unit']

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'report_type', 'status', 'generated_by', 'generated_at']

@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
    list_display = ['name', 'kpi_key', 'category', 'target_value', 'current_value', 'frequency']
