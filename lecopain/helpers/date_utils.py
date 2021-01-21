import calendar
from datetime import datetime, date
from datetime import timedelta
from aenum import Enum

class Period_Enum(Enum):
    ALL = 'all'
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'

def get_day_range(day):
    start = (day - timedelta(days=1)
            ).replace(hour=23).replace(minute=59).replace(second=59)
    end = day.replace(hour=23).replace(minute=59).replace(second=59)
    return start, end

def get_week_range(year, calendar_week):
    
    week = calendar_week
    if year == datetime.now().year:
        week = calendar_week +1
    
    monday = datetime.strptime(
        f'{year}-{week}-1', "%Y-%W-%w")
    return monday - timedelta(days=7), monday - timedelta(days=1)


def get_month_range(year, calendar_month):
    start = datetime.strptime(f'{year}-{calendar_month}-01', '%Y-%m-%d')
    tmp, day_end = calendar.monthrange(year, calendar_month)
    end = datetime.strptime(f'{year}-{calendar_month}-{day_end}', '%Y-%m-%d')
    return start, end

def dates_range(period, day=datetime.now(), before=0):
    start = 0
    end = 0

    if period == Period_Enum.DAY.value:
        if before > 0:
            day = day- timedelta(days=1)
        start, end = get_day_range(day)
    elif period == Period_Enum.WEEK.value:
        start, end = get_week_range(day.year, day.isocalendar()[1])
    elif period == Period_Enum.MONTH.value:
        if before > 0:
            day = day.replace(day=1) - timedelta(days=1)

        start, end = get_month_range(day.year, day.month)
    return start,end

def get_week_names():
    return {0 : 'Lundi', 1: 'Mardi', 2: 'Mercredi', 3 : 'Jeudi', 4 : 'Vendredi', 5 : 'Samedi', 6 : 'Dimanche'}


#start,end = dates_range(period=Period_Enum.MONTH.value,  before=2)
#print('start : ' + str(start) + ' - ' + str(end))

