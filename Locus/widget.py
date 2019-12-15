from django.db.models import F, Count, Sum

from database.models import ResultArticle, TopWord
from searchEngine.models import InternetResult
from twitter.models import Tweet, Hashtag

top_users_num = 7
top_words_num = 5
others_name = "others"


def users(resultType):
    result = {
        'tweet': tweet_users,
        'google': google_users,
        'article': article_users,
    }[resultType]()

    all_labels = list(map(lambda x: x['username'], result))
    all_series = list(map(lambda x: x['count'], result))

    labels = all_labels[:top_users_num]
    labels.append(others_name)
    series = all_series[:top_users_num]
    others = sum(all_series[top_users_num:])
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


def top_words():
    return TopWord.objects \
        .values('word') \
        .annotate(name=F('word')) \
        .annotate(count=Sum('count')) \
        .order_by('-count')[:top_words_num]


def count(result_type):
    return {
        'tweet': Tweet,
        'google': InternetResult,
        'article': ResultArticle,
    }[result_type].objects.count()


def hashtags():
    return Hashtag.objects \
        .values('id') \
        .annotate(name=F('id')) \
        .annotate(count=Count('tweet')) \
        .order_by('-count')[:top_words_num]
