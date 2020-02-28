from rest_framework import status, mixins, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import AdviceSearchFilter
from .models.advice import Advice
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
    lookup_field = "slug"
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AdviceSerializer
    filter_backends = (AdviceSearchFilter,)
    search_fields = (
        "title",
        "slug",
        "tags__title",
        "tags__slug",
    )
    ordering_fields = ("title", "created")
    ordering = "-created"

    @action(
        detail=True,  # noqa: W605
        methods=["delete"],
        url_path="tag/(?P<tag_slug>\w+)",
        permission_classes=(permissions.IsAuthenticated,),
    )
    def tag(self, request, tag_slug, slug=None):
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
