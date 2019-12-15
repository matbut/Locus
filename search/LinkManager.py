import asyncio
import logging
import traceback
from datetime import datetime

from channels.consumer import SyncConsumer
from django.db import transaction

from common import statusUpdate
from common.searcherUtils import send_to_worker, LINK_MANAGER_NAME, send_to_websocket, WORKER_NAMES, \
    add_parent, TWITTER_URL_SEARCHER_NAME, DB_URL_SEARCHER_NAME, get_main_search, search_cancelled
from common.url import is_valid, get_domain
from database.models import ImportedArticle
from searchEngine import patterns
from searchEngine.models import Domain, InternetResult
from search.models import Parent


def get_or_create(link, date, domain_str, domain, title, snippet):
    if InternetResult.objects.filter(link=link).exists():
        return InternetResult.objects.get(link=link)
    else:
        result = InternetResult(page=domain_str, date=date, link=link, domain=domain, title=title, snippet=snippet)
        result.save()
        return result


class Manager(SyncConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.name = LINK_MANAGER_NAME
        self.log(logging.INFO, 'Init')

    def log(self, level, message):
        logging.log(level, '[{0}] {1}'.format(self.name, message))

    def process_link(self, msg):

        main_search_id = msg['body']['search_id']
        updater = statusUpdate.get(self.name)
        updater.in_progress(main_search_id)

        if search_cancelled(main_search_id):
            self.log(logging.INFO, 'Search cancelled, finishing')
            updater.success(main_search_id)
            return

        try:
            asyncio.set_event_loop(asyncio.new_event_loop())
            link = msg['body']['link']
            date = datetime.fromtimestamp(int(msg['body'].get('date'))) if msg['body'].get('date') else None
            title = msg['body'].get('title') or ''
            snippet = msg['body'].get('snippet') or ''
            main_search = get_main_search(main_search_id)
            parent = Parent.from_dict(msg['body']['parent'])
            sender = msg['sender']

            if ImportedArticle.objects.filter(link=link).exists() and main_search.db_search:
                statusUpdate.get(DB_URL_SEARCHER_NAME).queued(main_search_id)
                send_to_worker(self.channel_layer, sender=sender, where=DB_URL_SEARCHER_NAME,
                               method='search', body={
                        'link': link,
                        'search_id': main_search.id,
                        'parent': parent.to_dict()
                    })
                return

            if is_valid(link) and main_search.link != link:
                try:
                    with transaction.atomic():
                        domain_str = get_domain(link)
                        domain, _ = Domain.objects.get_or_create(link=domain_str)
                        result = get_or_create(link, date, domain_str, domain, title, snippet)
                        add_parent(result, parent)

                        if main_search.twitter_search:
                            statusUpdate.get(TWITTER_URL_SEARCHER_NAME).queued(main_search_id)
                            send_to_worker(self.channel_layer, sender=sender, where=TWITTER_URL_SEARCHER_NAME,
                                           method='search', body={
                                    'link': result.link,
                                    'search_id': main_search.id,
                                    'parent': Parent(id=result.link, type=self.name).to_dict()
                                })
                except Exception as e:
                    self.log(logging.WARNING, 'Object was not added to database: {}'.format(str(e)))

                if sender not in WORKER_NAMES:
                    send_to_websocket(self.channel_layer, where=sender, method='success', message='')


        except Exception as e:
            print(traceback.format_exc())
            self.log(logging.ERROR, 'Failed: {0}'.format(str(e)))
