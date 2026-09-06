from rest_framework import generics, permissions, filters
from .models import SupportTicket, TicketMessage, CustomerFeedback, CustomerComplaint
from .serializers import SupportTicketSerializer, TicketMessageSerializer, CustomerFeedbackSerializer, CustomerComplaintSerializer

class SupportTicketListCreateView(generics.ListCreateAPIView):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    filterset_fields = ['priority', 'status']

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'CUSTOMER':
            return SupportTicket.objects.filter(customer=user)
        return SupportTicket.objects.all()

class TicketMessageListCreateView(generics.ListCreateAPIView):
    queryset = TicketMessage.objects.all()
    serializer_class = TicketMessageSerializer

class CustomerFeedbackCreateView(generics.CreateAPIView):
    queryset = CustomerFeedback.objects.all()
    serializer_class = CustomerFeedbackSerializer

class CustomerComplaintListCreateView(generics.ListCreateAPIView):
    queryset = CustomerComplaint.objects.all()
    serializer_class = CustomerComplaintSerializer
