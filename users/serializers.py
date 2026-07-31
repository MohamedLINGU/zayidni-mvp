from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import OTPCode, Profile

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username','password','email','phone')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        phone = validated_data.pop('phone', None)
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, phone=phone)
        return user

class OTPRequestSerializer(serializers.Serializer):
    phone = serializers.CharField()

class OTPVerifySerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()
