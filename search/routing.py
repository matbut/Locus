from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, ChannelNameRouter, URLRouter

from django.conf.urls import url

from common import searcherUtils
from search.LinkManager import Manager as LinkManager
from search.SearchBroker import Broker
from twitter.twitterSearcher import TwitterUrlSearcher, TwitterTextSearcher
from searchEngine.googleSearcher import Searcher as GoogleSearcher
from database.dbSearcher import FTSearcher, UrlSearcher

websocket_urlpatterns = [
    url('', Broker),
]

application = ProtocolTypeRouter({
    'channel': ChannelNameRouter({
        searcherUtils.LINK_MANAGER_NAME: LinkManager,
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