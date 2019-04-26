import json
import random
import string

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        async_to_sync(self.channel_layer.group_add)(
            self.id,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.id,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        print("RECEIVE")
        text_data_json = json.loads(text_data)
        url = text_data_json['url']
        #cp = CrawlParameters()
        #cp.Url = url

        # Send message to room group
        print("Sending messages to tweeter component")

        async_to_sync(self.channel_layer.send)("tweet_crawler",
                                               {"type": "crawl", "url": url, "id": self.id})
        print("Sent: ",url)

    # Receive message from room group
    def components(self, event):
        self.send("done")
