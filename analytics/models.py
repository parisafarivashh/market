from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.dispatch import receiver

from .signals import activity_signals


class Activity(models.Model):
    created_at = models.DateField(auto_now_add=True)
    activity_type = models.CharField(max_length=100)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'activity'


@receiver(signal=activity_signals)
def create_activity(sender, instance, activity_type, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)

    Activity.objects.create(
       activity_type=activity_type,
       content_type=c_type,
       object_id=instance.id,
    )

