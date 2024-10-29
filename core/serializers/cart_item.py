from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models.cart_item import CartItem
from ..models.variant import Variant
from ..models.cart import Cart
from ..serializers.product import ProductSerializer
from ..serializers.variant import VariantDetailSerializer


class CartItemSerializer(serializers.ModelSerializer):
    variant = serializers.PrimaryKeyRelatedField(
        queryset=Variant.objects.all()
    )

    class Meta:
        model = CartItem
        fields = ['variant']

    def create(self, validated_data):
        variant = validated_data['variant']

        cart, created = Cart.objects.get_or_create(
            user=self.context['request'].user,
            status='open'
        )

        if variant.number == 0:
            #ToDo send notif to user
            raise ValidationError(detail=dict(title=variant.product.title, count=variant.number))

        cart_item = cart.add_item(variant)
        cart.save()

        return cart_item


class CartItemListSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    variant = VariantDetailSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart_id', 'price', 'product', 'variant', 'quantity']


class RemoveCartItemSerializer(serializers.Serializer):
    cart_id = serializers.PrimaryKeyRelatedField(
        queryset=Cart.objects.all()
    )
    cart_item_id = serializers.PrimaryKeyRelatedField(
        queryset=CartItem.objects.all()
    )

    def validate(self, data):
        """Ensure that the cart item belongs to the cart."""
        cart = data['cart_id']
        cart_item = data['cart_item_id']

        if cart_item.cart != cart:
            raise serializers.ValidationError(detail=dict(
                cart_item_id= "This cart item does not belong to the provided cart."
            ))

        return data


class UpdateItemSerializer(RemoveCartItemSerializer):
    quantity = serializers.IntegerField(min_value=1)

