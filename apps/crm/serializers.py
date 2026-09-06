from rest_framework import serializers
from .models import CustomerSegment, SupportTicket, TicketMessage, CustomerFeedback, CustomerComplaint

class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = '__all__'
        read_only_fields = ['customer', 'created_at', 'updated_at']

class TicketMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = '__all__'

class CustomerFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerFeedback
        fields = '__all__'

class CustomerComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerComplaint
        fields = '__all__'
