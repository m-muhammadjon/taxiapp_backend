import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from account.models import User


@sync_to_async()
def user_change(user_id, connected=False):
    user = User.objects.get(id=user_id)
    if connected:
        user.is_online = True
    else:
        user.is_online = False
    user.save()


class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'user_%s' % self.scope['url_route']['kwargs']['user_id']
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'order_message', 'msg': 'connected'}
        )
        await user_change(self.scope['url_route']['kwargs']['user_id'], True)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(self.room_group_name, 'closed')
        await user_change(self.scope['url_route']['kwargs']['user_id'])

    async def receive(self, text_data=None, bytes_data=None):
        print('receive')
        # print(type(text_data))
        text_data_json = json.loads(text_data)
        print(text_data_json)
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'order_message',
                'data': text_data_json
            }
        )

    async def order_message(self, event):
        print('driver_msg')
        # print(event)
        await self.send(text_data=json.dumps(event))
