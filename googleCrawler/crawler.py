from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from search.models import CrawlParameters

from googlesearch import search
import urllib.request as request

from .models import GoogleResult
import asyncio
from datetime import datetime

import logging
logging.basicConfig(format='[%(asctime)s] %(message)s')
logging.getLogger().setLevel(logging.INFO)


class Crawler(SyncConsumer):
    def crawl(self, data):
        logging.info('Google crawler: starting')

        sender_id = data["id"]

        crawl_parameters = CrawlParameters(data["parameters"])
        query = crawl_parameters.title

        for url in search(query, tld="com", lang="pl", num=10, start=0, stop=10, pause=2):
            print(url)
            #conn = request.urlopen(url)
            #print(conn.info())

        asyncio.set_event_loop(asyncio.new_event_loop())


        # Send message
        async_to_sync(self.channel_layer.group_send)(
            sender_id,
            {
                'type': 'send_done',
                'message': 'google_crawler'
            }
        )
