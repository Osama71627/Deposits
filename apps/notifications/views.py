from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification, PushDevice
from .serializers import NotificationSerializer, PushDeviceSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)[:50]

class MarkNotificationReadView(APIView):
    def post(self, request, pk):
        notification = Notification.objects.get(id=pk, recipient=request.user)
        notification.is_read = True
        notification.save()
        return Response({'status': 'success'})

class MarkAllReadView(APIView):
    def post(self, request):
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return Response({'status': 'success'})

class RegisterPushDeviceView(generics.CreateAPIView):
    queryset = PushDevice.objects.all()
    serializer_class = PushDeviceSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
