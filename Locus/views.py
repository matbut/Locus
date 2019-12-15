import logging
from datetime import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView

from Locus.chart import aggregate, filter_objects
from Locus.widget import users, top_words
from database import uploader
from database.models import ResultArticle
from search.models import SearchParameters, SearcherStatus as Status
from searchEngine.models import InternetResult, Domain
from twitter.models import Tweet, TwitterUser


def charts(request):
    my_date = datetime.now()
    return render(request, 'charts.html', {'date': my_date})


def graph(request):
    tweets = Tweet.objects
    my_date = datetime.now()
    return render(request, 'graph.html', {'my_data': tweets.all(), 'date': my_date})


def twitter_tables(request):
    tweets = Tweet.objects
    return render(request, 'twitter_tables.html', {
        'tweets': tweets,
        'date': datetime.now(),
        'stats': [{
            'name': 'word1',
            'count': 10,
        }, {
            'name': 'word1',
            'count': 10,
        }, {
            'name': 'word1',
            'count': 10,
        }, {
            'name': 'word1',
            'count': 10,
        }, {
            'name': 'word1',
            'count': 10,
        }]
    })


def google_tables_official(request):
    google_results = InternetResult.objects
    return render(request, 'google_tables.html', {
        'google_results': google_results,
        'date': datetime.now(),
        'stats': [{
            'name': 'word1',
            'count': 10,
        }, {
            'name': 'word1',
            'count': 10,
        }, {
            'name': 'word1',
            'count': 10,
        }, {
            'name': 'word1',
            'count': 10,
        }, {
            'name': 'word1',
            'count': 10,
        }]
    })


def database_tables(request):
    database_results = ResultArticle.objects
    return render(request, 'database_tables.html', {
        'database_results': database_results,
        'date': datetime.now(),
        'stats': top_words(),
    })


def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "upload.html", data)
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("upload"))

        params = {
            'link': int(request.POST.get('link')),
            'title': int(request.POST.get('title')),
            'content': int(request.POST.get('content')),
            'date': int(request.POST.get('date')),
            'pattern': request.POST.get('pattern'),
            'delimiter': request.POST.get('delimiter'),
        }

        if csv_file.multiple_chunks():
            with open('/tmp/locus.csv', 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)
                uploader.read_upload('/tmp/locus.csv', params)
        else:
            file_data = csv_file.read().decode("utf-8")
            uploader.upload(file_data, params)
        messages.success(request, 'File uploaded successfully')
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("upload"))


def search(request):
    return render(request, 'search.html')


class Data(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        dateStr = request.query_params['date']
        aggregation = request.query_params['aggregation']

        date = datetime.strptime(dateStr, '%Y-%m-%d').date()

        tweet_table = [{
            "group": 'tweet',
            "tweet": {
                "date": tweet.date,
                "time": tweet.time,
                "username": tweet.username,
                "content": tweet.content,
                "likes": tweet.likes,
                "replies": tweet.replies,
                "retweets": tweet.retweets,
                "link": tweet.link,
                "userlink": tweet.userlink,
            }
        } for tweet in filter_objects(Tweet, aggregation, date)]

        google_table = [{
            "id": google.get_node_id,
            "group": 'google',
            "title": google.page,
            "google": {
                "page": google.page,
                "date": google.date,
                "link": google.link,
            }
        } for google in filter_objects(InternetResult, aggregation, date)]

        article_table = [{
            "group": 'article',
            "article": {
                "page": article.page,
                "date": article.date,
                "link": article.link,
                "similarity": "{0:.4f}".format(round(article.similarity, 4)),
                "title": article.title,
                "content": article.content,
                "words": article.get_top_words,
            }
        } for article in filter_objects(ResultArticle, aggregation, date)]

        return Response(tweet_table + article_table + google_table)


class Chart(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        aggregation = request.query_params['aggregate']

        result = aggregate(aggregation)
        return Response(result)


class CrawlerStatus(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        crawler = request.query_params['crawler']
        status = Status.objects.get(pk=crawler)
        return Response(status.get_status_json)


def node_spec(user):
    if user.avatar:
        return {
            "id": user.get_node_id,
            "group": 'user',
            "title": user.username,
            "shape": 'circularImage',
            "size": 30,
            "image": user.avatar,
            "user": {
                "id": user.id,
                "username": user.username,
                "link": user.link,
            }
        }
    return {
        "id": user.get_node_id,
        "group": 'user',
        "title": user.username,
        "shape": 'icon',
        "size": 40,
        "face": "'Font Awesome 5 Free'",
        "icon": {
            "weight": "bold",
            "code": '\uf007',
            "color": '#00485f',
        },
        "user": {
            "id": user.id,
            "username": user.username,
            "link": user.link,
        }
    }


class Graph(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        load_twitter_users = request.query_params['load_twitter_users'] == 'true'
        load_domain_users = request.query_params['load_domain_users'] == 'true'

        tweet_nodes = [{
            "id": tweet.get_node_id,
            "group": 'tweet',
            "title": tweet.username,
            "tweet": {
                "date": tweet.date,
                "time": tweet.time,
                "username": tweet.username,
                "content": tweet.content,
                "likes": tweet.likes,
                "replies": tweet.replies,
                "retweets": tweet.retweets,
                "link": tweet.link,
                "userlink": tweet.userlink,
            }
        } for tweet in Tweet.objects.all()]

        search_nodes = [{
            "id": search.get_node_id,
            "group": 'search',
            "title": search.link + "<br/>" + search.title,
        } for search in SearchParameters.objects.all()]

        google_nodes = [{
            "id": google.get_node_id,
            "group": 'google',
            "title": google.page,
            "google": {
                "page": google.page,
                "date": google.date,
                "link": google.link,
            }
        } for google in InternetResult.objects.all()]

        article_nodes = [{
            "id": article.get_node_id,
            "group": 'article',
            "title": article.page,
            "article": {
                "page": article.page,
                "date": article.date,
                "link": article.link,
                "similarity": "{0:.4f}".format(round(article.similarity, 4)),
                "title": article.title,
                "content": article.content,
                "words": article.get_top_words,
            }
        } for article in ResultArticle.objects.all()]

        nodes = tweet_nodes + search_nodes + google_nodes + article_nodes

        tweet_edges = [{
            "from": tweet.get_node_id,
            "to": search_node.get_node_id,
        } for search_node in SearchParameters.objects.all() for tweet in search_node.tweets.all()]

        google_tweet_edges = [{
            "from": tweet.get_node_id,
            "to": google.get_node_id,
        } for google in InternetResult.objects.all() for tweet in google.tweets.all()]

        google_edges = [{
            "from": search_node.get_node_id,
            "to": google.get_node_id,
        } for search_node in SearchParameters.objects.all() for google in search_node.internet_articles.all()]

        article_edges = [{
            "from": search_node.get_node_id,
            "to": article.get_node_id,
        } for search_node in SearchParameters.objects.all() for article in search_node.db_articles.all()]

        tweet_article_edges = [{
            "from": article.get_node_id,
            "to": tweet.get_node_id,
        } for article in ResultArticle.objects.all() for tweet in article.tweets.all()]

        edges = tweet_edges + google_tweet_edges + google_edges + article_edges + tweet_article_edges

        if load_twitter_users:
            twitter_user_nodes = [node_spec(user) for user in TwitterUser.objects.all()]
            nodes = nodes + twitter_user_nodes

            twitter_user_edges = [{
                "from": tweet.get_node_id,
                "to": tweet.user.get_node_id,
            } for tweet in Tweet.objects.all()]
            edges = edges + twitter_user_edges

        if load_domain_users:
            domain_user_nodes = [{
                "id": user.get_node_id,
                "group": 'domain',
                "title": user.link,
                "image": "https://www.google.com/s2/favicons?domain={0}".format(user.link),
                "domain": {
                    "link": user.link,
                }
            } for user in Domain.objects.all()]
            nodes = nodes + domain_user_nodes

            google_domain_user_edges = [{
                "from": google.get_node_id,
                "to": google.domain.get_node_id,
            } for google in InternetResult.objects.all()]
            edges = edges + google_domain_user_edges

            db_domain_user_edges = [{
                "from": article.get_node_id,
                "to": article.domain.get_node_id,
            } for article in ResultArticle.objects.all()]
            edges = edges + db_domain_user_edges

        print(load_domain_users)

        return Response({"nodes": nodes, "edges": edges})


class GetTweet(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        tweet_id = int(request.query_params['tweet_id'])
        tweet = Tweet.objects.get(id=1191383982392389632)

        return Response({"tweet": tweet.__dict__})


class UserStats(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        resultType = request.query_params['resultType']
        return Response(users(resultType))
