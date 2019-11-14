from django.db import models

from search.models import SearchParameters


class ImportedArticle(models.Model):
    id = models.IntegerField(primary_key=True)
    page = models.TextField()
    date = models.DateField(null=True)
    link = models.URLField(unique=True)
    title = models.TextField()
    content = models.TextField()


class ResultArticle(models.Model):
    id = models.IntegerField(primary_key=True)
    similarity = models.FloatField()
    page = models.TextField()
    date = models.DateField(null=True)
    link = models.URLField()
    title = models.TextField()
    content = models.TextField()

    searches = models.ManyToManyField(SearchParameters)
