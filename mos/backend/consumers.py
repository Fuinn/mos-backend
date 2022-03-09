import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class NotificationsConsumer(WebsocketConsumer):

    def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['user_id']
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        notification = json.loads(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'mos_notification',
                'notification': notification
            }
        )

    def mos_notification(self, event):
        notification = event['notification']
        self.send(text_data=json.dumps(notification))