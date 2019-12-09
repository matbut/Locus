import datetime
import re

from common.textUtils import remove_diacritics

month = {
    'styczen': 'Jan',
    'stycznia': 'Jan',
    'sty': 'Jan',
    'luty': 'Feb',
    'lutego': 'Feb',
    'lut': 'Feb',
    'marzec': 'Mar',
    'marca': 'Mar',
    'mar': 'Mar',
    'kwiecien': 'Apr',
    'kwietnia': 'Apr',
    'kwi': 'Apr',
    'maja': 'May',
    'maj': 'May',
    'czerwiec': 'Jun',
    'czerwca': 'Jun',
    'cze': 'Jun',
    'lipiec': 'Jul',
    'lipca': 'Jul',
    'lip': 'Jul',
    'sierpien': 'Aug',
    'sierpnia': 'Aug',
    'sie': 'Aug',
    'wrzesien': 'Sep',
    'wrzesnia': 'Sep',
    'wrz': 'Sep',
    'pazdziernika': 'Oct',
    'pazdziernik': 'Oct',
    'paz': 'Oct',
    'listopada': 'Nov',
    'listopad': 'Nov',
    'lis': 'Nov',
    'grudzien': 'Dec',
    'grudnia': 'Dec',
    'gru': 'Dec'
}

day = {
    'poniedzialek': '00',
    'pon': '00',
    'pn': '00',
    'wtorek': '01',
    'wt': '01',
    'sroda': '02',
    'sr': '02',
    'czwartek': '03',
    'czw': '03',
    'cz': '03',
    'piatek': '04',
    'pt': '04',
    'sobota': '05',
    'sob': '05',
    'sb': '05',
    'niedziela': '06',
    'nie': '06',
    'nd': '06',
}

LOCALE_MONTH = '%L'
LOCALE_DAY = '%l'


def to_datetime(date_time):
    article_date, article_time = date_time.split(', ')
    return datetime.datetime.strptime(replace_month(article_date, '\d+ (?P<month>[a-zA-Z]+) \d+') + ' ' + article_time,
                                      '%d %b %Y %H:%M')


def replace_month(str_date, regex):
    str_date_normalized = str_date
    groups = re.match(regex, str_date_normalized)
    m = groups.groupdict()['month']
    return str_date_normalized.replace(m, month[m])


def parse_date(date_str, regex):
    date_str = remove_diacritics(date_str.lower())
    if LOCALE_MONTH in regex:
        regex = regex.replace(LOCALE_MONTH, '%b')
        for pl_month in month:
            date_str = date_str.replace(pl_month, month[pl_month])
    if LOCALE_DAY in regex:
        regex = regex.replace(LOCALE_DAY, '%d')
        for pl_day in day:
            date_str = date_str.replace(pl_day, day[pl_day])
    return datetime.datetime.strptime(date_str, regex)
