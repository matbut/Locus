from django.db import models

from search.models import SearchParameters


class GoogleResultOfficial(models.Model):
    id = models.IntegerField(primary_key=True)
    page = models.TextField()
    date = models.DateField(null=True)
    link = models.URLField()

    searches = models.ManyToManyField(SearchParameters)

    @property
    def get_date(self):
        if self.date:
            return self.date
        else:
            return "-"
