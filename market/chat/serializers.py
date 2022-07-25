from rest_framework import serializers

from chat.models import PrivateChat
from chat.models import Message


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrivateChat
        fields = ['title']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['text', 'chat', 'sender', 'receiver']