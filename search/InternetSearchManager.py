import asyncio
import logging
import traceback

from channels.consumer import SyncConsumer

from common import statusUpdate
from common.searcherUtils import send_to_worker, INTERNET_SEARCH_MANAGER_NAME, send_to_websocket, WORKER_NAMES, \
    add_parent, TWITTER_URL_SEARCHER_NAME, DB_URL_SEARCHER_NAME, get_main_search
from common.url import is_valid, get_domain
from database.models import ImportedArticle
from googleCrawlerOfficial import patterns
from googleCrawlerOfficial.models import Domain, InternetResult
from search.models import Parent


def get_or_create(link, date, domain_str, domain):
    if InternetResult.objects.filter(link=link).exists():
        return InternetResult.objects.get(link=link)
    else:
        result = InternetResult(page=domain_str, date=date, link=link, domain=domain)
        result.save()
        return result


class Manager(SyncConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.name = INTERNET_SEARCH_MANAGER_NAME
        self.log(logging.INFO, 'Init')

    def log(self, level, message):
        logging.log(level, '[{0}] {1}'.format(self.name, message))

    def process_link(self, msg):
        #self.log(logging.INFO, 'Starting')
        try:
            asyncio.set_event_loop(asyncio.new_event_loop())
            link = msg['body']['link']
            date = patterns.retrieve_date(msg['body'].get('date'))
            main_search = get_main_search(msg['body']['search_id'])
            parent = Parent.from_dict(msg['body']['parent'])
            sender = msg['sender']

            if ImportedArticle.objects.filter(link=link).exists():
                statusUpdate.get(DB_URL_SEARCHER_NAME).queued()
                send_to_worker(self.channel_layer, sender=sender, where=DB_URL_SEARCHER_NAME,
                               method='search', body={
                        'link': link,
                        'search_id': main_search.id,
                        'parent': parent.to_dict()
                    })
            else:
                if is_valid(link) and main_search.link != link:
                    domain_str = get_domain(link)
                    domain, _ = Domain.objects.get_or_create(link=domain_str)
                    result = get_or_create(link, date, domain_str, domain)
                    add_parent(result, parent)

                    statusUpdate.get(TWITTER_URL_SEARCHER_NAME).queued()
                    send_to_worker(self.channel_layer, sender=sender, where=TWITTER_URL_SEARCHER_NAME,
                                   method='search', body={
                            'link': result.link,
                            'search_id': main_search.id,
                            'parent': Parent(id=result.link, type=self.name).to_dict()
                        })

                    if sender not in WORKER_NAMES:
                        send_to_websocket(self.channel_layer, where=sender, method='success', message='')

            #self.log(logging.INFO, 'Finished')

        except Exception as e:
            print(traceback.format_exc())
            self.log(logging.ERROR, 'Failed: {0}'.format(str(e)))
