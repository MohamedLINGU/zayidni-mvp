from celery import shared_task
from django.utils import timezone
from django.db import transaction
from .models import Listing
from bids.models import Bid
from notifications.models import Notification

@shared_task
def close_ended_auctions():
    now = timezone.now()
    ended = Listing.objects.filter(status=Listing.STATUS_ACTIVE, end_time__lte=now)
    results = []
    for listing in ended:
        try:
            with transaction.atomic():
                l = Listing.objects.select_for_update().get(pk=listing.pk)
                # double-check
                if l.status != Listing.STATUS_ACTIVE or l.end_time > now:
                    continue
                # find highest bid
                winner_bid = Bid.objects.filter(listing=l).order_by('-amount','created_at').first()
                l.status = Listing.STATUS_CLOSED
                l.save()
                if winner_bid:
                    # create a Transaction in pending_hold state so buyer can complete payment (escrow/hold)
                    from payments.models import Transaction
                    tx = Transaction.objects.create(
                        listing=l,
                        buyer=winner_bid.bidder,
                        seller=l.seller,
                        amount=winner_bid.amount,
                        currency='IQD',
                        payment_method='',
                        status=Transaction.STATUS_PENDING,
                    )
                    # notify winner and seller with transaction info and next steps
                    Notification.objects.create(user=winner_bid.bidder, type='auction_won', content=f'لقد فزت بالمزاد: {l.title} بالمبلغ {winner_bid.amount}. اكمال الدفع عبر المعاملات: {tx.id}')
                    Notification.objects.create(user=l.seller, type='auction_sold', content=f'انتهى المزاد: {l.title}. الفائز: {winner_bid.bidder} بمبلغ {winner_bid.amount}. معاملة: {tx.id}')
                    results.append({'listing': l.id, 'winner': str(winner_bid.bidder), 'amount': str(winner_bid.amount), 'transaction': str(tx.id)})
                else:
                    Notification.objects.create(user=l.seller, type='auction_ended_no_bids', content=f'انتهى المزاد: {l.title} بلا مزايدات')
                    results.append({'listing': l.id, 'winner': None})
        except Listing.DoesNotExist:
            continue
    return results
