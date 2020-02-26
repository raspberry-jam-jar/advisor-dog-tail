from rest_framework import mixins
from rest_framework import viewsets

from rest_framework import filters

from .models import Advice
from .serializers import AdviceSerializer


class AdviceViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    An Account model viewset
    """

    queryset = Advice.objects.order_by("-created").all()
    serializer_class = AdviceSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("title",)
    ordering_fields = ("title", "created")
    ordering = "-created"
