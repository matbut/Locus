import asyncio
import json
import logging
import os
import traceback
from datetime import datetime
from urllib import request
from urllib.parse import quote

from channels.consumer import SyncConsumer

from common.searcherUtils import get_main_search, send_to_worker, GOOGLE_SEARCHER_NAME, LINK_MANAGER_NAME, \
    search_cancelled
from common import statusUpdate
from common.url import clean_url
from searchEngine import patterns
from search.models import Parent


def run_query(title):
    query_raw = title
    query = quote(query_raw.encode('utf8'))

    key, engine_id = os.environ.get('API_KEY'), os.environ.get('ENGINE_ID')
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

    def search_parameters_correct(self, msg):
        if not msg['body']['title']:
            self.log(logging.INFO, 'Title cannot be empty')
            return False
        return True

    def search(self, msg):
        self.log(logging.INFO, 'Starting')
        asyncio.set_event_loop(asyncio.new_event_loop())

        main_search_id = msg['body']['search_id']
        updater = statusUpdate.get(self.name)
        updater.in_progress(main_search_id)

        if search_cancelled(main_search_id):
            self.log(logging.INFO, 'Search cancelled, finishing')
            updater.success(main_search_id)
            return

        if not self.search_parameters_correct(msg):
            self.log(logging.INFO, 'Parameters incorrect, finishing')
            updater.success(main_search_id)
            return

        try:
            main_search = get_main_search(main_search_id)
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
                statusUpdate.get(LINK_MANAGER_NAME).queued(main_search_id)
                date = patterns.retrieve_date(item['snippet'])
                send_to_worker(self.channel_layer, sender=sender, where=LINK_MANAGER_NAME,
                               method='process_link', body={
                        'link': clean_url(item['link']),
                        'date': datetime.timestamp(date) if date else None,
                        'parent': parent.to_dict(),
                        'search_id': main_search.id,
                        'snippet': item['snippet'],
                        'title': item['title'].split('...')[0],
                    })

            updater.success(main_search_id)
            self.log(logging.INFO, 'Finished')

        except Exception as e:
            print(traceback.format_exc())
            updater.failure(main_search_id)
            self.log(logging.WARNING, 'Failed: {0}'.format(str(e)))
