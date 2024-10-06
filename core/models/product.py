from django.db import models
from .mixins import BaseModelMixin


class Product(BaseModelMixin):
    creator = models.ForeignKey('authorize.User', on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product'

