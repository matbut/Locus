import json
import logging
import random
import string

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from common import searcherUtils, statusUpdate
from common.searcherUtils import send_to_worker, MAIN_SEARCH_NAME
from common.url import clean_url
from database.models import ResultArticle, TopWord
from search.models import SearchParameters, SearcherStatus, Parent, Domain
from searchEngine.models import InternetResult
from twitter.models import Tweet, TwitterUser

logging.basicConfig(format='[%(asctime)s] %(message)s')
logging.getLogger().setLevel(logging.INFO)


class Broker(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jobs = 0

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
        self.reset_crawler_status()

        text_data_json = json.loads(text_data)

        search_parameters = SearchParameters.create(
            link=clean_url(text_data_json['url']),
            title=text_data_json['title'],
            content=text_data_json['content'],
            twitter_search=text_data_json['twitter'],
            google_search=text_data_json['google'],
            db_search=text_data_json['db']
        )
        search_parameters.save()

        if search_parameters.twitter_search:
            self.send_search_request(searcherUtils.TWITTER_URL_SEARCHER_NAME, text_data_json, search_parameters.id)
            self.send_search_request(searcherUtils.TWITTER_TEXT_SEARCHER_NAME, text_data_json, search_parameters.id)

        if search_parameters.google_search:
            self.send_search_request(searcherUtils.GOOGLE_SEARCHER_NAME, text_data_json, search_parameters.id)

        if search_parameters.db_search:
            self.send_search_request(searcherUtils.DB_FTSEARCHER_NAME, text_data_json, search_parameters.id)

    def success(self, signal):
        logging.info(signal)
        # send info to web socket if first response received
        if self.jobs > 0:
            self.send('done')
        self.jobs = 0


    def send_search_request(self, where, text_data_json, search_parameters_id, search_type='search'):
        logging.info('Sending request to {0} component'.format(where))
        statusUpdate.get(where).queued(search_parameters_id)
        send_to_worker(self.channel_layer, sender=self.id, where=where, method=search_type, body={
            'link': clean_url(text_data_json['url']),
            'title': text_data_json['title'],
            'search_id': search_parameters_id,
            'parent': Parent(id=search_parameters_id, type=MAIN_SEARCH_NAME).to_dict(),
        })
        self.jobs += 1

    def delete_tables(self):
        SearcherStatus.objects.all().delete()
        TwitterUser.objects.all().delete()
        Tweet.objects.all().delete()
        InternetResult.objects.all().delete()
        ResultArticle.objects.all().delete()
        TopWord.objects.all().delete()
        SearchParameters.objects.all().delete()
        Domain.objects.all().delete()

    def reset_crawler_status(self):
        for crawler in ['twitter', 'google', 'db']:
            if SearcherStatus.objects.filter(pk=crawler).exists():
                SearcherStatus.objects.filter(pk=crawler).update(queued=0, in_progress=0, success=0, failure=0)
            else:
                SearcherStatus(searcher=crawler).save()
