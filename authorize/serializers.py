from rest_framework import serializers

from .models import User


class RegisterSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['title', 'phone_number', 'country_code', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }


class OtpSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['phone_number', 'country_code']

