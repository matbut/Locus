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


class ChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        dates = [tweet.date.month for tweet in Tweet.objects.all()]
        months = [dates.count(month) for month in range(1, 12)]
        return Response(months)
