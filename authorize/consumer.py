from channels.generic.websocket import AsyncJsonWebsocketConsumer


class UserConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        self.group_name = 'aaa'
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
        await self.send(text_data={'message': text_data})

    async def send_data(self, event):
        await self.send(text_data=event["data"])

