from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
import json
from .models import Transaction
from listings.models import Listing
from notifications.models import Notification

@csrf_exempt
def gateway_webhook(request):
    """Simple webhook receiver for payment gateway simulation.
    Expected JSON: {event: 'hold_created'|'captured'|'refund'|'hold_released', transaction_id, gateway_id, amount}
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
    elif event == 'captured' or event == 'hold_released':
        tx.status = Transaction.STATUS_RELEASED
        tx.gateway_id = gateway_id
        tx.save()
        Notification.objects.create(user=tx.seller, type='payment_released', content=f'Payment released for {tx.listing.title}')
        Notification.objects.create(user=tx.buyer, type='payment_released_buyer', content=f'Payment released to seller for {tx.listing.title}')
        return JsonResponse({'ok':True})
    elif event == 'refund':
        tx.status = Transaction.STATUS_REFUNDED
        tx.save()
        Notification.objects.create(user=tx.buyer, type='payment_refunded', content=f'Payment refunded for {tx.listing.title}')
        return JsonResponse({'ok':True})
    else:
        return JsonResponse({'detail':'unknown event'}, status=400)


class PendingForListingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        listing_id = request.GET.get('listing_id')
        if not listing_id:
            return Response({'detail': 'listing_id required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            listing = Listing.objects.get(id=listing_id)
        except Listing.DoesNotExist:
            return Response({'detail': 'listing not found'}, status=status.HTTP_404_NOT_FOUND)
        tx = Transaction.objects.filter(listing=listing, buyer=request.user, status__in=[Transaction.STATUS_PENDING, Transaction.STATUS_HELD]).order_by('-created_at').first()
        if not tx:
            return Response({'found': False})
        return Response({'found': True, 'transaction_id': str(tx.id), 'status': tx.status})


class CreatePaymentSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        tx_id = request.data.get('transaction_id')
        if not tx_id:
            return Response({'detail': 'transaction_id required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            tx = Transaction.objects.get(id=tx_id)
        except Transaction.DoesNotExist:
            return Response({'detail': 'transaction not found'}, status=status.HTTP_404_NOT_FOUND)
        if tx.status != Transaction.STATUS_PENDING:
            return Response({'detail': 'transaction not in pending state'}, status=status.HTTP_400_BAD_REQUEST)
        # In production, create gateway session and return payment URL. For sandbox, return internal sandbox URL
        scheme = 'https' if request.is_secure() else 'http'
        host = request.get_host()
        payment_url = f"{scheme}://{host}/api/payments/sandbox/pay/{tx.id}/"
        return Response({'payment_url': payment_url})


class SandboxPayView(View):
    """Simple HTML page to simulate payment gateway actions for a transaction."""
    def get(self, request, tx_id):
        try:
            tx = Transaction.objects.get(id=tx_id)
        except Transaction.DoesNotExist:
            return HttpResponse('Transaction not found', status=404)
        html = f"""
        <html><head><meta charset='utf-8'><title>Sandbox Pay - {tx.id}</title></head><body>
        <h3>Sandbox Payment Simulator for Transaction {tx.id}</h3>
        <p>Amount: {tx.amount} {tx.currency}</p>
        <button onclick="fetch('/api/payments/webhook/',{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{event:'hold_created',transaction_id:'{tx.id}',gateway_id:'sandbox-1',amount:'{tx.amount}'}})}).then(r=>r.json()).then(a=>alert(JSON.stringify(a)))">Simulate Hold Created</button>
        <button onclick="fetch('/api/payments/webhook/',{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{event:'captured',transaction_id:'{tx.id}',gateway_id:'sandbox-1',amount:'{tx.amount}'}})}).then(r=>r.json()).then(a=>alert(JSON.stringify(a)))">Simulate Capture (release funds)</button>
        <button onclick="fetch('/api/payments/webhook/',{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{event:'refund',transaction_id:'{tx.id}',gateway_id:'sandbox-1',amount:'{tx.amount}'}})}).then(r=>r.json()).then(a=>alert(JSON.stringify(a)))">Simulate Refund</button>
        <p>These buttons POST to /api/payments/webhook/ to simulate gateway webhooks.</p>
        </body></html>
        """
        return HttpResponse(html)
