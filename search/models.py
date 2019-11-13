from django.db import models


class SearchParameters(models.Model):
    url = models.TextField()
    title = models.TextField()
    content = models.TextField()
