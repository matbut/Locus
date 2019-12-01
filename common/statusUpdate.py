from django.db.models import F

from common.searcherUtils import DB_FTSEARCHER_NAME, DB_URL_SEARCHER_NAME, TWITTER_URL_SEARCHER_NAME, \
    TWITTER_TEXT_SEARCHER_NAME, GOOGLE_SEARCHER_NAME, INTERNET_SEARCH_MANAGER_NAME
from search.models import CrawlerStatus


class StatusUpdater:
    def __init__(self, crawler_name):
        self.crawler = crawler_name

    def queued(self):
        CrawlerStatus.objects.filter(pk=self.crawler).update(queued=F('queued') + 1)

    def in_progress(self):
        CrawlerStatus.objects.filter(pk=self.crawler).update(in_progress=F('in_progress') + 1)
        CrawlerStatus.objects.filter(pk=self.crawler).update(queued=F('queued') - 1)

    def success(self):
        CrawlerStatus.objects.filter(pk=self.crawler).update(in_progress=F('in_progress') - 1)
        CrawlerStatus.objects.filter(pk=self.crawler).update(success=F('success') + 1)

    def failure(self):
        CrawlerStatus.objects.filter(pk=self.crawler).update(in_progress=F('in_progress') - 1)
        CrawlerStatus.objects.filter(pk=self.crawler).update(failure=F('failure') + 1)


twitter_updater = StatusUpdater('twitter')
db_updater = StatusUpdater('db')
google_updater = StatusUpdater('google')
internet_manager_updater = StatusUpdater('manager')

updaters = {
    DB_FTSEARCHER_NAME: db_updater,
    DB_URL_SEARCHER_NAME: db_updater,
    TWITTER_URL_SEARCHER_NAME: twitter_updater,
    TWITTER_TEXT_SEARCHER_NAME: twitter_updater,
    GOOGLE_SEARCHER_NAME: google_updater,
    INTERNET_SEARCH_MANAGER_NAME: internet_manager_updater,
}


def get(worker_name):
    return updaters.get(worker_name)
