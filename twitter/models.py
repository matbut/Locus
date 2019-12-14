from django.db import models

from searchEngine.models import InternetResult
from search.models import SearchParameters


class TwitterUser(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    username = models.CharField(max_length=60)
    link = models.URLField()
    avatar = models.TextField(default="")

    @property
    def get_node_id(self):
        return 'twitterUser' + str(self.id)


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

    user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE, null=True)
    searches = models.ManyToManyField(SearchParameters, related_name='tweets')
    internet_articles = models.ManyToManyField(InternetResult, related_name='tweets')

    @property
    def get_node_id(self):
        return 'tweet' + str(self.id)
