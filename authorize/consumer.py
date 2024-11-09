import ujson
from channels.generic.websocket import AsyncWebsocketConsumer


# use AsyncJsonWebsocketConsumer
class UserConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        if user.is_authenticated:
            self.group_name = f'user__{user.id}'
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Here, you could handle incoming messages if necessary
        print('received text data')
        await self.send(text_data=ujson.dumps({'message': text_data}))

    async def create_product(self, event):
        await self.send(text_data=ujson.dumps(event["data"]))

