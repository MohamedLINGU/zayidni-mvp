import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate, login
from .serializers import RegisterSerializer, OTPRequestSerializer, OTPVerifySerializer
from .models import OTPCode, Profile

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'detail':'registered'}, status=status.HTTP_201_CREATED)


class RequestOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        code = '{:04d}'.format(random.randint(0,9999))
        otp = OTPCode.create_code(phone, code)
        # NOTE: In production send via SMS gateway (ZainCash/AsiaHawala integration or SMS provider)
        # For now return code in response for testing (remove in prod)
        return Response({'phone': phone, 'otp_test_code': code}, status=status.HTTP_201_CREATED)


class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']
        otp_qs = OTPCode.objects.filter(phone=phone, code=code, consumed=False).order_by('-created_at')
        if not otp_qs.exists():
            return Response({'detail':'invalid code'}, status=status.HTTP_400_BAD_REQUEST)
        otp = otp_qs.first()
        if not otp.is_valid():
            return Response({'detail':'code expired or consumed'}, status=status.HTTP_400_BAD_REQUEST)
        otp.consume()
        # mark profile(s) with this phone as verified
        profiles = Profile.objects.filter(phone=phone)
        for p in profiles:
            p.is_phone_verified = True
            p.save()
        return Response({'detail':'verified'}, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'detail':'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        return Response({'detail':'logged_in'})
