import datetime
import re
import unicodedata

month = {
    'styczen': 'Jan',
    'stycznia': 'Jan',
    'luty': 'Feb',
    'lutego': 'Feb',
    'marzec': 'Mar',
    'kwiecien': 'Apr',
    'kwietnia': 'Apr',
    'maj': 'May',
    'maja': 'May',
    'czerwiec': 'Jun',
    'czerwca': 'Jun',
    'lipiec': 'Jul',
    'lipca': 'Jul',
    'sierpien': 'Aug',
    'sierpnia': 'Aug',
    'wrzesien': 'Sep',
    'wrzesnia': 'Sep',
    'pazdziernik': 'Oct',
    'pazdziernika': 'Oct',
    'listopad': 'Nov',
    'listopada': 'Nov',
    'grudzien': 'Dec',
    'grudnia': 'Dec'
}


def to_datetime(date_time):
    article_date, article_time = date_time.split(', ')
    return datetime.datetime.strptime(replace_month(article_date) + ' ' + article_time, '%d %b %Y %H:%M')


def replace_month(str_date):
    str_date_normalized = str_date
    groups = re.match('\\d+ (?P<month>[a-zA-Z]+) \\d+', str_date_normalized)
    m = groups.groupdict()['month']
    return str_date_normalized.replace(m, month[m])


def remove_diacritics(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
