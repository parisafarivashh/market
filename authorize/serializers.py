
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class RegisterSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['title', 'phone_number', 'country_code', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }


class PhoneSerializer(serializers.Serializer):
    phone_regex = RegexValidator(regex=r'^9(\d{9})$')
    phone_number = serializers.CharField(validators=[phone_regex])

    class Meta:
        fields = ['phone_number', 'country_code']


class OtpSerializer(PhoneSerializer):
    otp_code = serializers.CharField(max_length=4)

    class Meta:
        fields = ['phone_number', 'country_code', 'otp_code']


class UserListSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'title', 'first_name', 'last_name', 'phone_number',
                  'country_code', 'is_staff', 'date_joined']

