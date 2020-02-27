from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel

from api.utils.models import UUIDModel, TitleSlugModel


class Tag(UUIDModel, TitleSlugModel, TimeStampedModel):

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')
        indexes = (
            models.Index(fields=('title',)),
        )
        unique_together = ('title', 'slug')

class Advice(UUIDModel, TitleSlugModel, TimeStampedModel):
    """
    An advice model for storing usefull links.
    """

    link = models.URLField(_("uri link"))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_('advice tags'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("advice")
        verbose_name_plural = _("advices")
