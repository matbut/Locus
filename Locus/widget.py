from django.db.models import F, Count

from database.models import ResultArticle
from searchEngine.models import InternetResult
from twitter.models import Tweet

top = 7
others_name = "others"


def users(resultType):
    print(resultType)

    result = {
        'tweet': tweet_users,
        'google': google_users,
        'article': article_users,
    }[resultType]()

    all_labels = list(map(lambda x: x['username'], result))
    all_series = list(map(lambda x: x['count'], result))

    labels = all_labels[:top]
    labels.append(others_name)
    series = all_series[:top]
    others = sum(all_series[top:])
    series.append(others)

    return {
        'labels': labels,
        'series': series,
        'users': len(all_labels)
    }


def tweet_users():
    return Tweet.objects \
        .values('username') \
        .annotate(count=Count('id')) \
        .order_by('-count')


def google_users():
    return InternetResult.objects \
        .values('domain') \
        .annotate(username=F('domain')) \
        .annotate(count=Count('link')) \
        .order_by('-count')


def article_users():
    return ResultArticle.objects \
        .values('domain') \
        .annotate(username=F('domain')) \
        .annotate(count=Count('link')) \
        .order_by('-count')
