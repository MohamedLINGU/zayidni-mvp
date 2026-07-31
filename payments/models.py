from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()

class Transaction(models.Model):
    STATUS_PENDING = 'pending_hold'
    STATUS_HELD = 'held'
    STATUS_RELEASED = 'released'
    STATUS_REFUNDED = 'refunded'
    STATUS_DISPUTED = 'disputed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending (hold)'),
        (STATUS_HELD, 'Held'),
        (STATUS_RELEASED, 'Released to seller'),
        (STATUS_REFUNDED, 'Refunded to buyer'),
        (STATUS_DISPUTED, 'Disputed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, related_name='transactions')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=8, default='IQD')
    payment_method = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    gateway_id = models.CharField(max_length=255, blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_hold(self):
        return self.status in (self.STATUS_PENDING, self.STATUS_HELD)

    def __str__(self):
        return f"Txn {self.id} {self.amount} {self.currency} ({self.status})"
