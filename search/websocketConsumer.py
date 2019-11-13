import json
import random
import string
import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from database.models import ResultArticle
from googleCrawlerOfficial.models import GoogleResultOfficial
from search.models import SearchParameters
from tweetCrawler.models import Tweet

logging.basicConfig(format='[%(asctime)s] %(message)s')
logging.getLogger().setLevel(logging.INFO)


class WSConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.awaited_components_number = 0

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
        self.delete_tables()

        search_parameters = SearchParameters(
            url=text_data_json['url'],
            title=text_data_json['title'],
            content=text_data_json['content']
        )
        search_parameters.save()


        if text_data_json['twitter']:
            logging.info("Sending parameters to tweeter component")
            async_to_sync(self.channel_layer.send)("tweet_crawler",
                                                   {"type": "crawl", "parameters": search_parameters.id, "id": self.id})
            self.awaited_components_number += 1

        if text_data_json['google']:
            logging.info("Sending parameters to google search component")
            async_to_sync(self.channel_layer.send)("google_crawler",
                                                   {"type": "crawl", "parameters": search_parameters.id, "id": self.id})
            self.awaited_components_number += 1

        if text_data_json['db']:
            logging.info("Sending parameters to database search component")
            async_to_sync(self.channel_layer.send)("db_searcher",
                                                   {"type": "search", "parameters": cp.__dict__, "id": self.id})
            self.awaited_components_number += 1

    def send_done(self, signal):
        logging.info(signal)
        self.awaited_components_number -= 1
        if self.awaited_components_number == 0:
            self.send("done")

    def delete_tables(self):
        Tweet.objects.all().delete()
        GoogleResultOfficial.objects.all().delete()
        ResultArticle.objects.all().delete()
        SearchParameters.objects.all().delete()
