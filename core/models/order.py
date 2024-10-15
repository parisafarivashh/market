from django.db import models


class Order(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.PROTECT, related_name='Orders')
    status = models.CharField(max_length=150, null=False, blank=False)
    payable_amount = models.IntegerField()

    class Meta:
        db_table = 'order'

