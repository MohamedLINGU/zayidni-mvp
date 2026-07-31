from celery import shared_task
from django.utils import timezone
from django.conf import settings
from .models import Transaction
from notifications.models import Notification

@shared_task
def auto_release_holds():
    """Release holds that passed the hold timeout and are still held.
    Timeout configurable via settings.PAYMENT_HOLD_TIMEOUT_SECONDS (default 3 days)
    """
    timeout = getattr(settings, 'PAYMENT_HOLD_TIMEOUT_SECONDS', 3 * 24 * 3600)
    cutoff = timezone.now() - timezone.timedelta(seconds=timeout)
    held = Transaction.objects.filter(status=Transaction.STATUS_HELD, created_at__lte=cutoff)
    results = []
    for tx in held:
        # For MVP auto-release to seller; in production this should consider tracking/shipping state and disputes
        tx.status = Transaction.STATUS_RELEASED
        tx.save()
        Notification.objects.create(user=tx.seller, type='payment_released_auto', content=f'Auto-released payment for {tx.listing.title}')
        Notification.objects.create(user=tx.buyer, type='payment_released_auto_buyer', content=f'Payment for {tx.listing.title} released to seller (auto)')
        results.append(str(tx.id))
    return results
