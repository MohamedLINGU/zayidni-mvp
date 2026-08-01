import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from listings.models import Listing
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

class BidAPITest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.seller = User.objects.create_user(username='seller2', password='pass')
        self.bidder = User.objects.create_user(username='bidder', password='pass')
        # mark bidder phone verified if Profile exists
        try:
            self.bidder.profile.phone_verified = True
            self.bidder.profile.save()
        except Exception:
            pass
        now = timezone.now()
        self.listing = Listing.objects.create(
            title='TestAPI',
            seller=self.seller,
            starting_price=Decimal('10.00'),
            current_price=None,
            min_increment=Decimal('1.00'),
            status=Listing.STATUS_ACTIVE,
            start_time=now - timedelta(minutes=1),
            end_time=now + timedelta(minutes=10),
        )

    def test_reject_bid_below_minimum(self):
        self.client.login(username='bidder', password='pass')
        url = '/api/bids/place/'
        data = json.dumps({'listing': self.listing.id, 'amount': '10.50'})
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Minimum allowed bid', response.json().get('detail', ''))
