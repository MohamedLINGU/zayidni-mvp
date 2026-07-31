from django.urls import path
from .views import PlaceBidView

urlpatterns = [
    path('place/', PlaceBidView.as_view(), name='place-bid'),
]
