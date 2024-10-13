from rest_framework import serializers

from ..models import Attribute, Variant
from ..models.product import Product

from .attribute import AttributeSerializer
from  .category import CategoryListCreateSerializer


class ProductCreateSerializer(serializers.ModelSerializer):
    from .variant import VariantSerializer

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

        self._bulk_create_attributes(product, attributes)
        self._bulk_create_variants(product, variants)

        return product

    @staticmethod
    def _bulk_create_attributes(product, attributes):
        """Helper function to bulk create attributes."""
        if attributes:
            instance_attributes = \
                [Attribute(product=product, **attr) for attr in attributes]
            Attribute.objects.bulk_create(instance_attributes)

    @staticmethod
    def _bulk_create_variants(product, variants):
        """Helper function to bulk create variants."""
        if variants:
            instance_variants = \
                [Variant(product=product, **variant) for variant in variants]
            Variant.objects.bulk_create(instance_variants)


class ProductListSerializer(serializers.ModelSerializer):
    from .variant import VariantSerializer

    category = CategoryListCreateSerializer(read_only=True)
    creator_title = serializers.ReadOnlyField(source='creator.title')
    attributes = AttributeSerializer(many=True, read_only=True, source='attributes.all')
    variants = VariantSerializer(many=True, read_only=True, source='variants.all')


    class Meta:
        model = Product
        fields = ['id', 'title', 'category', 'creator', 'creator_title', 'attributes', 'variants']

    #def to_representation(self, instance):
    #    data = super().to_representation(instance)
    #    data['attributes'] = AttributeSerializer(instance.attributes.all(), many=True).data
    #    data['variants'] = VariantSerializer(instance.variants.all(), many=True).data
    #    return data


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'category']

    def to_representation(self, instance):
        from .variant import VariantSerializer

        data = super().to_representation(instance)
        data['category'] = CategoryListCreateSerializer(instance.category).data
        data['attributes'] = AttributeSerializer(instance.attributes.all(), many=True).data
        data['variants'] = VariantSerializer(instance.variants.all(), many=True).data
        return data


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryListCreateSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'category']


