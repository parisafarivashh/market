from channels.generic.websocket import AsyncWebsocketConsumer


class UserConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']

        if self.user is None:
            print('*_* WS Closed: User was AnonymousUser')
            return await self.disconnect(code=3001)

        await self.channel_layer.group_add(
            'update_user',
            self.channel_name
        )

        await self.accept()

    # receive message from websocket. we don`t need them
    # async def receive(self, text_data):
    #     await self.channel_layer.group_send(
    #         'update_user',
    #         {
    #             'type': 'send_message',
    #             'text': text_data
    #         }
    #     )

    async def send_message(self, event):
        message = event['text']
        print('SendMessage To websocket : ', message)
        await self.send(text_data=message)

    async def disconnect(self, code):
        await self.close(code)


