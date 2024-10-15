from django.db import models


class CartItem(models.Model):
    product = models.ForeignKey('product', on_delete=models.PROTECT, related_name='cartItems')
    variant = models.ForeignKey('Variant', on_delete=models.PROTECT, related_name='cartItems')
    price = models.IntegerField()
    number = models.IntegerField()

    class Meta:
        db_table = 'cart_item'

