from django.db import models


class GoogleResultOfficial(models.Model):
    id = models.IntegerField(primary_key=True)
    page = models.TextField()
    date = models.DateField()
    link = models.URLField()