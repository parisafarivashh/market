from rest_framework import serializers

from ..models import Variant
from ..models.cart import Cart
from .cart_item import CartItemSerializer


class CartDetailsSerializer(serializers.ModelSerializer):
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'payable_amount', 'item_count', 'status']

    @staticmethod
    def get_item_count(obj):
        return obj.cartItems.count()


