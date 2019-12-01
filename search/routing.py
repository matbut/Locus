from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, ChannelNameRouter, URLRouter

from django.conf.urls import url

from common import searcherUtils
from search.InternetSearchManager import Manager as InternetManager
from search.websocketConsumer import WSConsumer
from tweetCrawler.twitterSearcher import TwitterUrlSearcher, TwitterTextSearcher
from googleCrawlerOfficial.googleSearcher import Searcher as GoogleSearcher
from database.dbSearcher import FTSearcher, UrlSearcher

websocket_urlpatterns = [
    url('', WSConsumer),
]

application = ProtocolTypeRouter({
    'channel': ChannelNameRouter({
        searcherUtils.INTERNET_SEARCH_MANAGER_NAME: InternetManager,
        searcherUtils.TWITTER_TEXT_SEARCHER_NAME: TwitterTextSearcher,
        searcherUtils.TWITTER_URL_SEARCHER_NAME: TwitterUrlSearcher,
        searcherUtils.DB_URL_SEARCHER_NAME: UrlSearcher,
        searcherUtils.DB_FTSEARCHER_NAME: FTSearcher,
        searcherUtils.GOOGLE_SEARCHER_NAME: GoogleSearcher,
    }),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})