from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/read/', views.MarkNotificationReadView.as_view(), name='mark-read'),
    path('notifications/read-all/', views.MarkAllReadView.as_view(), name='mark-all-read'),
    path('register-device/', views.RegisterPushDeviceView.as_view(), name='register-device'),
]
