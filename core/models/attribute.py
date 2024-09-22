from django.db import models
from .mixins import BaseModelMixin
from .product import Product


class Attribute(BaseModelMixin):
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='attributes'
    )

    class Meta:
        db_table = 'attribute'

