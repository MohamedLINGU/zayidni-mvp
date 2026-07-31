from django.urls import path
from .views import gateway_webhook, CreatePaymentSessionView, SandboxPayView, PendingForListingView

urlpatterns = [
    path('webhook/', gateway_webhook, name='payments-webhook'),
    path('create_session/', CreatePaymentSessionView.as_view(), name='payments-create-session'),
    path('pending_for_listing/', PendingForListingView.as_view(), name='payments-pending-for-listing'),
    path('sandbox/pay/<uuid:tx_id>/', SandboxPayView.as_view(), name='payments-sandbox-pay'),
]
