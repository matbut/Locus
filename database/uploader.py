import csv
import os
from datetime import datetime
from urllib.parse import urlparse

from database.models import ImportedArticle


def upload(file_data):
    lines = file_data.splitlines()
    articles = []
    csv_reader = get_csv_reader(lines[1:])
    for fields in csv_reader:
        article = get_article_from_field(fields)
        articles.append(article)
    save_articles(articles)


def read_upload(file_name):
    articles = []
    with open(file_name) as csv_file:
        csv_reader = get_csv_reader(csv_file)
        line_count = 0
        for fields in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                article = get_article_from_field(fields)
                articles.append(article)
                line_count += 1
    os.remove(file_name)
    save_articles(articles)


def save_articles(articles):
    for article in articles:
        article.save()


def get_csv_reader(content):
    return csv.reader(content, quotechar='"', delimiter=';', quoting=csv.QUOTE_ALL, skipinitialspace=True)


def get_article_from_field(fields):
    page = urlparse(fields[0]).netloc
    return ImportedArticle(page=page, date=datetime.strptime(fields[4], '%Y-%m-%d %H:%M:%S'),
                           link=fields[0], title=fields[3], content=fields[2])
