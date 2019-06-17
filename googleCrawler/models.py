from django.db import models


class GoogleResult(models.Model):
    id = models.IntegerField(primary_key=True)
    #date = models.DateField()
    #time = models.TimeField()
    link = models.URLField()
