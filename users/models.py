from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()

# Extend or replace with a custom user model as needed later
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)
    kyc_status = models.CharField(max_length=20, default='none')  # none/minimal/verified

    def __str__(self):
        return self.display_name or str(self.user)


class OTPCode(models.Model):
    """Simple OTP model for phone verification (one-time, short TTL)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=32)
    code = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    consumed = models.BooleanField(default=False)

    @classmethod
    def create_code(cls, phone, code, ttl_seconds=300):
        now = timezone.now()
        return cls.objects.create(phone=phone, code=code, expires_at=now + timezone.timedelta(seconds=ttl_seconds))

    def is_valid(self):
        return (not self.consumed) and (timezone.now() < self.expires_at)

    def consume(self):
        self.consumed = True
        self.save()
