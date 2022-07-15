import logging

from django.core.cache import cache
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as ParentTokenObtainPairSerializer,
)
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer as ParentTokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import AccessToken

from applications.authentication.models import User


class TokenObtainPairSerializer(ParentTokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(TokenObtainPairSerializer, self).validate(attrs)
        data.update(
            {
                "user": self.user.get_full_name(),
                "groups": list(self.user.groups.values_list('name', flat=True))
            }
        )
        self.store_access(data["access"])

        return data

    def store_access(self, access_token: str):
        token_key_lookup = f"token_key_{self.user.id}"
        token = cache.get(token_key_lookup, "")
        try:
            AccessToken(token)
            raise serializers.ValidationError("There is already an active session using your account.")

        except TokenError as e:
            logging.info('Access token is not valid: {}'.format(e))

        cache.set(token_key_lookup, access_token, timeout=30)


class TokenRefreshSerializer(ParentTokenRefreshSerializer):
    pass


class UserInfoSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True, source="get_full_name")
    groups = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "full_name",
            "groups",
        ]


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', "first_name", "last_name", 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
