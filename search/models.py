from django.db import models


class CrawlParameters:
    def __init__(self, url="", title="", content="", twitter_search=False, google_search=False, db_search=False):
        self.url = url
        self.title = title
        self.content = content
        self.twitter_search = twitter_search
        self.google_search = google_search
        self.db_search = db_search

    def to_dict(self):
        return {
            'url': self.url,
            'title': self.title,
            'content': self.content,
            'twitter': self.twitter_search,
            'google': self.google_search,
            'db': self.db_search
        }

    @classmethod
    def from_dict(cls, dictionary):
        return CrawlParameters(
            url=dictionary['url'] if dictionary.get('url') else '',
            title=dictionary['title'] if dictionary.get('title') else '',
            content=dictionary['content'] if dictionary.get('content') else '',
            twitter_search=dictionary['twitter'] if dictionary.get('twitter') else False,
            google_search=dictionary['google'] if dictionary.get('google') else False,
            db_search=dictionary['db'] if dictionary.get('db') else False
        )


class SearchParameters(models.Model):
    url = models.TextField()
    title = models.TextField()
    content = models.TextField()

    twitter_search = models.BooleanField(default=False)
    google_search = models.BooleanField(default=False)
    db_search = models.BooleanField(default=False)

    @property
    def get_node_id(self):
        return 'search' + str(self.id)


class CrawlerStatus(models.Model):
    crawler = models.CharField(max_length=64, primary_key=True)
    in_progress = models.IntegerField(default=0)
    success = models.IntegerField(default=0)
    failure = models.IntegerField(default=0)

    @property
    def get_status_json(self):
        return {
            'working': self.in_progress,
            'completed': self.success,
            'failed': self.failure,
        }
