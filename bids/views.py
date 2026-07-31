from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import transaction
from django.shortcuts import get_object_or_404

from listings.models import Listing
from .models import Bid
from .serializers import BidSerializer, CreateBidSerializer

class PlaceBidView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CreateBidSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        listing_id = serializer.validated_data['listing']
        amount = serializer.validated_data['amount']

        # require phone-verified user to place bids (anti-fake measure)
        if not hasattr(request.user, 'profile') or not request.user.profile.is_phone_verified:
            return Response({'detail': 'phone verification required to place bids'}, status=status.HTTP_403_FORBIDDEN)

        with transaction.atomic():
            listing = get_object_or_404(Listing.objects.select_for_update(), pk=listing_id)
            if not listing.is_active_now():
                return Response({'detail': 'Listing is not active'}, status=status.HTTP_400_BAD_REQUEST)
            current = listing.current_price if listing.current_price is not None else listing.starting_price
            min_allowed = current + listing.min_increment
            if amount < min_allowed:
                return Response({'detail': f'Minimum allowed bid is {min_allowed}'}, status=status.HTTP_400_BAD_REQUEST)
            # create bid with optional contact info
            contact_phone = request.data.get('contact_phone')
            contact_email = request.data.get('contact_email')
            message = request.data.get('message', '')
            bid = Bid.objects.create(listing=listing, bidder=request.user, amount=amount, contact_phone=contact_phone, contact_email=contact_email, message=message)
            listing.current_price = amount
            listing.save()

        # TODO: broadcast via Channels to websocket group for listing
        return Response(BidSerializer(bid).data, status=status.HTTP_201_CREATED)
