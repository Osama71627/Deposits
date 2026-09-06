from django.urls import path
from . import views

urlpatterns = [
    path('tickets/', views.SupportTicketListCreateView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/messages/', views.TicketMessageListCreateView.as_view(), name='ticket-messages'),
    path('feedback/', views.CustomerFeedbackCreateView.as_view(), name='customer-feedback'),
    path('complaints/', views.CustomerComplaintListCreateView.as_view(), name='complaint-list'),
]
