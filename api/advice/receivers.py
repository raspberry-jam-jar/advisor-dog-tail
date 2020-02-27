from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Advice, Tag


@receiver(post_save, sender=Advice)
def add_default_tag(sender, instance, created, **kwargs):
    """
    Try to add default tag to the advice model
    if it doesn't have any
    """
    if created:
        if not instance.tags.exists():
            # Add tag prochee by default
            instance.tags.add(
                Tag.objects.filter(slug='prochee').get()
            )