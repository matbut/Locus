from django.http import HttpResponse
from django.shortcuts import render
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
