import asyncio
import logging
from urllib import request
from datetime import datetime
import json

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer

from search.models import CrawlParameters
from .models import GoogleResultOfficial

logging.basicConfig(format='[%(asctime)s] %(message)s')
logging.getLogger().setLevel(logging.INFO)


class Crawler(SyncConsumer):
    def crawl(self, data):
        logging.info('Google crawler: starting')

        sender_id = data["id"]

        crawl_parameters = CrawlParameters(data["parameters"])
        query = crawl_parameters.title

        key, engine_id = self.retrieve_access_key()
        url = 'https://www.googleapis.com/customsearch/v1?key={0}&cx={1}&q={2}'.format(key, engine_id, query)
        print("HTTP GET: ", url)
        response = request.urlopen(url).read()
        response_json = json.loads(response)
        print(response_json)

        items = response_json["items"]
        for item in items:
            page = item['displayLink']
            date = datetime.utcfromtimestamp(100000000 / 1000.0).date()
            #date = item['metatags'] find article:published_time
            link = item['link']
            search_result = GoogleResultOfficial(page=page, date=date, link=link)
            search_result.save()
            print(item)

        asyncio.set_event_loop(asyncio.new_event_loop())


        # Send message
        async_to_sync(self.channel_layer.group_send)(
            sender_id,
            {
                'type': 'send_done',
                'message': 'google_crawler'
            }
        )

    def retrieve_access_key(self):
        from pathlib import Path
        import re
        home_dir = str(Path.home())
        credentials = open("{0}/.locus/credentials".format(home_dir), "r")
        content = credentials.read()
        m = re.match(r"key (?P<key>\w+)\nengine_id (?P<engine_id>\w+:\w+)", content)
        key = m.groupdict()
        return key["key"], key["engine_id"]
