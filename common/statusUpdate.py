from django.db.models import F

from search.models import CrawlerStatus


class StatusUpdater:
    def __init__(self, crawler_name):
        self.crawler = crawler_name

    def in_progress(self):
        status = CrawlerStatus.objects.get(pk=self.crawler)
        status.in_progress = F('in_progress') + 1
        status.save()

    def success(self):
        status = CrawlerStatus.objects.get(pk=self.crawler)
        status.in_progress = F('in_progress') - 1
        status.success = F('success') + 1
        status.save()

    def failure(self):
        status = CrawlerStatus.objects.get(pk=self.crawler)
        status.in_progress = F('in_progress') - 1
        status.failure = F('failure') + 1
        status.save()
