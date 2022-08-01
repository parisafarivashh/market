from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import Direct


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.group_name = None

    async def connect(self):
        user = self.scope['user']

        if user is None:
            print('*_* WS Closed: User was AnonymousUser')
            return await self.disconnect(code=4000)

        group = await get_direct(self.scope['url_route']['kwargs']['id'])
        if group is None:
            print('*_* WS Closed: Group Does Not Found')
            return await self.disconnect(4001)

        self.group_name = f'group_{group.id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def direct_message(self, event):
        message = event['text']
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_message',
                'message': message,
            }
        )

    async def send_message(self, event):
        message = event['message']
        print('SendMessage To websocket : ', message)
        await self.send(text_data=message)

    async def disconnect(self, code):
        await self.close(code)


@database_sync_to_async
def get_direct(id):
    try:
        return Direct.objects.get(id=id)
    except Direct.DoesNotExist:
        return None

