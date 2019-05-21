from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

from tweetCrawler.models import Tweet

def charts(request):
    tweets = Tweet.objects
    my_date = datetime.now()
    return render(request, 'charts.html', {'tweets': tweets, 'date': my_date})


def tables(request):
    tweets = Tweet.objects
    my_date = datetime.now()
    return render(request, 'tables.html', {'tweets': tweets, 'date': my_date})


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
        presentedYears = [years.count(year) for year in range(minYear, maxYear+1)]
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
        days = [tweet.date.day for tweet in Tweet.objects.all() if tweet.date.month == month]
        presentedDays = [days.count(day) for day in range(1, 31)]
        return Response(presentedDays)
