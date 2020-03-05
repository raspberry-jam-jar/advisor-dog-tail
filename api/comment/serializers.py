from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Comment model serializer.
    """

    class Meta:
        model = Comment
        fields = ("body", "score", "advice", "author")


class UpdateCommentSerializer(serializers.ModelSerializer):
    """
    Comment model serializer for updating.
    """

    class Meta:
        model = Comment
        fields = ("body", "score", "advice", "author")
        read_only_fields = ("advice", "author")
