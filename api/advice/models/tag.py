from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel

from api.utils.models import UUIDModel, TitleSlugModel

from .utils import get_default_tag_type


class TagTypeManger(models.Manager):
    def default(self):
        return self.get_queryset().filter(slug="prochee").get()


class TagType(UUIDModel, TitleSlugModel, TimeStampedModel):

    objects = TagTypeManger()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Tag type")
        verbose_name_plural = _("Tag types")


class Tag(UUIDModel, TitleSlugModel, TimeStampedModel):

    type = models.ForeignKey(
        TagType, default=get_default_tag_type, on_delete=models.SET_DEFAULT
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")
        indexes = (models.Index(fields=("title",)),)
        unique_together = ("title", "slug")
