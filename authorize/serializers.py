from django.core.validators import RegexValidator
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



class BindSerializer(serializers.Serializer):
    phone_regex = RegexValidator(regex=r'9(\d{9})$')
    otp_code = serializers.CharField(max_length=4)
    country_code = serializers.IntegerField()
    phone_number = serializers.CharField(validators=[phone_regex])

    class Meta:
        fields = ['phone_number', 'country_code', 'otp_code']

