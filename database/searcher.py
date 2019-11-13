import asyncio
import logging

import unidecode
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from database import stopwords
from database.models import ImportedArticle, ResultArticle
from search.models import SearchParameters


def remove_diacritics(str):
    return unidecode.unidecode(str)


class Searcher(SyncConsumer):

    def search(self, data):
        logging.info('Database searcher: starting')

        search_id = data["parameters"]
        search_parameters = SearchParameters.objects.get(id=search_id)

        result = ImportedArticle.objects.filter(title__contains='Sześcioraczki') #TODO use PostgreSQL full text search

        # TODO start

        result_article = result[0]
        result_content = result_article.content

        query_content = search_parameters.content

        similarity = self.count_similarity(query_content, result_content)
        article = ResultArticle(similarity=similarity, page=result_article.page, date=result_article.date,
                                link=result_article.link, title=result_article.title, content=result_article.content)
        article.save()


        # TODO end

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
        stops = stopwords.polish
        texts = [[w.lower() for w in text.split()] for text in [text1, text2]]
        texts = [[w for w in text if w not in stops] for text in texts]
        texts = [remove_diacritics(' '.join(text)) for text in texts]

        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(texts)

        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return sim[0][0]
