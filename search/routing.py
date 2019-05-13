from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, ChannelNameRouter, URLRouter

from django.conf.urls import url

from search.websocketConsumer import WSConsumer
from tweetCrawler.crawler import Crawler

websocket_urlpatterns = [
    url("search", WSConsumer),
]

application = ProtocolTypeRouter({
    "channel": ChannelNameRouter({
        "tweet_crawler": Crawler,
    }),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})