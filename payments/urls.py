from django.urls import path
from .views import gateway_webhook, CreatePaymentSessionView, SandboxPayView

urlpatterns = [
    path('webhook/', gateway_webhook, name='payments-webhook'),
    path('create_session/', CreatePaymentSessionView.as_view(), name='payments-create-session'),
    path('sandbox/pay/<uuid:tx_id>/', SandboxPayView.as_view(), name='payments-sandbox-pay'),
]
