from django.db import models
from django.conf import settings
from apps.common.models import BaseModel

class CourierProfile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courier_profile')
    is_available = models.BooleanField(default=False)
    is_on_duty = models.BooleanField(default=False)
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    last_location_update = models.DateTimeField(null=True, blank=True)
    total_deliveries = models.IntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    vehicle_type = models.CharField(max_length=50, blank=True)
    vehicle_plate = models.CharField(max_length=20, blank=True)
    license_number = models.CharField(max_length=50, blank=True)
    id_number = models.CharField(max_length=20, blank=True)
    emergency_contact = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Courier: {self.user.get_full_name()}"

class Attendance(BaseModel):
    courier = models.ForeignKey(CourierProfile, on_delete=models.CASCADE, related_name='attendance')
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField(null=True, blank=True)
    check_in_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    check_in_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    check_out_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    check_out_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('ON_TIME', 'On Time'),
        ('LATE', 'Late'),
        ('ABSENT', 'Absent'),
    ], default='ON_TIME')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-check_in_time']
        verbose_name_plural = 'Attendance'

class CourierEarnings(BaseModel):
    courier = models.ForeignKey(CourierProfile, on_delete=models.CASCADE, related_name='earnings')
    storage_request = models.ForeignKey('customers.StorageRequest', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=50, choices=[
        ('DELIVERY_FEE', 'Delivery Fee'),
        ('BONUS', 'Bonus'),
        ('TIP', 'Tip'),
        ('ADJUSTMENT', 'Adjustment'),
    ])
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('PAID', 'Paid'),
    ], default='PENDING')
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Courier Earnings'

class CourierPerformance(BaseModel):
    courier = models.ForeignKey(CourierProfile, on_delete=models.CASCADE, related_name='performance')
    date = models.DateField()
    deliveries_completed = models.IntegerField(default=0)
    deliveries_cancelled = models.IntegerField(default=0)
    on_time_deliveries = models.IntegerField(default=0)
    late_deliveries = models.IntegerField(default=0)
    average_response_time = models.DurationField(null=True, blank=True)
    total_distance_km = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ['courier', 'date']
        ordering = ['-date']
