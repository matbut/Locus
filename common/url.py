import re
from urllib.parse import urlparse

patterns = {
    'www.tvn24.pl': {
        'correct': [
            '^.+\.html$',
        ],
        'incorrect': []
    },
    'www.tvp.info': {
        'correct': [],
        'incorrect': [
            '^.+/(tag|polska|swiat|wideo|opinie|pogoda|zobacz-online|twoje-info|biznes|spoleczenstwo|kultura|nauka|rozmaitosci|polska-to-wiecej|raporty|foto)$',
            '^.+www.tvp.info/?$',
        ]
    },
    'www.rmf.fm': {
        'correct': [
            '^.+\.html$',
        ],
        'incorrect': []
    },
    'wiadomosci.radiozet.pl': {
        'correct': [],
        'incorrect': [
            '^.+/(Polska|Swiat|Polityka|Gosc-Radia-ZET|Nauka|Pogoda|Ciekawostki)$',
            '^.+wiadomosci.radiozet.pl/?$',
        ]
    },
    'www.wprost.pl': {
        'correct': [
            '^.+\.html$',
        ],
        'incorrect': []
    },
    'wiadomosci.wp.pl': {
        'correct': [],
        'incorrect': [
            '^.+/(polska|swiat|spoleczenstwo|polityka|przestepczosc|matura|tylko-w-wp|dzien-dobry-wp|wideo|najnowsze)$',
            '^.+wiadomosci.wp.pl/?$',
        ]
    },
    'fakty.interia.pl': {
        'correct': [],
        'incorrect': [
            '^.+/(polska|prasa|swiat|wideo|raporty|konkursy|tylko-u-nas|galerie|autor|opinie|nauka|wiadomosci-lokalne|dolnoslaskie|kujawsko-pomorskie|lodzkie|lubelskie|lubuskie|malopolskie|mazowieckie|opolskie|podkarpackie|podlaskie|pomorskie|slaskie|swietokrzyskie|warminsko-mazurskie|wielkopolskie|zachodniopomorskie)$',
            '^.+opinie/[^/]+/?$',
            '^.+autor/[^/]+/?$',
            '^.+galerie/(kraj|swiat|polskalokalna|kultura|ciekawostki|styl-zycia|obyczaje|nauka|natura|religia|historia|wasze-zdjecia)$',
            '^.+fakty.interia.pl/?$',
        ]
    },
}


def get_domain(url):
    return urlparse(url).netloc


def patterns_not_exist_or_are_empty(regex_list):
    return regex_list is None or (not regex_list['incorrect'] and not regex_list['correct'])


def is_valid(url):
    if not re.match('^https?://.*/.+$', url):
        return False
    domain = get_domain(url)
    regex_list = patterns.get(domain)
    if patterns_not_exist_or_are_empty(regex_list):
        return True
    if regex_list['incorrect']:
        return not any([bool(re.match(regex, url)) for regex in regex_list['incorrect']])
    else:
        return any([bool(re.match(regex, url)) for regex in regex_list['correct']])


def clean_youtube_url(url):
    m = re.match(r'.+/watch\?v=(?P<id>.+)(&.*)?', url)
    if not m:
        return url
    groups = m.groupdict()
    video_id = groups['id']
    return 'https://www.youtube.com/watch?v=' + video_id


def clean_url(url):
    if get_domain(url) == 'www.youtube.com':
        return clean_youtube_url(url)
    return url.split('?')[0].split('#')[0]
