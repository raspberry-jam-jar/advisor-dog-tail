from django.dispatch import receiver
from django.db.models.signals import post_save

from .models.advice import Advice
from .models.tag import Tag


@receiver(post_save, sender=Advice)
def add_default_tag(sender, instance, created, **kwargs):
    """Add default tag in case of none of them has the advice instance."""
    if instance.tags.count() < 1:
        instance.tags.add(Tag.objects.default())
    elif instance.tags.count() > 1:
        instance.tags.filter(slug=Tag.objects.default().slug).delete()
