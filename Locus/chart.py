from datetime import datetime

from django.db.models import Min, Max

from common.dateUtils import count_end_date, date_range
from database.models import ResultArticle
from googleCrawlerOfficial.models import GoogleResultOfficial
from tweetCrawler.models import Tweet


def filter_objects(db, aggregation, start_date):
    end_date = count_end_date(aggregation, start_date)
    return db.objects.filter(date__gte=start_date, date__lt=end_date).all()


def count_objects(db, aggregation, start_date):
    end_date = count_end_date(aggregation, start_date)
    return db.objects.filter(date__gte=start_date, date__lt=end_date).count()


def min_objects(db):
    return (db.objects.values('date').annotate(min=Min('date')) or [{'min': datetime.date(datetime.now())}])[0]['min']


def max_objects(db):
    return (db.objects.values('date').annotate(max=Max('date')) or [{'max': datetime.date(datetime.min)}])[0]['max']


def count_min_max_date():
    now = datetime.date(datetime.now())
    dbs = [Tweet, GoogleResultOfficial, ResultArticle]
    min_date = min([min_objects(db) for db in dbs], default=now)
    max_date = max([max_objects(db) for db in dbs], default=now)
    return min_date, max_date


def aggregate(aggregation):
    min_date, max_date = count_min_max_date()

    tweet_results = []
    google_results = []
    article_results = []

    for dateTime in date_range(aggregation, min_date, max_date):
        count = count_objects(Tweet, aggregation, dateTime)
        tweet_results.append([dateTime.date(), count])

        count = count_objects(GoogleResultOfficial, aggregation, dateTime)
        google_results.append([dateTime.date(), count])

        count = count_objects(ResultArticle, aggregation, dateTime)
        article_results.append([dateTime.date(), count])

    return [{
        "name": 'Tweets',
        "data": tweet_results
    }, {
        "name": 'Google',
        "data": google_results
    }, {
        "name": 'Database',
        "data": article_results
    }]
