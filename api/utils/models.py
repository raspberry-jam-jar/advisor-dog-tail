import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from django_extensions.db.fields import AutoSlugField


class UUIDModel(models.Model):
    """
    An abstract base class model with a UUID as its primary key.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TitleSlugModel(models.Model):
    """
    TitleSlugModel

    An abstract base class model that provides title field and
    a self-managed "slug" field that populates from the title.

    .. note ::
        If you want to use custom "slugify" function, you could
        define ``slugify_function`` which then will be used
        in :py:class:`AutoSlugField` to slugify ``populate_from`` field.

        See :py:class:`AutoSlugField` for more details.
    """

    title = models.CharField(_("title"), max_length=255)
    slug = AutoSlugField(_("slug"), populate_from="title")

    class Meta:
        abstract = True
