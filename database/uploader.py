import csv
import os

from common.dates import parse_date
from common.url import get_domain, clean_url
from database.models import ImportedArticle


def upload(file_data, params):
    lines = file_data.splitlines()
    articles = []
    csv_reader = get_csv_reader(lines[1:], params['delimiter'])
    for fields in csv_reader:
        article = get_article_from_field(fields, params)
        articles.append(article)
    save_articles(articles)


def read_upload(file_name, params):
    articles = []
    with open(file_name) as csv_file:
        csv_reader = get_csv_reader(csv_file, params['delimiter'])
        line_count = 0
        for fields in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                article = get_article_from_field(fields, params)
                articles.append(article)
                line_count += 1
    os.remove(file_name)
    save_articles(articles)


def save_articles(articles):
    for article in articles:
        article.save()


def get_csv_reader(content, delimiter):
    return csv.reader(content, quotechar='"', delimiter=delimiter, quoting=csv.QUOTE_ALL, skipinitialspace=True)


def get_article_from_field(fields, params):
    page = get_domain(fields[params['link']])
    return ImportedArticle(page=page, date=parse_date(fields[params['date']], params['pattern']),
                           link=clean_url(fields[params['link']]), title=fields[params['title']], content=fields[params['content']])
