import asyncio
import json
import logging
from urllib import request
from urllib.parse import quote

from channels.consumer import SyncConsumer

from common.searcherUtils import get_main_search, send_to_worker, GOOGLE_SEARCHER_NAME, INTERNET_SEARCH_MANAGER_NAME
from common import statusUpdate
from common.url import clean_url
from googleCrawlerOfficial import patterns
from search.models import Parent


def run_query(title):
    query_raw = title
    query = quote(query_raw.encode('utf8'))

    key, engine_id = patterns.retrieve_access_key()
    response = request.urlopen('https://www.googleapis.com/customsearch/v1?key={0}&cx={1}&q={2}'
                               .format(key, engine_id, query)).read()
    return json.loads(response)


class Searcher(SyncConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.awaited_components_number = 0
        self.name = GOOGLE_SEARCHER_NAME

    def log(self, level, message):
        logging.log(level, '[{0}] {1}'.format(self.name, message))

    def search(self, msg):
        self.log(logging.INFO, 'Starting')
        asyncio.set_event_loop(asyncio.new_event_loop())

        updater = statusUpdate.get(self.name)
        updater.in_progress()

        try:
            main_search = get_main_search(msg['body']['search_id'])
            title = msg['body']['title']
            link = msg['body']['link']
            parent = Parent.from_dict(msg['body']['parent'])
            sender = msg['sender']

            response_json = run_query(title)

            items = response_json['items']

            for item in items:
                if item['link'] == link:
                    continue
                # send to InternetSearchManager
                statusUpdate.get(INTERNET_SEARCH_MANAGER_NAME).queued()
                send_to_worker(self.channel_layer, sender=sender, where=INTERNET_SEARCH_MANAGER_NAME,
                               method='process_link', body={
                        'link': clean_url(item['link']),
                        'date': item['snippet'],
                        'parent': parent.to_dict(),
                        'search_id': main_search.id,
                    })

            updater.success()
            self.log(logging.INFO, 'Finished')

        except Exception as e:
            updater.failure()
            self.log(logging.WARNING, 'Failed: {0}'.format(str(e)))
