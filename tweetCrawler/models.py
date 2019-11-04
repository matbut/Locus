from django.db import models


class Tweet(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    username = models.CharField(max_length=60)
    userlink = models.URLField()
    link = models.URLField()
    likes = models.IntegerField()
    replies = models.IntegerField()
    retweets = models.IntegerField()
