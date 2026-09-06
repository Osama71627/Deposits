from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import StorageRequest, CustomerProfile
from .serializers import StorageRequestSerializer, CreateStorageRequestSerializer, CustomerProfileSerializer

class StorageRequestListCreateView(generics.ListCreateAPIView):
    queryset = StorageRequest.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'is_paid', 'is_geofence_valid']
    search_fields = ['pickup_address', 'description']
    ordering_fields = ['created_at', 'total_amount']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateStorageRequestSerializer
        return StorageRequestSerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'CUSTOMER':
            return StorageRequest.objects.filter(customer=user)
        return StorageRequest.objects.all()

class StorageRequestDetailView(generics.RetrieveUpdateAPIView):
    queryset = StorageRequest.objects.all()
    serializer_class = StorageRequestSerializer

class CustomerProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer

    def get_object(self):
        profile, _ = CustomerProfile.objects.get_or_create(user=self.request.user)
        return profile
