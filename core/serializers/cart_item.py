from rest_framework import serializers

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

        try:
            cart_item = CartItem.objects.get(variant=variant, cart=cart)
            cart_item.quantity += 1
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                variant=variant,
                product=variant.product,
                cart=cart,
                price=variant.price,
                quantity=1,
            )

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

