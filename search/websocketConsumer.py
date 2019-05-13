import json
import random
import string

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from tweetCrawler.models import CrawlParameters


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
        text_data_json = json.loads(text_data)
        cp = CrawlParameters(text_data_json)

        if cp.twitter:
            print("Sending parameters to tweeter component")
            async_to_sync(self.channel_layer.send)("tweet_crawler",
                                                   {"type": "crawl", "parameters": cp.__dict__, "id": self.id})

    def send_done(self, event):
        self.send("done")
