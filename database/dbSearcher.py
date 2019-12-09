import asyncio
import logging
import string
import traceback

import numpy as np
from channels.consumer import SyncConsumer
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.db import transaction
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from common.searcherUtils import get_main_search, send_to_websocket, DB_FTSEARCHER_NAME, DB_URL_SEARCHER_NAME, \
    WORKER_NAMES, add_parent, send_to_worker, TWITTER_URL_SEARCHER_NAME, search_cancelled
from common import statusUpdate
from common.textUtils import remove_diacritics, remove_stopwords
from database.models import ImportedArticle, ResultArticle, TopWord
from googleCrawlerOfficial.models import Domain
from search.models import Parent

postgresql_rank_threshold = 0.3
cosine_similarity_threshold = 0.13


def get_or_create(result_article, domain, similarity):
    if ResultArticle.objects.filter(link=result_article.link).exists():
        return ResultArticle.objects.get(link=result_article.link)
    else:
        result = ResultArticle(similarity=similarity, page=result_article.page, date=result_article.date,
                             link=result_article.link, title=result_article.title,
                             content=result_article.content, domain=domain)
        result.save()
        return result


@transaction.atomic
def save_or_skip(result_article, main_search, parent):
    result_content = result_article.content

    similarity, top_words, counts = count_similarity(main_search.content, result_content, top=5)
    if similarity > cosine_similarity_threshold:
        words = [TopWord(word=word, count=count) for word, count in zip(top_words, counts)]
        domain, _ = Domain.objects.get_or_create(link=result_article.page)
        article = get_or_create(result_article, domain, similarity)
        for word in words:
            word.save()
            article.top_words.add(word)
        add_parent(article, parent)
        return article
    return None


def prepare_title(title):
    return ' '.join(remove_stopwords(
        title
            .translate(str.maketrans('', '', string.punctuation))
            .split()))


def count_similarity(text1, text2, top=5):
    # preprocessing
    texts = [[w.lower() for w in text.translate(str.maketrans('', '', string.punctuation)).split()] for text in
             [text1, text2]]
    texts = [remove_stopwords(text) for text in texts]
    texts = [remove_diacritics(' '.join(text)) for text in texts]

    # find most frequent words
    count_vectorizer = CountVectorizer()
    count_matrix = count_vectorizer.fit_transform(texts)
    features = count_vectorizer.get_feature_names()
    indices = np.argsort(count_matrix[1].toarray().astype('int')).flatten()[::-1]

    # count similarity
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(texts)
    sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return sim[0][0], np.array(features)[indices][:top], count_matrix.toarray()[1][indices][:top]


def find_articles(title_without_stop):
    vector = SearchVector('title', 'content', config='public.polish')
    query = SearchQuery(title_without_stop, config='public.polish')
    return ImportedArticle.objects \
        .annotate(rank=SearchRank(vector, query)) \
        .filter(rank__gte=postgresql_rank_threshold) \
        .order_by('-rank')


class FTSearcher(SyncConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.name = DB_FTSEARCHER_NAME

    def log(self, level, message):
        logging.log(level, '[{0}] {1}'.format(self.name, message))

    def save_or_skip(self, result_article, main_search, parent, where):
        if result_article.link == main_search.link:
            return
        try:
            result = save_or_skip(result_article, main_search, parent)
            if result and where not in WORKER_NAMES:
                send_to_websocket(self.channel_layer, where=where, method='success', message='')
            if result and result.link != main_search.link and main_search.twitter_search:
                statusUpdate.get(TWITTER_URL_SEARCHER_NAME).queued(main_search.id)
                send_to_worker(self.channel_layer, sender=self.name, where=TWITTER_URL_SEARCHER_NAME,
                               method='search', body={
                        'link': result.link,
                        'search_id': main_search.id,
                        'parent': Parent(id=result.link, type=self.name).to_dict()
                    })
        except Exception as e:
            self.log(logging.WARNING, 'Object was not added to database: {}'.format(str(e)))

    def search_parameters_correct(self, msg):
        if not msg['body']['title']:
            self.log(logging.INFO, 'Title cannot be empty')
            return False
        return True

    def search(self, msg):
        self.log(logging.INFO, 'Starting')
        asyncio.set_event_loop(asyncio.new_event_loop())

        main_search_id = msg['body']['search_id']
        updater = statusUpdate.get(self.name)
        updater.in_progress(main_search_id)

        if search_cancelled(main_search_id):
            self.log(logging.INFO, 'Search cancelled, finishing')
            updater.success(main_search_id)
            return

        if not self.search_parameters_correct(msg):
            self.log(logging.INFO, 'Parameters incorrect, finishing')
            updater.success(main_search_id)
            return

        try:
            main_search = get_main_search(main_search_id)
            title = msg['body']['title']
            parent = Parent.from_dict(msg['body']['parent'])
            sender = msg['sender']

            title_without_stop = prepare_title(title)
            result = find_articles(title_without_stop)

            for result_article in result:
                self.save_or_skip(result_article, main_search, parent, sender)

            updater.success(main_search_id)

            self.log(logging.INFO, 'Finished')

        except Exception as e:
            print(traceback.format_exc())
            updater.failure(main_search_id)
            self.log(logging.WARNING, 'Failed: {0}'.format(str(e)))


class UrlSearcher(SyncConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.name = DB_URL_SEARCHER_NAME

    def log(self, level, message):
        logging.log(level, '[{0}] {1}'.format(self.name, message))

    def save_or_skip(self, result_article, main_search, parent, where):
        try:
            result = save_or_skip(result_article, main_search, parent)
            if result and where not in WORKER_NAMES:
                send_to_websocket(self.channel_layer, where=where, method='success', message='')
            if result and result.link != main_search.link and main_search.twitter_search:
                statusUpdate.get(TWITTER_URL_SEARCHER_NAME).queued(main_search.id)
                send_to_worker(self.channel_layer, sender=self.name, where=TWITTER_URL_SEARCHER_NAME,
                               method='search', body={
                        'link': result.link,
                        'search_id': main_search.id,
                        'parent': Parent(id=result.link, type=self.name).to_dict()
                    })
        except Exception as e:
            self.log(logging.WARNING, 'Object was not added to database: {}'.format(str(e)))

    def search_parameters_correct(self, msg):
        if not msg['body']['link']:
            self.log(logging.INFO, 'Link cannot be empty')
            return False
        return True

    def search(self, msg):
        self.log(logging.INFO, 'Starting')
        asyncio.set_event_loop(asyncio.new_event_loop())

        main_search_id = msg['body']['search_id']
        updater = statusUpdate.get(self.name)
        updater.in_progress(main_search_id)

        if search_cancelled(main_search_id):
            self.log(logging.INFO, 'Search cancelled, finishing')
            updater.success(main_search_id)
            return

        if not self.search_parameters_correct(msg):
            self.log(logging.INFO, 'Parameters incorrect, finishing')
            updater.success(main_search_id)
            return

        try:
            main_search = get_main_search(main_search_id)
            link = msg['body']['link']
            parent = Parent.from_dict(msg['body']['parent'])
            sender = msg['sender']

            result_article = ImportedArticle.objects.get(pk=link)
            self.save_or_skip(result_article, main_search, parent, sender)

            updater.success(main_search_id)
            self.log(logging.INFO, 'Finished')

        except Exception as e:
            print(traceback.format_exc())
            updater.failure(main_search_id)
            self.log(logging.WARNING, 'Failed: {0}'.format(str(e)))
