import json

import ujson
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction
from django.db.models import Q
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, UpdateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import CantSeenOwnMessage
from .serializers import CreateDirectSerializer, MessageSerializer, \
    ListChatSerializer, UpdateMessageSerializer, DirectMessageSerializer, \
    SeenMessageSerializer
from .models import Message, ChatMember, Direct

from user.models import User


class CreateDirect(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateDirectSerializer

    def post(self, request, *args, **kwargs):
        try:
            receiver = User.objects.get(id=request.data['receiver'])
        except User.DoesNotExist:
            raise NotFound

        first_name_group = f'chat_{self.request.user.id}_{receiver.id}'
        second_name_group = f'chat_{receiver.id}_{self.request.user.id}'

        with transaction.atomic():
            try:
                chat = Direct.objects.get(Q(title=first_name_group) | Q(title=second_name_group))
            except Direct.DoesNotExist:
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.validated_data['creator'] = self.request.user
                serializer.validated_data['title'] = first_name_group
                direct = Direct.objects.create(**serializer.validated_data)

                ChatMember.objects.create(direct=direct, member=self.request.user)
                ChatMember.objects.create(direct=direct, member=receiver)

                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_200_OK)


class SendMessage(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def post(self, request, *args, **kwargs):
        try:
            direct = Direct.objects.get(id=request.data['direct'])
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['sender'] = self.request.user
            serializer.validated_data['receiver'] = direct.receiver

            message = Message.objects.create(**serializer.validated_data)

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'group_{direct.id}',
                {
                    'type': 'direct_message',
                    'text': json.dumps(
                        MessageSerializer(instance=message).data)
                }
            )
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'User-Notification-{direct.receiver.id}',
                {
                    'type': 'send_notification',
                    'text': ujson.dumps(
                        dict(text=message.text, sender=self.request.user.phone_number)
                    )
                }

            )
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Direct.DoesNotExist:
            return Response(data={'direct does not exist '}, status=status.HTTP_400_BAD_REQUEST)


class ListAllChat(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ListChatSerializer

    def get_queryset(self):
        chat_member = ChatMember.objects.filter(member=self.request.user).values_list('direct', flat=True)
        return Direct.objects.filter(id__in=chat_member)


class ListMessageOfDirect(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DirectMessageSerializer

    def get(self, request, id):
        try:
            direct = Direct.objects.get(id=id)
        except Direct.DoesNotExist:
            return Response(data={'Direct Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)
        message = Message.objects.filter(direct=direct)
        message.update(seen=True)

        text = self.request.query_params.get('text', None)
        if text is not None:
            message = message.filter(text__startswith=text)

        serializer = DirectMessageSerializer(message, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class DeleteOrUpdateMessage(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateMessageSerializer
    queryset = Message.objects.all()
    lookup_field = 'id'


class SeenMessage(UpdateAPIView):
    permission_classes = [IsAuthenticated, CantSeenOwnMessage]
    serializer_class = SeenMessageSerializer
    queryset = Message.objects.all()
    lookup_field = 'id'

