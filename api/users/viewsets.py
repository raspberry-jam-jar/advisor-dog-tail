from rest_framework import mixins
from rest_framework import viewsets

from rest_framework import filters
from django_filters import rest_framework as filter_ext

from .models import Account
from .filters import AccountFilterSet
from .serializers import AccountSerializer, ReadOnlyAccountSerializer


class AccountViewset(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    A generic viewset for a client model.
    """

    queryset = Account.objects.order_by("-created").all()
    serializers = {
        "list": ReadOnlyAccountSerializer,
        "retreive": ReadOnlyAccountSerializer,
        "create": AccountSerializer,
        "default": ReadOnlyAccountSerializer,
    }
    filter_backends = (filters.SearchFilter, filter_ext.DjangoFilterBackend)
    filterset_class = AccountFilterSet
    search_fields = ("email",)
    ordering_fields = ("email", "created")
    ordering = ("-created",)

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers["default"])
