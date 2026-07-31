from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
import json
from .models import Transaction
from listings.models import Listing
from notifications.models import Notification

@csrf_exempt
def gateway_webhook(request):
    """Simple webhook receiver for payment gateway simulation.
    Expected JSON: {event: 'hold_created'|'hold_captured'|'refund'|'hold_released', transaction_id, gateway_id, amount}
    """
    if request.method != 'POST':
        return JsonResponse({'detail':'method not allowed'}, status=405)
    try:
        payload = json.loads(request.body)
    except Exception:
        return JsonResponse({'detail':'invalid json'}, status=400)
    event = payload.get('event')
    tx_id = payload.get('transaction_id')
    gateway_id = payload.get('gateway_id')
    amount = payload.get('amount')

    if not tx_id or not event:
        return JsonResponse({'detail':'missing fields'}, status=400)

    try:
        tx = Transaction.objects.get(id=tx_id)
    except Transaction.DoesNotExist:
        return JsonResponse({'detail':'transaction not found'}, status=404)

    if event == 'hold_created':
        tx.status = Transaction.STATUS_HELD
        tx.gateway_id = gateway_id
        tx.save()
        Notification.objects.create(user=tx.buyer, type='payment_held', content=f'Held {tx.amount} {tx.currency} for listing {tx.listing.title}')
        Notification.objects.create(user=tx.seller, type='payment_pending', content=f'Buyer has initiated payment for {tx.listing.title}')
        return JsonResponse({'ok':True})
    elif event == 'hold_released' or event == 'captured':
        tx.status = Transaction.STATUS_RELEASED
        tx.gateway_id = gateway_id
        tx.save()
        Notification.objects.create(user=tx.seller, type='payment_released', content=f'Payment released for {tx.listing.title}')
        return JsonResponse({'ok':True})
    elif event == 'refund':
        tx.status = Transaction.STATUS_REFUNDED
        tx.save()
        Notification.objects.create(user=tx.buyer, type='payment_refunded', content=f'Payment refunded for {tx.listing.title}')
        return JsonResponse({'ok':True})
    else:
        return JsonResponse({'detail':'unknown event'}, status=400)
