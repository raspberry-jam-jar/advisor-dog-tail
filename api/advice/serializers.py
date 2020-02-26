from rest_framework import serializers

from .models import Advice


class AdviceSerializer(serializers.ModelSerializer):
    """
    Advice model serializer.
    """

    class Meta:
        model = Advice
        fields = ("title", "slug", "link", "created")
        read_only_fields = ("slug", "created")
