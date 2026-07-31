from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/listing/(?P<listing_id>\d+)/$', consumers.ListingConsumer.as_asgi()),
]
