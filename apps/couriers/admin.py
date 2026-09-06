from django.contrib import admin
from .models import CourierProfile, Attendance, CourierEarnings, CourierPerformance

@admin.register(CourierProfile)
class CourierProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_available', 'is_on_duty', 'total_deliveries', 'total_earnings', 'rating']
    list_filter = ['is_available', 'is_on_duty']
    search_fields = ['user__username']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['courier', 'check_in_time', 'check_out_time', 'status']

@admin.register(CourierEarnings)
class CourierEarningsAdmin(admin.ModelAdmin):
    list_display = ['courier', 'amount', 'type', 'status', 'created_at']

@admin.register(CourierPerformance)
class CourierPerformanceAdmin(admin.ModelAdmin):
    list_display = ['courier', 'date', 'deliveries_completed', 'on_time_deliveries', 'rating']
