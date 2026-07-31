from rest_framework import serializers
from .models import Bid

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'listing', 'bidder', 'amount', 'created_at']

class CreateBidSerializer(serializers.Serializer):
    listing = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
