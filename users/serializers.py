from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.contrib.auth.models import update_last_login

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, required=True)
    password2 = serializers.CharField(write_only=True, min_length=6, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'password', 'password2']

    def validate_username(self, value):
        if User.objects.get(username=value).exists():
            raise serializers.ValidationError('username already in user')
        return value

    def validate_email(self, value):
        if User.objects.get(email=value).exists():
            raise serializers.ValidationError('email already in user')
        return value

    def validate_phone(self, value):
        if User.objects.get(phone=value).exists():
            raise serializers.ValidationError('phone already in user')
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('password did not match')
        return data

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data['username']
        password = data['password']
        
        user = authenticate(username=username, password=password)
        
        if not user:
            raise serializers.ValidationError('invalid credential')
        
        if not user.is_active:
            raise serializers.ValidationError('inactive user')

        refresh = RefreshToken.for_user(user)
        update_last_login(None, user)

        return {
            'user': user,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }


class RefreshSerializer(serializers.Serializer):
    def validate(self, data):
        refresh_token = data['token']

        if not refresh_token:
            raise serializers.ValidationError({'detail': 'no refresh token'})

        try:
            refresh = RefreshToken(refresh_token)

            new_access = str(refresh.access_token)
            new_refresh = str(refresh)


            return {
                'new_access': new_access,
                'new_refresh': new_refresh
            }

        except TokenError:
            raise serializers.ValidationError({'detail': 'invalid token'})

