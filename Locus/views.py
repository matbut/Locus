import logging
from datetime import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView

from database import uploader
from database.models import ResultArticle
from googleCrawlerOfficial.models import GoogleResultOfficial
from search.models import SearchParameters, CrawlerStatus as Status
from tweetCrawler.models import Tweet


def charts(request):
    my_date = datetime.now()
    return render(request, 'charts.html', {'date': my_date})


def graph(request):
    tweets = Tweet.objects
    my_date = datetime.now()
    return render(request, 'graph.html', {'my_data': tweets.all(), 'date': my_date})


def twitter_tables(request):
    tweets = Tweet.objects
    my_date = datetime.now()
    return render(request, 'twitter_tables.html', {'tweets': tweets, 'date': my_date})


def google_tables_official(request):
    google_results = GoogleResultOfficial.objects
    my_date = datetime.now()
    return render(request, 'google_tables.html', {'google_results': google_results, 'date': my_date})


def database_tables(request):
    database_results = ResultArticle.objects
    return render(request, 'database_tables.html', {'database_results': database_results})


def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "upload.html", data)
    try:

        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("upload"))

        if csv_file.multiple_chunks():
            with open('/tmp/locus.csv', 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)
                uploader.read_upload('/tmp/locus.csv')
        else:
            file_data = csv_file.read().decode("utf-8")
            uploader.upload(file_data)
        messages.success(request, 'File uploaded successfully')
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("upload"))


def search(request):
    return render(request, 'search.html')


class ChartTweetsYearly(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        years = [tweet.date.year for tweet in Tweet.objects.all()]
        nowYear = datetime.now().year
        minYear = min(years, default=nowYear)
        maxYear = max(years, default=nowYear)
        presentedYears = [years.count(year) for year in range(minYear, maxYear + 1)]
        return Response({
            'minYear': minYear,
            'maxYear': maxYear,
            'activity': presentedYears,
        })


class ChartTweetsMonthly(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        year = int(request.query_params['year'])
        months = [tweet.date.month for tweet in Tweet.objects.all() if tweet.date.year == year]
        presentedMonths = [months.count(month) for month in range(1, 12)]
        return Response(presentedMonths)


class ChartTweetsDaily(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        month = int(request.query_params['month'])
        year = int(request.query_params['year'])
        days = [tweet.date.day for tweet in Tweet.objects.all() if
                tweet.date.month == month and tweet.date.year == year]
        presentedDays = [days.count(day) for day in range(1, 31)]
        return Response(presentedDays)


class CrawlerStatus(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        crawler = request.query_params['crawler']
        status = Status.objects.get(pk=crawler)
        return Response(status.get_status_json)


class Graph(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
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
            "title": search.url+"<br/>"+search.title,
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
        } for google in GoogleResultOfficial.objects.all()]

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
        } for search_node in SearchParameters.objects.all() for tweet in search_node.tweet_set.all()]

        google_tweet_edges = [{
            "from": tweet.get_node_id,
            "to": google.get_node_id,
        } for google in GoogleResultOfficial.objects.all() for tweet in google.tweet_set.all()]

        google_edges = [{
            "from": search_node.get_node_id,
            "to": google.get_node_id,
        } for search_node in SearchParameters.objects.all() for google in search_node.googleresultofficial_set.all()]

        article_edges = [{
            "from": search_node.get_node_id,
            "to": article.get_node_id,
        } for search_node in SearchParameters.objects.all() for article in search_node.resultarticle_set.all()]

        edges = tweet_edges + google_tweet_edges + google_edges + article_edges

        return Response({"nodes": nodes, "edges": edges})


class GetTweet(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        tweet_id = int(request.query_params['tweet_id'])
        tweet = Tweet.objects.get(id=1191383982392389632)

        return Response({"tweet": tweet.__dict__})
