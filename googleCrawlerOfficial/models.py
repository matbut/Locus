from django.db import models

from search.models import SearchParameters


class GoogleResultOfficial(models.Model):
    page = models.TextField()
    date = models.DateField(null=True)
    link = models.URLField(primary_key=True)

    searches = models.ManyToManyField(SearchParameters)

    @property
    def get_date(self):
        if self.date:
            return self.date
        else:
            return "-"

    @property
    def get_node_id(self):
        return 'google' + str(self.link)
