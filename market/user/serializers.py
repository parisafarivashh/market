import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import serializers

from .models import User, Wallet


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'birth_date']

    def update(self, instance, validated_data):
        super(UserProfileSerializer, self).update(instance, validated_data=validated_data)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'update_user',
            {'type': 'send_message', 'text': json.dumps(UserProfileSerializer(instance=instance).data)}
        )
        return instance


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



