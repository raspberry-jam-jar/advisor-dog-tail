from rest_framework import status, mixins, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import AdviceSearchFilter
from .models import Advice
from .serializers import (
    ReadOnlyAdviceSerializer,
    AdviceSerializer,
    UpdateAdviceSerializer,
)


class AdviceViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    An Account model viewset
    """

    queryset = Advice.objects.order_by("-created").all()
    permission_classes = (permissions.IsAuthenticated,)
    serializers = {
        "default": ReadOnlyAdviceSerializer,
        "create": AdviceSerializer,
        "update": UpdateAdviceSerializer,
        "partial_update": UpdateAdviceSerializer,
    }
    filter_backends = (AdviceSearchFilter,)
    search_fields = (
        "title",
        "tags__title",
        "tags__slug",
    )
    ordering_fields = ("title", "created")
    ordering = "-created"

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers.get("default"))

    @action(
        detail=True,
        methods=["delete"],
        url_path=r"tag/(?P<tag_slug>\w{1})",
        permission_classes=(permissions.IsAuthenticated,),
    )
    def tag(self, request, tag_slug, pk=None):
        """
        Remove tag attached to the advice.
        """
        advice = self.get_object()
        rel_tag_qs = advice.tags.filter(slug=tag_slug)
        if rel_tag_qs.exists():
            rel_tag_qs.first().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
