import unidecode

from common import stopwords

stopwords_list = stopwords.polish


def remove_diacritics(str):
    return unidecode.unidecode(str)


def remove_stopwords(text):
    return [w for w in text if w not in stopwords_list]
