from django.db import models

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

    searches = models.ManyToManyField(SearchParameters)
    #tweets = models.ManyToManyField(Tweet)
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
