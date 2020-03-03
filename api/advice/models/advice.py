from django.db import models

from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel

from api.utils.models import UUIDModel, TitleSlugModel

from .tag import Tag


class Advice(UUIDModel, TitleSlugModel, TimeStampedModel):
    """
    An advice model for storing useful links.
    """

    link = models.URLField(_("uri link"))
    author = models.ForeignKey(
        "users.Account",
        on_delete=models.PROTECT,
        verbose_name=_("author of the advice"),
    )
    tags = models.ManyToManyField(
        Tag, blank=True, through="Mapping", verbose_name=_("advice's tags")
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("advice")
        verbose_name_plural = _("advices")


class Mapping(UUIDModel, TimeStampedModel):
    """
    Mapping entry between advice and tag model instance
    """

    tag = models.ForeignKey("advice.Tag", on_delete=models.CASCADE)
    advice = models.ForeignKey("advice.Advice", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("advice's tags")
        verbose_name_plural = _("advices' tags")
        unique_together = ("tag", "advice")
        indexes = (models.Index(fields=("tag", "advice")),)
