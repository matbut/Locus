"""Locus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.search, name='search'),
    path('charts/', views.charts, name='charts'),
    path('twitter_tables/', views.twitter_tables, name='twitter_tables'),
    path('google_tables/', views.google_tables, name='google_tables'),

    path('api/tweets/yearly', views.ChartTweetsYearly.as_view()),
    path('api/tweets/monthly', views.ChartTweetsMonthly.as_view()),
    path('api/tweets/daily', views.ChartTweetsDaily.as_view()),
]