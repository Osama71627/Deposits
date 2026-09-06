from rest_framework import serializers
from .models import Payment, PaymentGateway, POSDevice, POSTransaction, Refund

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['customer', 'status', 'paid_at']
