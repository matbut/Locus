from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, ChannelNameRouter, URLRouter

from django.conf.urls import url

from search.websocketConsumer import WSConsumer
from tweetCrawler.crawler import Crawler as tweet_crawler
from googleCrawler.crawler import Crawler as google_crawler
from googleCrawlerOfficial.crawler import Crawler as google_crawler_official

websocket_urlpatterns = [
    url("search", WSConsumer),
]

application = ProtocolTypeRouter({
    "channel": ChannelNameRouter({
        "tweet_crawler": tweet_crawler,
        "google_crawler": google_crawler,
        "google_crawler_official": google_crawler_official,
    }),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})