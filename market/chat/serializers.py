from rest_framework import serializers

from chat.models import Direct, Message


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Direct
        fields = ['receiver']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['text', 'direct', 'sender', 'receiver']
        extra_kwargs = {
            'sender': {'required': False},
            'receiver': {'required': False},
        }


class LatestMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['text', 'sender']


class ListChatSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Direct
        fields = ['title', 'date_create', 'last_message']

    def get_last_message(self, obj):
        messages = Message.objects.filter(direct=obj.id).order_by('-date_create').first()
        return LatestMessageSerializer(messages).data

