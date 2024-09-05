from rest_framework import serializers

from core.models import Category


class CategoryListCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['title', 'parent']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['children'] = CategoryListCreateSerializer(
                instance.childrens.all(),
                many=True
        ).data
        return data
