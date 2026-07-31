from django.test import TestCase
from django.contrib.auth import get_user_model
from listings.models import Listing
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from .models import Bid

class BidConcurrencyTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.seller = User.objects.create_user(username='seller', password='pass')
        self.bidder1 = User.objects.create_user(username='b1', password='pass')
        self.bidder2 = User.objects.create_user(username='b2', password='pass')
        now = timezone.now()
        self.listing = Listing.objects.create(
            title='Test',
            seller=self.seller,
            starting_price=Decimal('10.00'),
            current_price=None,
            min_increment=Decimal('1.00'),
            status=Listing.STATUS_ACTIVE,
            start_time=now - timedelta(minutes=1),
            end_time=now + timedelta(minutes=10),
        )

    def test_sequential_bids_update_listing(self):
        Bid.objects.create(listing=self.listing, bidder=self.bidder1, amount=Decimal('11.00'))
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.current_price, Decimal('11.00'))
