from django.db import models
from django.conf import settings
from apps.common.models import BaseModel

class CustomerSegment(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    criteria = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class SupportTicket(BaseModel):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('WAITING', 'Waiting on Customer'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    subject = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    storage_request = models.ForeignKey('customers.StorageRequest', on_delete=models.SET_NULL, null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"#{self.id} - {self.subject}"

class TicketMessage(BaseModel):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    attachment = models.FileField(upload_to='tickets/', blank=True)

    class Meta:
        ordering = ['created_at']

class CustomerFeedback(BaseModel):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedback')
    storage_request = models.ForeignKey('customers.StorageRequest', on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    courier_rating = models.IntegerField(null=True, blank=True)
    warehouse_rating = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ['customer', 'storage_request']
        verbose_name_plural = 'Customer Feedback'

class CustomerComplaint(BaseModel):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints')
    subject = models.CharField(max_length=255)
    description = models.TextField()
    storage_request = models.ForeignKey('customers.StorageRequest', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('OPEN', 'Open'),
        ('INVESTIGATING', 'Investigating'),
        ('RESOLVED', 'Resolved'),
        ('DISMISSED', 'Dismissed'),
    ], default='OPEN')
    resolution = models.TextField(blank=True)
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
