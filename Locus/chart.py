from datetime import date, datetime

from common.dateUtils import days_date_range, weeks_date_range, months_date_range, years_date_range
from database.models import ResultArticle
from googleCrawlerOfficial.models import GoogleResultOfficial
from tweetCrawler.models import Tweet


def aggregate(aggregation):
    if aggregation == 'day':
        return count_daily()

    if aggregation == 'week':
        return count_weekly()

    if aggregation == 'month':
        return count_monthly()

    if aggregation == 'year':
        return count_yearly()


def count_min_max_date():
    now = datetime.date(datetime.now())

    tweets_min = min([tweet.date for tweet in Tweet.objects.all()], default=now)
    google_min = min([google.date for google in GoogleResultOfficial.objects.all() if google.date is not None], default=now)
    article_min = min([article.date for article in ResultArticle.objects.all() if article.date is not None], default=now)

    min_date = min([tweets_min, google_min, article_min])

    early = datetime.date(datetime.min)

    tweets_max = max([tweet.date for tweet in Tweet.objects.all()], default=early)
    google_max = max([google.date for google in GoogleResultOfficial.objects.all() if google.date is not None], default=early)
    article_max = max([article.date for article in ResultArticle.objects.all() if article.date is not None], default=early)

    max_date = max([tweets_max, google_max, article_max])

    return min_date, max_date


def count_daily():
    min_date, max_date = count_min_max_date()

    tweet_results = []
    google_results = []
    article_results = []

    for date in days_date_range(min_date, max_date):
        count = len([1 for tweet in Tweet.objects.all() if tweet.date == date])
        tweet_results.append([date, count])

        count = len([1 for google in GoogleResultOfficial.objects.all() if
                     google.date is not None and google.date == date])
        google_results.append([date, count])

        count = len([1 for article in ResultArticle.objects.all() if
                     article.date is not None and article.date == date])
        article_results.append([date, count])

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


def count_weekly():
    min_date, max_date = count_min_max_date()

    tweet_results = []
    google_results = []
    article_results = []

    for (from_date,to_date) in weeks_date_range(min_date, max_date):
        count = len([1 for tweet in Tweet.objects.all() if from_date <= tweet.date <= to_date])
        tweet_results.append([to_date, count])

        count = len([1 for google in GoogleResultOfficial.objects.all() if
                     google.date is not None and from_date <= google.date <= to_date])
        google_results.append([to_date, count])

        count = len([1 for article in ResultArticle.objects.all() if
                     article.date is not None and from_date <= article.date <= to_date])
        article_results.append([to_date, count])

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


def count_monthly():
    min_date, max_date = count_min_max_date()

    tweet_results = []
    google_results = []
    article_results = []

    for (month, year) in months_date_range(min_date, max_date):
        count = len([1 for tweet in Tweet.objects.all() if tweet.date.month == month and tweet.date.year == year])
        tweet_results.append((date(year, month, 1),count))

        count = len([1 for google in GoogleResultOfficial.objects.all() if
                     google.date is not None and google.date.month == month and google.date.year == year])
        google_results.append((date(year, month, 1),count))

        count = len([1 for article in ResultArticle.objects.all() if
                     article.date is not None and article.date.month == month and article.date.year == year])
        article_results.append((date(year, month, 1),count))

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


def count_yearly():
    min_date, max_date = count_min_max_date()

    tweet_results = []
    google_results = []
    article_results = []

    for year in years_date_range(min_date, max_date):
        count = len([1 for tweet in Tweet.objects.all() if tweet.date.year == year])
        tweet_results.append((date(year, 1, 1),count))

        count = len([1 for google in GoogleResultOfficial.objects.all() if
                     google.date is not None and google.date.year == year])
        google_results.append((date(year, 1, 1),count))

        count = len([1 for article in ResultArticle.objects.all() if
                     article.date is not None and article.date.year == year])
        article_results.append((date(year, 1, 1),count))

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


# tweet_query_set = (Tweet.objects
#                    .annotate(day=TruncDay('date'))  # Truncate to month and add to select list
#                    .values('day')  # Group By month
#                    .annotate(c=Count('id'))  # Select the count of the grouping
#                    .order_by('day').all())
#
# tweet_result_list = list(map(lambda x: [x['day'], x['c']], list(tweet_query_set)))