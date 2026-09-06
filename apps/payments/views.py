from rest_framework import generics, permissions, filters
from .models import Payment, PaymentGateway
from .serializers import PaymentSerializer

class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_fields = ['status', 'payment_method']

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'CUSTOMER':
            return Payment.objects.filter(customer=user)
        return Payment.objects.all()

class PaymentDetailView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
