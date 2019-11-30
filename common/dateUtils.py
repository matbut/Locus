from datetime import datetime
from datetime import timedelta

from dateutil.relativedelta import relativedelta, MO
from dateutil.rrule import rrule, MONTHLY, YEARLY


def days_date_range(start_date, end_date):
    start_date = start_date - timedelta(1)
    end_date = end_date + timedelta(2)

    for n in range(int((end_date - start_date).days)):
        yield (start_date + timedelta(n))


def weeks_date_range(start_date, end_date):
    start_date = start_date + relativedelta(weeks=-1, weekday=MO(-1))
    end_date = end_date + relativedelta(weeks=+1, weekday=MO(+1))

    for n in range(0, int((end_date - start_date).days), 7):
        yield ((start_date + timedelta(n)), (start_date + timedelta(n + 6)))


def months_date_range(start_date, end_date):
    start_date = start_date + relativedelta(months=-1, day=1)
    end_date = end_date + relativedelta(months=+1, day=1)

    return [(d.month, d.year) for d in rrule(MONTHLY, dtstart=start_date, until=end_date)]


def years_date_range(start_date, end_date):
    start_date = start_date + relativedelta(years=-1, month=1, day=1)
    end_date = end_date + relativedelta(years=+1, month=1, day=1)

    return [d.year for d in rrule(YEARLY, dtstart=start_date, until=end_date)]
