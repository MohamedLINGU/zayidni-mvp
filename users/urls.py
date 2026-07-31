from django.urls import path
from .views import RegisterView, RequestOTPView, VerifyOTPView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('otp/request/', RequestOTPView.as_view(), name='otp-request'),
    path('otp/verify/', VerifyOTPView.as_view(), name='otp-verify'),
]
