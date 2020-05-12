import calendar
from datetime import datetime
from datetime import timedelta


def get_day_range():
    start = datetime.today().replace(hour=0).replace(minute=00)
    end = datetime.today().replace(hour=23).replace(minute=59)
    return start, end


def get_week_range(year, calendar_week):
    monday = datetime.strptime(
        f'{year}-{calendar_week}-1', "%Y-%W-%w").date()
    return monday - timedelta(days=7), monday


def get_month_range(year, calendar_month):
    start = datetime.today().replace(day=1)
    tmp, day_end = calendar.monthrange(year, calendar_month)
    end = datetime.today().replace(day=day_end)
    return start, end
