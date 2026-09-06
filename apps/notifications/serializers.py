from rest_framework import serializers
from .models import Notification, PushDevice

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['recipient', 'is_read', 'read_at', 'is_sent', 'sent_at']

class PushDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushDevice
        fields = '__all__'
