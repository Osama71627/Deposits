from rest_framework import serializers
from .models import CourierProfile, Attendance, CourierEarnings, CourierPerformance

class CourierProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierProfile
        fields = '__all__'
        read_only_fields = ['id', 'user', 'total_deliveries', 'total_earnings', 'rating']

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class CourierEarningsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierEarnings
        fields = '__all__'
