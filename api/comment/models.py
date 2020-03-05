from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel

from api.utils.models import UUIDModel


class CommentQuerySet(models.QuerySet):
    """
    Comment model query set.
    """

    def advice_mean_score(self, advice: str):
        """
        Calculate a mean score for the advice.
        :param advice: advice uuid
        """
        return [
            *self.filter(advice_id=advice).aggregate(models.Avg("score")).values()
        ].pop()


class CommentManager(models.Manager):
    def get_queryset(self):
        return CommentQuerySet(model=self.model, using=self._db, hints=self._hints)

    def advice_mean_score(self, advice: str):
        """
        Get a mean score for the advice.
        :param advice: advice uuid
        """
        return self.get_queryset().advice_mean_score(advice)


class Comment(UUIDModel, TimeStampedModel):
    """
    A user comment left on an advice
    """

    body = models.TextField(_("a user comment"))
    score = models.DecimalField(
        verbose_name=_("a user score on the advice"),
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0),],  # noqa: E231
        default=0.0,
        max_digits=5,
        decimal_places=3,
    )
    advice = models.ForeignKey("advice.Advice", on_delete=models.PROTECT)
    author = models.ForeignKey("users.Account", on_delete=models.PROTECT)

    objects = CommentManager()

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
        unique_together = ("advice", "author")
