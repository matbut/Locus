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
from search.models import SearchParameters
from tweetCrawler.models import Tweet

import random


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

        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("upload"))

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


class Graph(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        tweet_nodes = [{
            "color": "#0275D8",
            "id": tweet.id,
            "label": tweet.content,
            "size": tweet.likes,
            "x": random.randint(0, 100),
            "y": random.randint(0, 100)
        } for tweet in Tweet.objects.all()]

        search_nodes = [{
            "color": "#fd7e14",
            "id": search.id,
            "label": search.url,
            "size": 10,
            "x": random.randint(0, 100),
            "y": random.randint(0, 100)
        } for search in SearchParameters.objects.all()]

        nodes = tweet_nodes + search_nodes

        edges = [{
            "id": tweet.id+search_node.id,
            "source": tweet.id,
            "target": search_node.id,
            "color" : '#66b2ff',
        } for search_node in SearchParameters.objects.all() for tweet in search_node.tweet_set.all()]

        return Response({"nodes": nodes, "edges": edges})


class GetTweet(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        tweet_id = int(request.query_params['tweet_id'])
        tweet = Tweet.objects.get(id=1191383982392389632)

        return Response({"tweet": tweet.__dict__})
