import re
from datetime import datetime
from datetime import timedelta

from common.textUtils import remove_diacritics

locale_months = {
    1: ['sty'],
    2: ['lut'],
    3: ['mar'],
    4: ['kwi'],
    5: ['maj'],
    6: ['cze'],
    7: ['lip'],
    8: ['sie'],
    9: ['wrz'],
    10: ['paz'],
    11: ['lis'],
    12: ['gru']
}


def inverse(lm):
    inv = {}
    for key in lm.keys():
        for val in lm[key]:
            inv[val] = key
    return inv


inversed_locale_months = inverse(locale_months)


def retrieve_access_key():
    from pathlib import Path
    home_dir = str(Path.home())
    credentials = open("{0}/.locus/credentials".format(home_dir), "r")
    content = credentials.read()
    m = re.match(r"key (?P<key>\w+)\nengine_id (?P<engine_id>\w+:\w+)", content)
    key = m.groupdict()
    return key["key"], key["engine_id"]


def retrieve_date(snippet):
    if snippet is None:
        return None
    try:
        m = re.match(r"(?P<date>(\w|\s)+)\s...\s\w+", remove_diacritics(snippet))
        if m is None:
            return
        key = m.groupdict()
        date_str = key['date']
        if date_str.endswith('temu'):
            return retrieve_date_ago(date_str)
        else:
            return retrieve_pure_date(date_str)
    except:
        return None


def retrieve_pure_date(date_str):
    m = re.match(r'(?P<day>\d+)\s(?P<month>\w+)\s(?P<year>\d+)', date_str.lower())
    groups = m.groupdict()
    day = int(groups['day'])
    month = int(inversed_locale_months[groups['month']])
    year = int(groups['year'])
    return datetime(year, month, day)


def retrieve_date_ago(date_str):
    m = re.match(r'(?P<number>\d+)\s(?P<unit>\w+)\stemu', date_str)
    if m is None:
        return
    now = datetime.now()
    groups = m.groupdict()
    unit = groups['unit']
    number = int(groups['number'])

    if unit in ['dni', 'dzien']:
        return (now - timedelta(days=number)).replace(microsecond=0, second=0, minute=0, hour=0)
    if unit in ['godz.', 'godzine']:
        return (now - timedelta(hours=number)).replace(microsecond=0, second=0, minute=0)
    if unit in ['min']:
        return (now - timedelta(minutes=number)).replace(microsecond=0, second=0)
