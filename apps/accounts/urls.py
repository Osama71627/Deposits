from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('me/', views.UserDetailView.as_view(), name='user-detail'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('roles/', views.RoleListView.as_view(), name='role-list'),
    path('audit-logs/', views.AuditLogListView.as_view(), name='audit-log-list'),
]
