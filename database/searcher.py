import asyncio
import logging
import string

import unidecode
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from database import stopwords
from database.models import ImportedArticle, ResultArticle
from search.models import SearchParameters, CrawlParameters

postgresql_rank_threshold = 0.05
cosine_similarity_threshold = 0.1
stopwords_list = stopwords.polish


def remove_diacritics(str):
    return unidecode.unidecode(str)


def remove_stopwords(text):
    return [w for w in text if w not in stopwords_list]


class Searcher(SyncConsumer):

    def search(self, data):
        logging.info('Database searcher: starting')

        crawl_parameters = CrawlParameters.from_dict(data["parameters"])

        search_id = data.get("search_id")
        search_parameters = None
        if search_id is not None:
            search_parameters = SearchParameters.objects.get(id=search_id)

        title_without_stop = ' '.join(remove_stopwords(
            crawl_parameters.title
                .translate(str.maketrans('', '', string.punctuation))
                .split()))

        vector = SearchVector('title', 'content', config='public.polish')
        query = SearchQuery(title_without_stop, config='public.polish')
        result = ImportedArticle.objects \
            .annotate(rank=SearchRank(vector, query)) \
            .filter(rank__gte=postgresql_rank_threshold) \
            .order_by('-rank')

        for result_article in result:
            result_content = result_article.content

            query_content = crawl_parameters.content

            similarity = self.count_similarity(query_content, result_content)
            article = ResultArticle(similarity=similarity, page=result_article.page, date=result_article.date,
                                    link=result_article.link, title=result_article.title,
                                    content=result_article.content)
            if article.similarity > cosine_similarity_threshold:
                article.save()
                if search_parameters is not None:
                    article.searches.add(search_parameters)

        asyncio.set_event_loop(asyncio.new_event_loop())
        sender_id = data["id"]
        async_to_sync(self.channel_layer.group_send)(
            sender_id,
            {
                'type': 'send_done',
                'message': 'db_searcher'
            }
        )

    def count_similarity(self, text1, text2):
        # preprocessing
        texts = [[w.lower() for w in text.translate(str.maketrans('', '', string.punctuation)).split()] for text in
                 [text1, text2]]
        texts = [remove_stopwords(text) for text in texts]
        texts = [remove_diacritics(' '.join(text)) for text in texts]

        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(texts)

        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return sim[0][0]
