import string
import time

import random

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from channels.generic.websocket import WebsocketConsumer
import json


class Crawler(SyncConsumer):
    def process(self, data):
        time.sleep(data["duration"])
        print("crawler: processing finished - ", data["duration"])
        group_name = data["id"]
        # Send message to group
        async_to_sync(self.channel_layer.group_send)(
            group_name,
            {
                'type': 'components',
                'message': data["duration"]
            }
        )

class SomeComponent(SyncConsumer):
    def process(self, data):
        time.sleep(data["duration"])
        print("some component: processing finished - ", data["duration"])
        group_name = data["id"]
        # Send message to group
        async_to_sync(self.channel_layer.group_send)(
            group_name,
            {
                'type': 'components',
                'message': data["duration"]
            }
        )

class AnotherComponent(SyncConsumer):
    def process(self, data):
        time.sleep(data["duration"])
        print("another component: processing finished - ", data["duration"])
        group_name = data["id"]
        # Send message to group
        async_to_sync(self.channel_layer.group_send)(
            group_name,
            {
                'type': 'components',
                'message': data["duration"]
            }
        )

class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        async_to_sync(self.channel_layer.group_add)(
            self.id,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.id,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        print("RECEIVE")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        print("Sending messages to components")

        dur = int(message) / 3
        async_to_sync(self.channel_layer.send)("crawler", {"type": "process", "duration": dur, "id": self.id})
        async_to_sync(self.channel_layer.send)("some_component", {"type": "process", "duration": dur, "id": self.id})
        async_to_sync(self.channel_layer.send)("another_component", {"type": "process", "duration": dur, "id": self.id})
        print("Sent")

    # Receive message from room group
    def components(self, event):
        self.send("done")
