from django.db import models
from .cart_item import CartItem


class Cart(models.Model):
    user = models.ForeignKey('authorize.User', on_delete=models.PROTECT, related_name='carts')
    status = models.CharField(max_length=150, null=False, blank=False)

    class Meta:
        db_table = 'cart'

    def add_item(self, variant):
        """Add an item in the cart."""
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            variant=variant,
            price=variant.price,
            product=variant.product,
        )
        cart_item.quantity += 1
        cart_item.save()
        return cart_item

    def remove_item(self, item_id):
        return self.cartItems.filter(id=item_id).delete()

    def get_cart_data(self):
        from ..serializers.cart import CartDetailsSerializer
        from ..serializers.cart_item import CartItemListSerializer

        cart_data = CartDetailsSerializer(instance=self).data
        cart_items = CartItem.objects.filter(cart=self)
        cart_items_data = CartItemListSerializer(cart_items, many=True).data
        return dict(cart=cart_data, cart_items=cart_items_data)

