from asgiref.sync import async_to_sync

from database.models import ResultArticle
from googleCrawlerOfficial.models import InternetResult
from search.models import SearchParameters
from tweetCrawler.models import Tweet

MAIN_SEARCH_NAME = 'main_search'

DB_FTSEARCHER_NAME = 'db_ftsearcher'
DB_URL_SEARCHER_NAME = 'db_url_searcher'
TWITTER_URL_SEARCHER_NAME = 'twitter_url_searcher'
TWITTER_TEXT_SEARCHER_NAME = 'twitter_text_searcher'
GOOGLE_SEARCHER_NAME = 'google_searcher'
LINK_MANAGER_NAME = 'link_manager'

WORKER_NAMES = [DB_FTSEARCHER_NAME, DB_URL_SEARCHER_NAME, TWITTER_URL_SEARCHER_NAME, TWITTER_TEXT_SEARCHER_NAME,
                GOOGLE_SEARCHER_NAME, LINK_MANAGER_NAME]


def add_parent(result, parent):
    if parent.type == MAIN_SEARCH_NAME:
        result.searches.add(SearchParameters.objects.get(pk=parent.id))
    elif parent.type == DB_FTSEARCHER_NAME:
        result.db_articles.add(ResultArticle.objects.get(pk=parent.id))
    elif parent.type == DB_URL_SEARCHER_NAME:
        result.db_articles.add(ResultArticle.objects.get(pk=parent.id))
    elif parent.type == TWITTER_URL_SEARCHER_NAME:
        result.tweets.add(Tweet.objects.get(pk=parent.id))
    elif parent.type == TWITTER_TEXT_SEARCHER_NAME:
        result.tweets.add(Tweet.objects.get(pk=parent.id))
    elif parent.type == LINK_MANAGER_NAME:
        result.internet_articles.add(InternetResult.objects.get(pk=parent.id))


def get_main_search(search_id):
    search_parameters = SearchParameters.objects.get(id=search_id) if search_id is not None else None
    return search_parameters


def send_to_worker(channel_layer, sender, where, body, method='search'):
    async_to_sync(channel_layer.send)(where, {
        'type': method,
        'sender': sender,
        'body': body
    })


def send_to_websocket(channel_layer, where, method, message):
    async_to_sync(channel_layer.group_send)(
        where,
        {
            'type': method,
            'message': message
        }
    )


def is_worker(sender):
    return sender in WORKER_NAMES


def search_cancelled(search_id):
    return not SearchParameters.objects.filter(pk=search_id).exists()
