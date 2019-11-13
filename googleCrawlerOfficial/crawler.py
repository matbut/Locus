import asyncio
import json
import logging
from urllib import request
from urllib.parse import quote

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer

from googleCrawlerOfficial import patterns
from search.models import CrawlParameters, SearchParameters
from .models import GoogleResultOfficial

logging.basicConfig(format='[%(asctime)s] %(message)s')
logging.getLogger().setLevel(logging.INFO)


class Crawler(SyncConsumer):
    def crawl(self, data):
        logging.info('Google crawler: starting')

        sender_id = data["id"]

        search_id = data["parameters"]
        search_parameters = SearchParameters.objects.get(id=search_id)

        query_raw = search_parameters.title
        query = quote(query_raw.encode('utf8'))

        key, engine_id = patterns.retrieve_access_key()
        response = request.urlopen('https://www.googleapis.com/customsearch/v1?key={0}&cx={1}&q={2}'
                                   .format(key, engine_id, query)).read()
        response_json = json.loads(response)

        items = response_json['items']
        for item in items:
            page = item['displayLink']
            date = patterns.retrieve_date(item['snippet'])
            link = item['link']
            search_result = GoogleResultOfficial(page=page, date=date, link=link)
            search_result.save()

        asyncio.set_event_loop(asyncio.new_event_loop())

        # Send message
        async_to_sync(self.channel_layer.group_send)(
            sender_id,
            {
                'type': 'send_done',
                'message': 'google_crawler'
            }
        )
