from django.db import models


class Tweet(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    username = models.CharField(max_length=30)
    link = models.CharField(max_length=60)


class CrawlParameters:
    Url = None
    Title = None
    Content = None
