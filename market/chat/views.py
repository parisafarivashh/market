from django.db import transaction
from django.db.models import Q
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from chat.serializers import ChatSerializer, MessageSerializer, ListChatSerializer
from chat.models import Message, ChatMember, Direct
from rest_framework.response import Response

from user.models import User


class CreateDirect(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def post(self, request, *args, **kwargs):
        try:
            receiver = User.objects.get(id=request.data['receiver'])
        except User.DoesNotExist:
            raise NotFound

        first_name_group = f'chat_{self.request.user.id}_{receiver.id}'
        second_name_group = f'chat_{receiver.id}_{self.request.user.id}'
        print(first_name_group)
        print(second_name_group)
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
                print(serializer.data)

                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_200_OK)


class SendMessage(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def post(self, request, *args, **kwargs):
        direct = Direct.objects.get(id=request.data['direct'])
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['sender'] = self.request.user
        serializer.validated_data['receiver'] = direct.receiver

        Message.objects.create(**serializer.validated_data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        # bayad channel name user ro save konam ta be on user mostagim payam
        # befrestam.... vase notification khobe

        # ya id group begiram send konam to ws
        # harki ham connect mishe id group mide payam beshesh bedan mibine
        # ...real time mishe chat
        #api ham hast ta history sho begire


class ListAllChat(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ListChatSerializer

    def get_queryset(self):
        chat_member = ChatMember.objects.filter(member=self.request.user).values_list('direct', flat=True)
        return Direct.objects.filter(id__in=chat_member)


class ListMessageOfDirect(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    lookup_field = 'id'

