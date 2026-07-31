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

        with transaction.atomic():
            listing = get_object_or_404(Listing.objects.select_for_update(), pk=listing_id)
            if not listing.is_active_now():
                return Response({'detail': 'Listing is not active'}, status=status.HTTP_400_BAD_REQUEST)
            current = listing.current_price if listing.current_price is not None else listing.starting_price
            min_allowed = current + listing.min_increment
            if amount < min_allowed:
                return Response({'detail': f'Minimum allowed bid is {min_allowed}'}, status=status.HTTP_400_BAD_REQUEST)
            bid = Bid.objects.create(listing=listing, bidder=request.user, amount=amount)
            listing.current_price = amount
            listing.save()

        return Response(BidSerializer(bid).data, status=status.HTTP_201_CREATED)
