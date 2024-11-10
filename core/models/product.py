from django.db import models

from .mixins import BaseModelMixin


class Product(BaseModelMixin):
    creator = models.ForeignKey('authorize.User', on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')

    class Meta:
        db_table = 'product'


#@receiver(post_save, sender=Product)
#def created_product(created, instance, sender, **kwargs):
#    from ..serializers import ProductListSerializer

#    if created:
#        channel_layer = get_channel_layer()
#        async_to_sync(channel_layer.group_send)(
#            f"user__{instance.creator.id}",
#            {
#                "type": "create_product",
#                "data": {
#                    "product": ProductListSerializer(instance).data,
#                },
#            },
#        )
