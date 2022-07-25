from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from chat.serializers import ChatSerializer, MessageSerializer
from chat.models import PrivateChat

from chat.models import Message


class CreateChat(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def post(self, request, *args, **kwargs):
        try:
            receiver = Users.objects.get(id=request.data['id'])
        except Users.DoesNotExist:
            raise NotFound

        first_name_group = f'chat_{self.request.user.id}_{receiver.id}'
        second_name_group = f'chat_{receiver.id}_{self.request.user.id}'
        try:
            chat = PrivateChat.objects.get(Q(title=first_name_group) | Q(title=second_name_group))
        except PrivateChat.DoesNotExist:
            serializer = self.serializer_class(request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['creator'] = self.request.user
            chat = PrivateChat.objects.create(**serializer.validated_data)

            ChatMember.objects.create(chat=chat.id, member=self.request.user.id)
            ChatMember.objects.create(chat=chat.id, member=receiver.id)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class SendMessage(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def post(self, request, *args, **kwargs):
        chat = PrivateChat.objects.get(id=request.data['chat'])
        serializer = self.serializer_class(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['sender'] = self.request.user
        serializer.validated_data['receiver'] = chat.receiver

        Message.objects.create(**serializer.validated_data)

        # bayad channel name user ro save konam ta be on user mostagim payam
        # befrestam.... vase notification khobe

        # ya id group begiram send konam to ws
        # harki ham connect mishe id group mide payam beshesh bedan mibine
        # ...real time mishe chat
        #api ham hast ta history sho begire









