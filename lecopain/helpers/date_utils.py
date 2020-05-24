import calendar
from datetime import datetime
from datetime import timedelta
from aenum import Enum

class Period_Enum(Enum):
    ALL = 'all'
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'


def get_day_range():
    start = (datetime.now() - timedelta(days=1)
             ).replace(hour=23).replace(minute=59).replace(second=59)
    end = datetime.today().replace(hour=23).replace(minute=59).replace(second=59)
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

def dates_range(period):
    today = datetime.today()
    start = 0
    end = 0

    if period == Period_Enum.DAY.value:
        start, end = get_day_range()
    elif period == Period_Enum.WEEK.value:
        start, end = get_week_range(
            today.year, today.isocalendar()[1])
    elif period == Period_Enum.MONTH.value:
        start, end = get_month_range(
            today.year, today.month)
    return start,end
