from rest_framework import serializers

from ..models import Attribute, Variant
from ..models.product import Product

from .attribute import AttributeSerializer
from .variant import VariantSerializer

from  .category import CategoryListCreateSerializer



class ProductCreateSerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(many=True, required=False)
    variants = VariantSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'title', 'category', 'attributes', 'variants', 'creator']
        extra_kwargs = {'creator': {'required': False}}


    def create(self, validated_data):
        print(validated_data)
        attributes = validated_data.pop('attributes', None)
        variants = validated_data.pop('variants', None)

        product = Product.objects.create(**validated_data)

        if attributes:
            instance_attributes = [Attribute(product=product, **attribute) for attribute in attributes]
            Attribute.objects.bulk_create(instance_attributes)

        if variants:
            instance_variant = [Variant(product=product, **variant) for variant in variants]
            Variant.objects.bulk_create(instance_variant)

        return product


class ProductListSerializer(serializers.ModelSerializer):
    category = CategoryListCreateSerializer(read_only=True)
    creator_title = serializers.ReadOnlyField(source='creator.title')

    class Meta:
        model = Product
        fields = ['id', 'title', 'category', 'creator', 'creator_title']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['attributes'] = AttributeSerializer(instance.attributes.all(), many=True).data
        data['variants'] = VariantSerializer(instance.variants.all(), many=True).data
        return data


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'category']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = CategoryListCreateSerializer(instance.category).data
        data['attributes'] = AttributeSerializer(instance.attributes.all(), many=True).data
        data['variants'] = VariantSerializer(instance.variants.all(), many=True).data
        return data

