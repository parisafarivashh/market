from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .models import Notifications


class UserConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']

        if self.user is None:
            print('*_* WS Closed: User was AnonymousUser')
            return await self.disconnect(code=3001)

        self.group_name = f"User-Notification-{self.user.id}"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    # receive message from websocket. we don`t need them
    async def receive_json(self, content, **kwargs):
        print(content)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_notification',
                'text': content
            }
        )

    async def send_notification(self, event):
        print('akkkkkkkkkkkkkkk')
        message = event['text']
        await create_notif(self.user, message)

        print('SendMessage To websocket : ', message)
        await self.send(text_data=message)

    async def disconnect(self, code):
        await self.close(code)


@database_sync_to_async
def create_notif(user, text):
    print('hereeeeeeee')
    return Notifications.objects.create(user=user, text=text)
