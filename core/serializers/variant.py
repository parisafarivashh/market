from rest_framework import serializers
from ..models.variant import Variant


class VariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Variant
        fields = ['number', 'price', 'color', 'material', 'product']
        extra_kwargs = {'product': {'required': False}}

