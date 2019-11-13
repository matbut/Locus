import asyncio
import json
import logging
from urllib import request
from urllib.parse import quote

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer

from googleCrawlerOfficial import patterns
from search.models import SearchParameters
from .models import GoogleResultOfficial

logging.basicConfig(format='[%(asctime)s] %(message)s')
logging.getLogger().setLevel(logging.INFO)


class Crawler(SyncConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.awaited_components_number = 0

    def crawl(self, data):
        logging.info('Google crawler: starting')

        self.sender_id = data["id"]

        search_id = data["parameters"]
        search_parameters = SearchParameters.objects.get(id=search_id)

        query_raw = search_parameters.title
        query = quote(query_raw.encode('utf8'))

        key, engine_id = patterns.retrieve_access_key()
        response = request.urlopen('https://www.googleapis.com/customsearch/v1?key={0}&cx={1}&q={2}'
                                   .format(key, engine_id, query)).read()
        response_json = json.loads(response)

        items = response_json['items']
        search_results = []
        for item in items:
            page = item['displayLink']
            date = patterns.retrieve_date(item['snippet'])
            link = item['link']
            search_result = GoogleResultOfficial(page=page, date=date, link=link)
            search_result.save()
            search_results.append(search_result)

            search_result.searches.add(search_parameters)

        self.send_tweeter_requests(search_results)

    def send_tweeter_requests(self, search_results):
        for result in search_results:
            search_parameters = SearchParameters(
                url=result.link,
                title="",
                content=""
            )
            search_parameters.save()

            logging.info("[google_search] Sending parameters to tweeter component")
            async_to_sync(self.channel_layer.send)(
                "tweet_crawler",
                {
                    "type": "crawl",
                    "parameters": search_parameters.id,
                    "id": "google_crawler"
                }
            )
            self.awaited_components_number += 1

    def send_done(self, data):
        self.awaited_components_number -= 1
        logging.info(data)

        if self.awaited_components_number == 0:
            asyncio.set_event_loop(asyncio.new_event_loop())
            # Send message
            async_to_sync(self.channel_layer.group_send)(
                self.sender_id,
                {
                    'type': 'send_done',
                    'message': 'google_crawler'
                }
            )
