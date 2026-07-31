from django.db import models

# Extend or replace with a custom user model as needed later
class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    display_name = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.display_name or str(self.user)
