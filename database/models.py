from django.db import models


class ImportedArticle(models.Model):
    id = models.IntegerField(primary_key=True)
    page = models.TextField()
    date = models.DateField(null=True)
    link = models.URLField()
    title = models.TextField()
    content = models.TextField()
