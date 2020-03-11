from rest_framework.exceptions import NotFound
from rest_framework import response, status, mixins, viewsets, permissions
from rest_framework.decorators import action

from api.advice.models.advice import Advice
from api.users import permissions as user_permissions

from .models import Comment
from .serializers import (
    CommentSerializer,
    UpdateCommentSerializer,
)


class CommentViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    An Account model viewset
    """

    queryset = Comment.objects.order_by("-created").all()
    permission_classes = (permissions.IsAuthenticated, user_permissions.IsAuthor)
    serializers = {
        "default": CommentSerializer,
        "create": CommentSerializer,
        "update": UpdateCommentSerializer,
        "partial_update": UpdateCommentSerializer,
    }
    ordering = "-created"

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers.get("default"))

    @action(
        detail=False,
        methods=["GET"],
        url_path=r"for/(?P<advice_slug>\w+)",
        permission_classes=(permissions.IsAuthenticated,),
    )
    def for_advice(self, request, advice_slug):
        """
        Get paginated set of comments for the passed advice
        """
        try:
            advice = Advice.objects.get(slug=advice_slug)
            queryset = Comment.objects.filter(advice=advice).all()
            c_serializer = CommentSerializer(queryset, many=True)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(c_serializer.data)
            return response.Response(c_serializer.data)
        except Advice.DoesNotExist:
            raise NotFound(
                detail="No comments found for advice {advice_slug}",
                code=status.HTTP_404_NOT_FOUND,
            )
