from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Listing(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_ACTIVE = 'active'
    STATUS_CLOSED = 'closed'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_ACTIVE, 'Active'),
        (STATUS_CLOSED, 'Closed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    starting_price = models.DecimalField(max_digits=12, decimal_places=2)
    current_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    min_increment = models.DecimalField(max_digits=12, decimal_places=2, default=1.00)
    image_urls = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # contact options for seller (seller can choose to allow contact info to be shown)
    allow_contact_info = models.BooleanField(default=False)
    contact_phone = models.CharField(max_length=32, blank=True, null=True)
    contact_email = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    def is_active_now(self):
        now = timezone.now()
        return self.status == self.STATUS_ACTIVE and self.start_time <= now < self.end_time
