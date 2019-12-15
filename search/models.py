from django.db import models

from common.url import get_domain


class Parent:
    def __init__(self, id, type):
        self.id = id
        self.type = type

    def to_dict(self):
        return {
            'parent_id': self.id,
            'parent_type': self.type
        }

    @classmethod
    def from_dict(cls, dictionary):
        return Parent(
            id=dictionary['parent_id'],
            type=dictionary['parent_type']
        )


class Domain(models.Model):
    link = models.URLField(primary_key=True)

    @property
    def get_node_id(self):
        return 'domainUser' + str(self.link)

class SearchParameters(models.Model):
    link = models.TextField()
    title = models.TextField()
    content = models.TextField()

    twitter_search = models.BooleanField(default=False)
    google_search = models.BooleanField(default=False)
    db_search = models.BooleanField(default=False)

    domain = models.ForeignKey(Domain, null=True, on_delete=models.SET_NULL)

    @property
    def get_node_id(self):
        return 'search' + str(self.id)

    @classmethod
    def create(cls, link, title, content, twitter_search=False, google_search=False, db_search=False):
        domain, _ = Domain.objects.get_or_create(link=get_domain(link))
        return cls(link=link, title=title, content=content,
                   twitter_search=twitter_search, google_search=google_search, db_search=db_search,
                   domain=domain)


class SearcherStatus(models.Model):
    searcher = models.CharField(max_length=64, primary_key=True)
    queued = models.IntegerField(default=0)
    in_progress = models.IntegerField(default=0)
    success = models.IntegerField(default=0)
    failure = models.IntegerField(default=0)

    @property
    def get_status_json(self):
        return {
            'queued': self.queued,
            'working': self.in_progress,
            'completed': self.success,
            'failed': self.failure,
        }
