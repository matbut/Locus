import logging
from datetime import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView

from database import uploader
from googleCrawlerOfficial.models import GoogleResultOfficial
from tweetCrawler.models import Tweet


def charts(request):
    tweets = Tweet.objects
    my_date = datetime.now()
    return render(request, 'charts.html', {'tweets': tweets, 'date': my_date})


def twitter_tables(request):
    tweets = Tweet.objects
    my_date = datetime.now()
    return render(request, 'twitter_tables.html', {'tweets': tweets, 'date': my_date})


def google_tables_official(request):
    google_results = GoogleResultOfficial.objects
    my_date = datetime.now()
    return render(request, 'google_tables.html', {'google_results': google_results, 'date': my_date})


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
