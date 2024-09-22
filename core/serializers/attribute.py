from rest_framework import serializers
from ..models.attribute import Attribute


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = ['title', 'value', 'product']
        extra_kwargs = {'product': {'required': False}}

