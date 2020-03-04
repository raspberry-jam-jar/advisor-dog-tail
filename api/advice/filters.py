import operator

from functools import reduce

from django.db import models
from django.db.models.constants import LOOKUP_SEP

from rest_framework import filters
from rest_framework.compat import distinct

from .models.advice import Mapping


class AdviceSearchFilter(filters.SearchFilter):
    def build_lookup_queries(
        self, orm_lookups: list, search_terms: list, operator=operator.or_
    ):
        conditions = []
        for search_term in search_terms:
            queries = [
                models.Q(**{orm_lookup: search_term}) for orm_lookup in orm_lookups
            ]
            conditions.append(reduce(operator, queries))
        return conditions

    def filter_tag_count(self, orm_lookups: list, search_terms: list):
        """Convet tags lookup field to mapping tag field"""
        # Filter out all non-tag-related fields
        tag_orm_lookups = filter(lambda t: "tags" in t, list(orm_lookups))
        # Normalize lookup fields
        tag_orm_lookups = map(lambda t: t.replace("s", "", 1), tag_orm_lookups)
        # Remove current lookup modifcators
        tag_orm_lookups = map(lambda t: t.split(LOOKUP_SEP, 2)[:-1], tag_orm_lookups)
        # Build a lookup query to check for an search item entry
        tag_orm_lookups = map(lambda t: LOOKUP_SEP.join(t), tag_orm_lookups)

        return self.build_lookup_queries(list(tag_orm_lookups), search_terms)

    def filter_queryset(self, request, queryset, view):
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)

        if not search_fields or not search_terms:
            return queryset

        orm_lookups = [
            self.construct_search(str(search_field)) for search_field in search_fields
        ]

        base = queryset
        conditions = self.build_lookup_queries(orm_lookups, search_terms)
        queryset = queryset.filter(reduce(operator.or_, conditions))

        if self.must_call_distinct(queryset, search_fields):
            # Filtering against a many-to-many field requires us to
            # call queryset.distinct() in order to avoid duplicate items
            # in the resulting queryset.
            # We try to avoid this if possible, for performance reasons.
            queryset = distinct(queryset, base)

        tag_conditions = models.Q(
            reduce(operator.or_, self.filter_tag_count(orm_lookups, search_terms))
        )
        mapping_sub_qs = Mapping.objects.filter(advice_id=models.OuterRef("id")).filter(
            tag_conditions
        )
        return queryset.annotate(
            matches=models.Subquery(
                mapping_sub_qs.values("advice_id")
                .annotate(count=models.Count("pk", distinct=True))
                .values("count")
            )
        ).order_by("-matches")
