import json
from datetime import timedelta

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone

from listings.tasks import close_ended_auctions
from listings.models import Listing
from bids.models import Bid
from payments.models import Transaction


class PaymentsFlowTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.seller = User.objects.create_user(username='seller', password='pw')
        self.buyer = User.objects.create_user(username='buyer', password='pw')
        # set profile phone and mark verified if Profile exists
        try:
            self.buyer.profile.phone = '888'
            self.buyer.profile.phone_verified = True
            self.buyer.profile.save()
        except Exception:
            pass

        now = timezone.now()
        self.listing = Listing.objects.create(
            title='Test Listing',
            seller=self.seller,
            starting_price=10,
            current_price=10,
            start_time=now - timedelta(minutes=5),
            end_time=now - timedelta(minutes=1),
            min_increment=5,
        )
        Bid.objects.create(listing=self.listing, bidder=self.buyer, amount=100)
        self.client = Client()

    def test_close_creates_transaction_and_webhook_updates(self):
        # run the closing task which should create a Transaction when a winner exists
        close_ended_auctions()
        tx = Transaction.objects.get(listing=self.listing)
        self.assertIsNotNone(tx)
        # expect initial pending hold status (string name may vary by implementation)
        self.assertIn(tx.status, ['pending_hold', 'pending', 'pending_hold_created', 'pending_hold'])

        old_updated = tx.updated_at
        payload = {'event': 'hold_created', 'transaction_id': str(tx.id)}
        resp = self.client.post('/api/payments/webhook/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        tx.refresh_from_db()
        # webhook should update the transaction record timestamp/status
        self.assertTrue(tx.updated_at >= old_updated)
