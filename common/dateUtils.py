from dateutil.relativedelta import relativedelta, MO
from dateutil.rrule import rrule, MONTHLY, YEARLY, WEEKLY, DAILY


def count_end_date(aggregation, start_date):
    if aggregation == 'day':
        return start_date + relativedelta(days=+1)
    if aggregation == 'week':
        return start_date + relativedelta(weeks=+1)
    if aggregation == 'month':
        return start_date + relativedelta(months=+1)
    if aggregation == 'year':
        return start_date + relativedelta(years=+1)


def date_range(aggregation, start_date, end_date, offset=False):
    if aggregation == 'day':
        return days_date_range(start_date, end_date, offset)
    if aggregation == 'week':
        return weeks_date_range(start_date, end_date, offset)
    if aggregation == 'month':
        return months_date_range(start_date, end_date, offset)
    if aggregation == 'year':
        return years_date_range(start_date, end_date, offset)


def days_date_range(start_date, end_date, offset=False):
    if offset:
        start_date = start_date + relativedelta(days=-1)
        end_date = end_date + relativedelta(days=+2)
    return rrule(DAILY, dtstart=start_date, until=end_date)


def weeks_date_range(start_date, end_date, offset=False):
    if offset:
        start_date = start_date + relativedelta(weeks=-1, weekday=MO(-1))
        end_date = end_date + relativedelta(weekday=MO(+1))
    return rrule(WEEKLY, dtstart=start_date, until=end_date)


def months_date_range(start_date, end_date, offset=False):
    if offset:
        start_date = start_date + relativedelta(months=-1, day=1)
        end_date = end_date + relativedelta(months=+1, day=1)
    return rrule(MONTHLY, dtstart=start_date, until=end_date)


def years_date_range(start_date, end_date, offset=False):
    if offset:
        start_date = start_date + relativedelta(years=-1, month=1, day=1)
        end_date = end_date + relativedelta(years=+1, month=1, day=1)
    return rrule(YEARLY, dtstart=start_date, until=end_date)
