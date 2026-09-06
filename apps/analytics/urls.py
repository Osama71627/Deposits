from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.DashboardMetricsView.as_view(), name='dashboard-metrics'),
    path('metrics/', views.DashboardMetricListView.as_view(), name='metric-list'),
    path('reports/', views.ReportListCreateView.as_view(), name='report-list'),
    path('kpis/', views.KPIListView.as_view(), name='kpi-list'),
]
