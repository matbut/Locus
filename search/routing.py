from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, ChannelNameRouter, URLRouter

from django.conf.urls import url

from search.websocketConsumer import WSConsumer
from tweetCrawler.crawler import Crawler as tweet_crawler
from googleCrawlerOfficial.crawler import Crawler as google_crawler
from database.searcher import Searcher

websocket_urlpatterns = [
    url("", WSConsumer),
]

application = ProtocolTypeRouter({
    "channel": ChannelNameRouter({
        "tweet_crawler": tweet_crawler,
        "google_crawler": google_crawler,
        "db_searcher": Searcher,
    }),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})