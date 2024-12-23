from django.db import models

from .mixins import BaseModelMixin
from .product import Product


class AttributeManager(models.Manager):

    def not_removed(self):
        return self.filter(removed_at__isnull=True)

    def removed(self):
        return self.filter(removed_at__isnull=False)


class Attribute(BaseModelMixin):
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='attributes'
    )

    objects = AttributeManager()

    class Meta:
        db_table = 'attribute'

