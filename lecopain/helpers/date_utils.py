import calendar
from datetime import datetime
from datetime import timedelta


def get_start_and_end_date_from_calendar_week(year, calendar_week):
    monday = datetime.strptime(
        f'{year}-{calendar_week}-1', "%Y-%W-%w").date()
    return monday, monday + timedelta(days=6.9)


def get_start_and_end_date_from_calendar_month(year, calendar_month):
    start = datetime.today().replace(day=1)
    tmp, end = calendar.monthrange(year, calendar_month)
    return start, end
