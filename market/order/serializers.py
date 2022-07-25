from rest_framework import serializers

from order.models import ItemOrder, Order
from product.serializers import OrderDetailSerializer


class ItemOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOrder
        fields = ['detail', 'order', 'count']
        extra_kwargs = {
            'order': {'required': False},
        }


class UpdateItemOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOrder
        exclude = ['price', 'order', 'detail']


class ListItemOrder(serializers.ModelSerializer):
    class Meta:
        model = ItemOrder
        fields = ['id', 'price', 'count', 'detail', 'cost']

    def to_representation(self, instance):
        data = super(ListItemOrder, self).to_representation(instance)
        data['detail'] = OrderDetailSerializer(instance=instance.detail).data
        return data


class ListOrderSerializer(serializers.ModelSerializer):
    final_cost = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ['id', 'items', 'final_cost', 'paid']

    def to_representation(self, instance):
        data = super(ListOrderSerializer, self).to_representation(instance)
        data['items'] = ListItemOrder(instance=instance.items, many=True).data
        return data


