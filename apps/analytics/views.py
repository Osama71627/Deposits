from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta
from .models import DashboardMetric, Report, KPI
from .serializers import DashboardMetricSerializer, ReportSerializer, KPISerializer
from apps.customers.models import StorageRequest
from apps.payments.models import Payment

class DashboardMetricsView(APIView):
    def get(self, request):
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        
        metrics = {
            'total_requests': StorageRequest.objects.count(),
            'active_requests': StorageRequest.objects.filter(status__in=['PENDING', 'ASSIGNED', 'PICKUP_IN_PROGRESS', 'IN_TRANSIT']).count(),
            'completed_today': StorageRequest.objects.filter(completed_at__date=today).count(),
            'total_revenue': Payment.objects.filter(status='COMPLETED').aggregate(total=Sum('net_amount'))['total'] or 0,
            'revenue_today': Payment.objects.filter(paid_at__date=today, status='COMPLETED').aggregate(total=Sum('net_amount'))['total'] or 0,
            'avg_rating': StorageRequest.objects.filter(feedback__isnull=False).aggregate(avg=Avg('feedback__rating'))['avg'] or 0,
        }
        return Response(metrics)

class DashboardMetricListView(generics.ListAPIView):
    queryset = DashboardMetric.objects.all()
    serializer_class = DashboardMetricSerializer

class ReportListCreateView(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAdminUser]

class KPIListView(generics.ListAPIView):
    queryset = KPI.objects.filter(is_active=True)
    serializer_class = KPISerializer
