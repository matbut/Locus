import csv
from datetime import datetime

from database.models import ImportedArticle


def upload(file_data):
    lines = file_data.splitlines()
    articles = []
    for fields in csv.reader(lines[1:], quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
        article = ImportedArticle(page=fields[0], date=datetime.strptime(fields[1], '%Y-%m-%d %H:%M:%S'),
                                  link=fields[2], title=fields[3], content=fields[4])
        articles.append(article)
    for article in articles:
        article.save()



