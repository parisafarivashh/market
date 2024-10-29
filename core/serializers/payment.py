from rest_framework import serializers

from ..models import CartItem


class PaymentFailSerializer(serializers.ModelSerializer):
    variant_number = serializers.CharField(source='variant.number', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart_id', 'price', 'variant_id', 'variant_number',  'quantity']

