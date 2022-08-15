from rest_framework import serializers

from .models import Product, Detail, SubCategory
from admins.serializers import SubCategorySerializer, ColorSerializer

from user.serializers import SellerSerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        data = super(ProductSerializer, self).to_representation(instance)
        data['sub_category'] = SubCategorySerializer(instance=instance.sub_category).data
        details = Detail.objects.filter(product=instance.id)
        data['details'] = DetailSerializer(instance=details, many=True).data
        return data


class CreateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'description', 'sub_category']

    # because details dose not exist here we don`t write create serializer
    # def create(self, validated_data):
    #     details = validated_data.pop('details') details dose not exist here
    #     product = Product.objects.create(**validated_data)
    #     for detail in details:
    #         serializer_detail = DetailSerializer(data=detail)
    #         serializer_detail.is_valid(raise_exception=True)
    #         serializer_detail.validated_data['product'] = product
    #         Detail.objects.create(**serializer_detail.validated_data)
    #     return product


class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = '__all__'
        extra_kwargs = {
            'product': {'required': False},
        }

    def create(self, validated_data):
        # validated_data['product'] = product
        Detail.objects.create(**validated_data)

    def to_representation(self, instance):
        data = super(DetailSerializer, self).to_representation(instance)
        data['color'] = ColorSerializer(instance=instance.color).data
        data['product'] = CreateProductSerializer(instance=instance.product).data
        return data


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = ['id', 'color', 'product', 'size']

    def to_representation(self, instance):
        data = super(OrderDetailSerializer, self).to_representation(instance)
        data['color'] = ColorSerializer(instance=instance.color).data
        data['product'] = CreateProductSerializer(instance=instance.product).data
        return data


