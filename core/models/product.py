from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .mixins import BaseModelMixin


class Product(BaseModelMixin):
    creator = models.ForeignKey('authorize.User', on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')

    class Meta:
        db_table = 'product'


@receiver(post_save, sender=Product)
def created_product(created, instance, sender, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user__{instance.user.id}",
            {
                "type": "create_product",
                "data": {
                    "message": instance.item.to_dict(),
                },
            },
        )