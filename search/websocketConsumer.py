import json
import logging
import random
import string

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from database.models import ResultArticle
from googleCrawlerOfficial.models import GoogleResultOfficial
from search.models import SearchParameters, CrawlParameters
from tweetCrawler.models import Tweet, TwitterUser

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
        self.delete_tables()

        text_data_json = json.loads(text_data)

        crawl_parameters = CrawlParameters.from_dict(text_data_json)
        search_parameters = SearchParameters(
            url=text_data_json['url'],
            title=text_data_json['title'],
            content=text_data_json['content'],
            twitter_search=text_data_json['twitter'],
            google_search=text_data_json['google'],
            db_search=text_data_json['db']
        )
        search_parameters.save()

        if crawl_parameters.twitter_search:
            self.send_message('tweet_crawler', 'crawl', crawl_parameters, search_parameters.id)

        if crawl_parameters.google_search:
            self.send_message('google_crawler', 'crawl', crawl_parameters, search_parameters.id)

        if crawl_parameters.db_search:
            self.send_message('db_searcher', 'search', crawl_parameters, search_parameters.id)

    def send_done(self, signal):
        logging.info(signal)
        self.awaited_components_number -= 1
        if self.awaited_components_number == 0:
            self.send('done')

    def send_failure(self, signal):
        logging.warning('Failure: ', signal)

    def send_message(self, where, search_type, crawl_parameters, search_parameters_id):
        logging.info('Sending parameters to {0} component'.format(where))
        async_to_sync(self.channel_layer.send)(
            where,
            {
                'type': search_type,
                'parameters': crawl_parameters.to_dict(),
                'search_id': search_parameters_id,
                'id': self.id
            }
        )

        self.awaited_components_number += 1

    def delete_tables(self):
        TwitterUser.objects.all().delete()
        Tweet.objects.all().delete()
        GoogleResultOfficial.objects.all().delete()
        ResultArticle.objects.all().delete()
        SearchParameters.objects.all().delete()
