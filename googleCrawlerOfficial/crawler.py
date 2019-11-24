import asyncio
import json
import logging
from urllib import request
from urllib.parse import quote

from channels.consumer import SyncConsumer

from common.crawlerUtils import retrieve_params, group_send_message, send_message
from common.statusUpdate import StatusUpdater
from googleCrawlerOfficial import patterns
from search.models import CrawlParameters
from .models import GoogleResultOfficial

component = 'google'


def log(level, message):
    logging.log(level, '[google] {0}'.format(message))


def get_article_from_item(item):
    page = item['displayLink']
    date = patterns.retrieve_date(item['snippet'])
    link = item['link']
    return GoogleResultOfficial(page=page, date=date, link=link)


def run_query(title):
    query_raw = title
    query = quote(query_raw.encode('utf8'))

    key, engine_id = patterns.retrieve_access_key()
    response = request.urlopen('https://www.googleapis.com/customsearch/v1?key={0}&cx={1}&q={2}'
                               .format(key, engine_id, query)).read()
    return json.loads(response)


class Crawler(SyncConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.awaited_components_number = 0

    def crawl(self, data):
        log(logging.INFO, 'Starting')
        self.sender_id = data['id']
        asyncio.set_event_loop(asyncio.new_event_loop())

        updater = StatusUpdater('google_crawler')
        updater.in_progress()

        try:
            search_parameters, crawl_parameters = retrieve_params(data)
            response_json = run_query(crawl_parameters.title)

            items = response_json['items']
            search_results = []
            for item in items:
                search_result = get_article_from_item(item)
                search_result.save()
                search_results.append(search_result)

                if search_parameters is not None:
                    search_result.searches.add(search_parameters)

            updater.success()

            if crawl_parameters.twitter_search:
                self.send_tweeter_requests(search_results)
            else:
                group_send_message(component, self.channel_layer, self.sender_id, 'send_done', 'google_crawler')

        except Exception as e:
            updater.failure()
            group_send_message(component, self.channel_layer, self.sender_id, 'send_failure', 'google_crawler: {0}'.format(str(e)))

    def send_tweeter_requests(self, search_results):
        for result in search_results:
            crawl_parameters = CrawlParameters(url=result.link)
            send_message(component, self.channel_layer, 'tweet_crawler', {
                    'type': 'crawl',
                    'parameters': crawl_parameters.__dict__,
                    'google_id': result.link,
                    'id': 'google_crawler'
                })
            self.awaited_components_number += 1

    def send_done(self, data):
        self.awaited_components_number -= 1
        if self.awaited_components_number == 0:
            group_send_message(component, self.channel_layer, self.sender_id, 'send_done', 'google_crawler')

    def send_failure(self, data):
        log(logging.WARNING, data)
