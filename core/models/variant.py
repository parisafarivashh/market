from django.db import models
from .mixins import BaseModelMixin
from .product import Product


class ManagerVariant(models.Manager):

    def not_removed(self):
        return self.filter(removed_at__isnull=True)

    def removed(self):
        return self.filter(removed_at__isnull=False)


class Variant(BaseModelMixin):
    number = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    color = models.CharField(max_length=50, blank=True, null=True)
    material = models.CharField(max_length=50, blank=True, null=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )

    objects = ManagerVariant()

    class Meta:
        db_table = 'variant'

