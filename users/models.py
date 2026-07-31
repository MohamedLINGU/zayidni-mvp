from django.db import models
from django.contrib.auth import get_user_model

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
