from django.db import models

from search.models import SearchParameters


class ImportedArticle(models.Model):
    page = models.TextField()
    date = models.DateField(null=True)
    link = models.URLField(primary_key=True)
    title = models.TextField()
    content = models.TextField()


class ResultArticle(models.Model):
    similarity = models.FloatField()
    page = models.TextField()
    date = models.DateField(null=True)
    link = models.URLField(primary_key=True)
    title = models.TextField()
    content = models.TextField()

    searches = models.ManyToManyField(SearchParameters)
