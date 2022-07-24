from django.db import transaction
from django.db.models import Q
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

    # def create(self, validated_data):
    #     print(validated_data)
    #     with transaction.atomic():
    #         detail = validated_data['detail']
    #         print(detail)
    #         order = validated_data['order']
    #         item = ItemOrder.objects.filter(detail=detail)
    #         if len(item) == 0:
    #             item = ItemOrder.objects.create(**validated_data)
    #             final_count = validated_data['count']
    #
    #         else:
    #             object_item = item.first()
    #             final_count = 1
    #             object_item.count += final_count
    #             object_item.save(update_fields=['count'])
    #         print(detail.count)
    #         detail.count = detail.count - final_count
    #         print(detail.count)
    #         if detail.count < 0:
    #             raise ValueError('order number not available')
    #         detail.save(update_fields=['count'])
    #         return item


class UpdateItemOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOrder
        exclude = ['price', 'order']


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
        fields = ['id', 'items', 'final_cost']

    def to_representation(self, instance):
        data = super(ListOrderSerializer, self).to_representation(instance)
        data['items'] = ListItemOrder(instance=instance.items, many=True).data
        return data


