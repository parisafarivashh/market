from django.db import models
from .mixins import BaseModelMixin


class Product(BaseModelMixin):
    title = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product'

