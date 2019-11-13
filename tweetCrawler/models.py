from django.db import models

from googleCrawlerOfficial.models import GoogleResultOfficial
from search.models import SearchParameters


class Tweet(models.Model):
    tweet_id = models.TextField()
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
