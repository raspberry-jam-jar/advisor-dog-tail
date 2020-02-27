from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "api.users.serializers.UserSerializer"
        model = get_user_model()
        fields = ("pk", "username", "email", "first_name", "last_name")
