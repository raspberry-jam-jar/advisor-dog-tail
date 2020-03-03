from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel

from api.utils.models import UUIDModel, TitleSlugModel


class Advice(UUIDModel, TitleSlugModel, TimeStampedModel):
    """
    An advice model for storing usefull links.
    """

    link = models.URLField(_("uri link"))
    author = models.ForeignKey(
        "users.Account",
        on_delete=models.PROTECT,
        verbose_name=_("author of the advice"),
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("advice")
        verbose_name_plural = _("advices")
