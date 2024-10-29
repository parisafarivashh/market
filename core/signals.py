from django.db.models.signals import post_save
from django.dispatch import receiver

from analytics.models import Activity
from analytics.signals import activity_signals


@receiver(post_save)
def model_post_save(sender, instance, created, **kwargs):
    if sender == Activity:
        return

    activity_type = 'create' if created else 'update'

    activity_signals.send(
        sender=sender,
        instance=instance,
        activity_type=activity_type,
    )

