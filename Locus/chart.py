from datetime import datetime

from django.db.models import Min, Max, Count
from django.db.models.functions import TruncMonth, TruncDay, TruncYear, TruncWeek

from common.dateUtils import count_end_date
from database.models import ResultArticle
from searchEngine.models import InternetResult
from twitter.models import Tweet


def min_objects(db):
    return db.objects.values('date').filter(date__isnull=False).aggregate(min=Min('date'))['min'] or datetime.date(datetime.now())


def max_objects(db):
    return db.objects.values('date').filter(date__isnull=False).aggregate(max=Max('date'))['max'] or datetime.date(datetime.min)


def count_min_max_date():
    dbs = [Tweet, InternetResult, ResultArticle]

    print(min_objects(ResultArticle))

    min_date = min([min_objects(db) for db in dbs])
    max_date = max([max_objects(db) for db in dbs])
    return min_date, max_date


def filter_objects(db, aggregation, start_date):
    end_date = count_end_date(aggregation, start_date)
    return db.objects.filter(date__isnull=False, date__gte=start_date, date__lt=end_date).all()


def count_objects(db, aggregation, start_date):
    end_date = count_end_date(aggregation, start_date)
    return db.objects.filter(date__isnull=False, date__gte=start_date, date__lt=end_date).count()


def count_by_aggregation(db, aggregation):
    return list(map(lambda x: [x['aggregated_date'], x['count']],
                    db.objects
                    .filter(date__isnull=False)
                    .annotate(aggregated_date=trunc_by_aggregation(aggregation))
                    .values('aggregated_date')
                    .annotate(count=Count('link'))
                    .values('aggregated_date', 'count')
                    .order_by('aggregated_date')))


def trunc_by_aggregation(aggregation):
    return {
        'day': TruncDay,
        'week': TruncWeek,
        'month': TruncMonth,
        'year': TruncYear,
    }[aggregation]('date')


def aggregate(aggregation):
    return [{
        "name": 'Tweets',
        "data": count_by_aggregation(Tweet, aggregation)
    }, {
        "name": 'Google',
        "data": count_by_aggregation(InternetResult, aggregation)
    }, {
        "name": 'Database',
        "data": count_by_aggregation(ResultArticle, aggregation)
    }]
