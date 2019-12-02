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


LOCALE_MONTH_SHORT = '%l'
LOCALE_MONTH_LONG = '%L'


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
    print(date_str)
    if LOCALE_MONTH_LONG in regex:
        regex = regex.replace(LOCALE_MONTH_LONG, '%b')
        for pl_month in month:
            date_str = date_str.replace(pl_month, month[pl_month])
    if LOCALE_MONTH_SHORT in regex:
        regex = regex.replace(LOCALE_MONTH_SHORT, '%b')
        for pl_month in month:
            date_str = date_str.replace(pl_month, month[pl_month])
    return datetime.datetime.strptime(date_str, regex)
