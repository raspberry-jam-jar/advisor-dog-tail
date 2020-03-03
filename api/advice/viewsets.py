from rest_framework import mixins, viewsets, filters, permissions

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
    filter_backends = (filters.SearchFilter,)
    search_fields = ("title",)
    ordering_fields = ("title", "created")
    ordering = "-created"

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers.get("default"))
