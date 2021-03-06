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
        data['seller_id'] = SellerSerializer(instance=instance.seller_id).data
        details = Detail.objects.filter(product_id=instance.id)
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
    #         serializer_detail.validated_data['product_id'] = product
    #         Detail.objects.create(**serializer_detail.validated_data)
    #     return product


class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = '__all__'
        extra_kwargs = {
            'product_id': {'required': False},
        }

    def create(self, validated_data):
        # validated_data['product_id'] = product
        Detail.objects.create(**validated_data)

    def to_representation(self, instance):
        data = super(DetailSerializer, self).to_representation(instance)
        data['color_id'] = ColorSerializer(instance=instance.color_id).data
        return data

