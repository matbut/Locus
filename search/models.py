from django.db import models

# Create your models here.

class CrawlParameters:
    def __init__(self, dictionary=None):
        if dictionary:
            self.url = dictionary['url']
            self.title = dictionary['title']
            self.content = dictionary['content']
        else:
            self.url = None
            self.title = None
            self.content = None

