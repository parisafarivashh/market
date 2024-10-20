from rest_framework import serializers
from django.db.models import Sum, F
from ..models.cart import Cart


class CartDetailsSerializer(serializers.ModelSerializer):
    item_count = serializers.SerializerMethodField()
    payable_amount = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'payable_amount', 'item_count', 'status', 'order_date']

    @staticmethod
    def get_item_count(obj):
        quantity_sum = obj.cartItems.aggregate(sum=Sum('quantity'))
        return quantity_sum['sum']

    @staticmethod
    def get_payable_amount(obj):
        payable_amount = obj.cartItems \
            .annotate(total_price=F('quantity') * F('price')) \
            .aggregate(payable_amount=Sum('total_price'))

        return payable_amount['payable_amount']

