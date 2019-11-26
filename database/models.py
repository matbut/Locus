from django.db import models

from googleCrawlerOfficial.models import Domain
from search.models import SearchParameters


class ImportedArticle(models.Model):
    page = models.TextField()
    date = models.DateField(null=True)
    link = models.URLField(primary_key=True)
    title = models.TextField()
    content = models.TextField()


class TopWord(models.Model):
    word = models.TextField(default='')
    count = models.IntegerField(default=0)


class ResultArticle(models.Model):
    similarity = models.FloatField()
    page = models.TextField()
    date = models.DateField(null=True)
    link = models.URLField(primary_key=True)
    title = models.TextField()
    content = models.TextField()

    top_words = models.ManyToManyField(TopWord)
    searches = models.ManyToManyField(SearchParameters)
    domain = models.ForeignKey(Domain, null=True, on_delete=models.SET_NULL)

    @property
    def get_node_id(self):
        return 'db' + str(self.link)

    @property
    def get_top_words(self):
        return ', '.join(['{0} ({1})'.format(tw.word, tw.count) for tw in self.top_words.all()])
