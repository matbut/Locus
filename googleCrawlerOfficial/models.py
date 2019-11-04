from django.db import models


class GoogleResultOfficial(models.Model):
    id = models.IntegerField(primary_key=True)
    page = models.TextField()
    date = models.DateField(null=True)
    link = models.URLField()

    @property
    def get_date(self):
        if self.date:
            return self.date
        else:
            return "-"
