from django.db import models

class Bid(models.Model):
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.bidder} -> {self.amount}"
