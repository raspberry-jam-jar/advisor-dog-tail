from django_filters import rest_framework as filters
from .models import Account


class AccountFilterSet(filters.FilterSet):
    created_from = filters.DateTimeFilter(field_name="created", lookup_expr="gte")
    created_to = filters.DateTimeFilter(field_name="created", lookup_expr="lte")

    class Meta:
        model = Account
        fields = ("created_from", "created_to")
