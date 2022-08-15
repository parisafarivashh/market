from rest_framework import serializers

from .models import User, Wallet


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'birth_date']


class UserPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.RegexField(regex=r'09(\d{9})$')


class SellerSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar']


class WalletDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['total_amount', 'can_withdraw_amount', 'amount_withdrawn']



