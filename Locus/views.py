from django.http import HttpResponse
from django.shortcuts import render

from tweetCrawler.models import Tweet


def home(request):
    tweets = Tweet.objects
    return render(request, 'index.html', {'tweets': tweets})
