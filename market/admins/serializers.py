from rest_framework import serializers

from .models import Admin, AdminPermissions
from product.models import Color, Category, SubCategory


class CreateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        exclude = ['super_admin',]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone_number': {'required': True},
            'email': {'required': True},
            'avatar': {'required': False}
        }


class GetAdminPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model   = AdminPermissions
        exclude = ['id', 'admin_id']


class GetAdminSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField('get_permission')

    class Meta:
        model = Admin
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'avatar', 'permissions']

    def get_permission(self, obj):
        try:
            return GetAdminPermissionsSerializer(obj.adminpermissions).data
        except Admin.adminpermissions.RelatedObjectDoesNotExist:
            return GetAdminPermissionsSerializer(None).data


class UpdateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        exclude = ['password', 'last_login']
        extra_kwargs = {
            'username': {'required': False},
            'avatar': {'required': False}
        }


class GetAdminPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminPermissions
        fields = ['id', 'admin_id']


class AdminPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminPermissions
        exclude = ['admin_id']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = ['name', 'category_id']
        depth = 1


class CreateSubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = ['name', 'category_id']

