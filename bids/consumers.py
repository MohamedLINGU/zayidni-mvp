from channels.generic.websocket import AsyncJsonWebsocketConsumer

class ListingConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.listing_id = self.scope['url_route']['kwargs'].get('listing_id')
        self.group_name = f'listing_{self.listing_id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        # Optionally send a hello message
        await self.send_json({'type': 'connection.accepted', 'listing_id': self.listing_id})

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        # Clients shouldn't send arbitrary messages; ignore or handle pings
        pass

    # Handler for price updates sent via group_send
    async def price_update(self, event):
        await self.send_json({
            'type': 'price.update',
            'listing_id': event.get('listing_id'),
            'current_price': event.get('current_price'),
            'bidder': event.get('bidder'),
        })
