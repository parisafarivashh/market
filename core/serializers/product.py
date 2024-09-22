from rest_framework import serializers

from ..models import Attribute, Variant
from ..models.product import Product

from .attribute import AttributeSerializer
from .variant import VariantSerializer



class ProductCreateSerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(many=True)
    variants = VariantSerializer(many=True)

    class Meta:
        model = Product
        fields = ['title', 'category']

    def create(self, validated_data):
        attributes = validated_data.pop('attributes')
        varaints = validated_data.pop('variants')

        product = Product.objects.create(**validated_data)

        instance_attributes = [Attribute(product=product, **attribute) for attribute in attributes]
        Attribute.objects.bulk_create(instance_attributes)

        instance_variant = [Variant(product=product, **variant) for variant in varaints]
        Variant.objects.bulk_create(instance_variant)

        return product

