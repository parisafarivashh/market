from django.db import models


class Cart(models.Model):
    user = models.ForeignKey('authorize.User', on_delete=models.PROTECT, related_name='carts')
    cart_item = models.ForeignKey('CartItem', on_delete=models.PROTECT, related_name='carts')
    payable_amount = models.IntegerField()
    status = models.CharField(max_length=150, null=False, blank=False)

    class Meta:
        db_table = 'cart'

