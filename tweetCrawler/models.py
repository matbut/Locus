from django.db import models

from googleCrawlerOfficial.models import GoogleResultOfficial
from search.models import SearchParameters


class Tweet(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    content = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    username = models.CharField(max_length=60)
    userlink = models.URLField()
    link = models.URLField()
    likes = models.IntegerField()
    replies = models.IntegerField()
    retweets = models.IntegerField()

    searches = models.ManyToManyField(SearchParameters)
    google = models.ManyToManyField(GoogleResultOfficial)

    @property
    def get_node_id(self):
        return 'tweet' + str(self.id)
