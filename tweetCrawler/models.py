from django.db import models


class Tweet(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    username = models.CharField(max_length=30)
    link = models.CharField(max_length=60)


class CrawlParameters:
    def __init__(self, dictionary=None):
        if dictionary:
            self.url = dictionary['url']
            self.title = dictionary['title']
            self.content = dictionary['content']
            self.twitter = dictionary['twitter']
        else:
            self.url = None
            self.title = None
            self.content = None
            self.twitter = None
