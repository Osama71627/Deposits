from rest_framework import generics, permissions
from .models import CourierProfile, Attendance, CourierEarnings
from .serializers import CourierProfileSerializer, AttendanceSerializer, CourierEarningsSerializer

class CourierProfileView(generics.RetrieveUpdateAPIView):
    queryset = CourierProfile.objects.all()
    serializer_class = CourierProfileSerializer

    def get_object(self):
        profile, _ = CourierProfile.objects.get_or_create(user=self.request.user)
        return profile

class AttendanceListCreateView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def perform_create(self, serializer):
        courier = CourierProfile.objects.get(user=self.request.user)
        serializer.save(courier=courier)

    def get_queryset(self):
        courier = CourierProfile.objects.get(user=self.request.user)
        return Attendance.objects.filter(courier=courier)

class CourierEarningsListView(generics.ListAPIView):
    serializer_class = CourierEarningsSerializer

    def get_queryset(self):
        courier = CourierProfile.objects.get(user=self.request.user)
        return CourierEarnings.objects.filter(courier=courier)

class AvailableCouriersView(generics.ListAPIView):
    queryset = CourierProfile.objects.filter(is_available=True, is_on_duty=True)
    serializer_class = CourierProfileSerializer
