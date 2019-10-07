import asyncio
import logging
from urllib.parse import urlparse

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from googlesearch import search

from search.models import CrawlParameters
from .models import GoogleResult

logging.basicConfig(format='[%(asctime)s] %(message)s')
logging.getLogger().setLevel(logging.INFO)


class Crawler(SyncConsumer):
    def crawl(self, data):
        logging.info('Google crawler: starting')

        sender_id = data["id"]

        crawl_parameters = CrawlParameters(data["parameters"])
        query = crawl_parameters.title

        for url_result in search(query, tld="com", lang="pl", num=10, start=0, stop=5, pause=2):
            logging.info(f'Google crawler: saving {url_result}')
            search_result = GoogleResult(page=self.extract_page(url_result), link=url_result)
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

    def extract_page(self, link):
        res = urlparse(link)
        return res.netloc
