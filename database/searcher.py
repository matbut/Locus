import asyncio
import logging
import numpy as np
import string

from channels.consumer import SyncConsumer
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from common.crawlerUtils import retrieve_params, group_send_message
from common.statusUpdate import StatusUpdater
from common.textUtils import remove_diacritics, remove_stopwords
from database.models import ImportedArticle, ResultArticle

component = 'db'


def log(level, message):
    logging.log(level, '[db] {0}'.format(message))


postgresql_rank_threshold = 0.3
cosine_similarity_threshold = 0.13


def prepare_title(crawl_parameters):
    return ' '.join(remove_stopwords(
        crawl_parameters.title
            .translate(str.maketrans('', '', string.punctuation))
            .split()))


def count_similarity(text1, text2, top=5):
    # preprocessing
    texts = [[w.lower() for w in text.translate(str.maketrans('', '', string.punctuation)).split()] for text in
             [text1, text2]]
    texts = [remove_stopwords(text) for text in texts]
    texts = [remove_diacritics(' '.join(text)) for text in texts]

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(texts)

    feature_array = np.array(tfidf_vectorizer.get_feature_names())
    common1 = np.argsort(tfidf_matrix[0].toarray()).flatten()[::-1]
    common2 = np.argsort(tfidf_matrix[1].toarray()).flatten()[::-1]

    sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return sim[0][0], feature_array[common1][:top], feature_array[common2][:top]


def save_or_skip(result_article, crawl_parameters, search_parameters):
    result_content = result_article.content

    query_content = crawl_parameters.content

    similarity, top_query, top_result = count_similarity(query_content, result_content, top=5)
    article = ResultArticle(similarity=similarity, page=result_article.page, date=result_article.date,
                            link=result_article.link, title=result_article.title,
                            content=result_article.content, top_words=','.join(top_result))
    if article.similarity > cosine_similarity_threshold:
        article.save()
        if search_parameters is not None:
            article.searches.add(search_parameters)


def find_articles(title_without_stop):
    vector = SearchVector('title', 'content', config='public.polish')
    query = SearchQuery(title_without_stop, config='public.polish')
    return ImportedArticle.objects \
        .annotate(rank=SearchRank(vector, query)) \
        .filter(rank__gte=postgresql_rank_threshold) \
        .order_by('-rank')


class Searcher(SyncConsumer):

    def search(self, data):
        log(logging.INFO, 'Starting')
        asyncio.set_event_loop(asyncio.new_event_loop())
        sender_id = data['id']

        updater = StatusUpdater('db_searcher')
        updater.in_progress()

        try:
            search_parameters, crawl_parameters = retrieve_params(data)

            title_without_stop = prepare_title(crawl_parameters)
            result = find_articles(title_without_stop)

            for result_article in result:
                save_or_skip(result_article, crawl_parameters, search_parameters)

            updater.success()

            group_send_message(component, self.channel_layer, sender_id, 'send_done', 'db_searcher')

        except Exception as e:
            updater.failure()
            message = 'db_searcher: {0}'.format(str(e))
            group_send_message(component, self.channel_layer, sender_id, 'send_failure', message)
