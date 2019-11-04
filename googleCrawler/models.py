from django.db import models


class GoogleResult(models.Model):
    id = models.IntegerField(primary_key=True)
    page = models.TextField()
    link = models.URLField()
