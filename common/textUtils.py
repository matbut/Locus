import numpy as np
import string

import unidecode
from sklearn.feature_extraction.text import CountVectorizer

from common import stopwords

stopwords_list = stopwords.polish


def remove_diacritics(s):
    return unidecode.unidecode(s)


def remove_stopwords(s):
    if isinstance(s, list):
        return [w for w in s if w not in stopwords_list]
    return ' '.join([w for w in s.split() if w not in stopwords_list])


def remove_punctuation(s):
    return s.translate(str.maketrans('', '', string.punctuation))


def get_top_words_count(texts, top, text_num=0):
    if not texts or not any(bool(text) for text in texts):
        return [], []
    count_vectorizer = CountVectorizer()
    count_matrix = count_vectorizer.fit_transform(texts)
    features = count_vectorizer.get_feature_names()
    indices = np.argsort(count_matrix[text_num].toarray().astype('int')).flatten()[::-1]
    return np.array(features)[indices][:top], count_matrix.toarray()[text_num][indices][:top]
