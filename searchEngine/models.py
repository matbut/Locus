from django.db import models

from common.textUtils import remove_punctuation, remove_stopwords, remove_diacritics, get_top_words_count
from search.models import SearchParameters


class Domain(models.Model):
    link = models.URLField(primary_key=True)

    @property
    def get_node_id(self):
        return 'domainUser' + str(self.link)


class InternetResult(models.Model):
    page = models.TextField()
    date = models.DateField(null=True)
    link = models.URLField(primary_key=True)
    title = models.TextField(default="")
    snippet = models.TextField(default="")

    searches = models.ManyToManyField(SearchParameters, related_name='internet_articles')
    domain = models.ForeignKey(Domain, null=True, on_delete=models.SET_NULL)

    @property
    def get_date(self):
        if self.date:
            return self.date
        else:
            return '-'

    @property
    def get_node_id(self):
        return 'google' + str(self.link)


def get_global_title_top_five():
    title_concat = ' '.join([r.title for r in InternetResult.objects.all()]).lower()
    title_concat = remove_diacritics(remove_stopwords(remove_punctuation(title_concat)))
    words, counts = get_top_words_count([title_concat], top=5)
    return [{'name': w, 'count': c} for w, c in zip(words, counts)]
