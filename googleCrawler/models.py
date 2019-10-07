from django.db import models


class GoogleResult(models.Model):
    id = models.IntegerField(primary_key=True)
    page = models.TextField()
    #date = models.DateField()
    #time = models.TimeField()
    link = models.URLField()
