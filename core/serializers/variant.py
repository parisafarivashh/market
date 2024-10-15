from rest_framework import serializers
from ..models.variant import Variant


class VariantSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
    #price = serializers.SerializerMethodField()

    class Meta:
        model = Variant
        fields = ['id', 'number', 'price', 'color', 'material', 'product']
        extra_kwargs = {'product': {'required': False}}

    def to_representation(self, instance):
        from .product import ProductSerializer
        data = super().to_representation(instance)
        data['product'] = ProductSerializer(instance.product).data
        return data

    #def get_price(self, obj):
    #    return float(obj.price)


class VariantDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Variant
        fields = ['id', 'number', 'price', 'color', 'material']

