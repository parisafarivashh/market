from django.db import models, transaction


class CartItem(models.Model):
    product = models.ForeignKey('product', on_delete=models.PROTECT, related_name='cartItems')
    variant = models.ForeignKey('Variant', on_delete=models.PROTECT, related_name='cartItems')
    price = models.IntegerField()
    quantity = models.IntegerField(default=0)
    cart = models.ForeignKey('Cart', on_delete=models.PROTECT, related_name='cartItems')

    class Meta:
        db_table = 'cart_item'

    def update_quantity(self, quantity: int):
        with transaction.atomic():
            car_item = CartItem.objects.get(id=self.id)
            car_item.quantity = models.F('quantity') + quantity
            car_item.save(update_fields=['quantity'])

