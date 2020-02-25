from django.contrib.auth import get_user_model
from rest_framework import serializers

from djoser.serializers import UserSerializer as UserSerializerBase

from .models import Account


class UserSerializer(UserSerializerBase):
    class Meta(UserSerializerBase.Meta):
        ref_name = "api.users.serializers.UserSerializer"
        model = get_user_model()
        fields = ("pk", "username", "email")


class AccountSerializer(serializers.ModelSerializer):
    """
    A write-only serializer for a client model instance
    """

    class Meta:
        model = Account
        fields = ("email",)
        extra_kwargs = {"email": {"write_only": True}}


class ReadOnlyAccountSerializer(serializers.ModelSerializer):
    """
    A read-only serializer for a client model instance
    """

    class Meta:
        model = Account
        fields = (
            "pk",
            "email",
        )
        read_only_fields = (
            "pk",
            "email",
        )
