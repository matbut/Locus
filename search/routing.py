from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, ChannelNameRouter, URLRouter
from crawler.crawler import Crawler
from crawler.crawler import SomeComponent
from crawler.crawler import AnotherComponent
from crawler.crawler import WSConsumer
from django.conf.urls import url

websocket_urlpatterns = [
    url("search", WSConsumer),
]

application = ProtocolTypeRouter({
    "channel": ChannelNameRouter({
        "crawler": Crawler,
        "some_component": SomeComponent,
        "another_component": AnotherComponent,
    }),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
