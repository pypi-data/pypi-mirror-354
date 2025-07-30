"""Utils to work with time"""

import datetime  # keep around! It's to be able to access the mother of datetime
from datetime import datetime as dt
from dateutil import tz

__author__ = 'tcw'

second_ms = 1000.0
second_ns = 1e9
minute_ms = float(60 * second_ms)
five_mn_ms = 5 * minute_ms
hour_ms = float(60 * minute_ms)
day_ms = float(24 * hour_ms)
day_hours = float(24)

hour_as_day = 1 / day_hours
day_minutes = float(24 * 60)
minute_as_day = 1 / day_minutes
day_seconds = float(24 * 3600)
second_as_day = 1 / day_seconds

epoch = dt.utcfromtimestamp(0)


def utcnow_timestamp():
    return (dt.utcnow() - epoch).total_seconds()


def utcnow_ms():
    return (dt.utcnow() - epoch).total_seconds() * second_ms


def utcnow_ns():
    return (dt.utcnow() - epoch).total_seconds() * second_ns


def utc_datetime_to_utc_ms(utc_datetime):
    return (utc_datetime - epoch).total_seconds() * second_ms


def utc_ms_to_utc_datetime(ums):
    return dt.utcfromtimestamp(ums / second_ms)


def utc_ms_to_local_datetime(ums):
    return dt.fromtimestamp(ums / second_ms)


def utc_to_local(utc_date):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    return utc_date.replace(tzinfo=from_zone).astimezone(to_zone)


def local_to_utc(local_date):
    from_zone = tz.tzlocal()
    to_zone = tz.tzutc()
    return local_date.replace(tzinfo=from_zone).astimezone(to_zone)


def day_utc_ms_from_utc_ms(ums):
    """
    Get a utc_ms corresponding to midnight of the day of the input ums
    :param ums: utc in milliseconds
    :return: utc_ms corresponding to midnight of the day of the input ums
    >>> from numpy.random import randint
    >>> ums = randint(1, 2000000000000)
    >>> day_ums = utc_datetime_to_utc_ms(day_datetime_from_utc_ms(ums))
    >>> int(day_utc_ms_from_utc_ms(day_ums)) == int(day_ums)
    True
    """
    return int(day_ms * (ums // day_ms))


def day_datetime_from_datetime(date_time):
    """
    Get a datetime corresponding to midnight of the day of the input datetime
    :param date_time: (utc) datetime
    :return:
    >>> from numpy.random import randint
    >>> ums = randint(1, 2000000000000)
    >>> date_time = utc_ms_to_utc_datetime(ums)
    >>> day_ums = day_utc_ms_from_utc_ms(ums)
    >>> day_datetime_from_datetime(date_time) == utc_ms_to_utc_datetime(day_ums)
    True
    """
    return datetime.datetime(date_time.year, date_time.month, date_time.day)


def day_datetime_from_utc_ms(ums):
    """
    Get a datetime corresponding to midnight of the day of the input ums
    :param ums: utc in milliseconds
    :return: datetime corresponding to midnight of the day of the input ums
    >>> from numpy.random import randint
    >>> ums = randint(1, 2000000000000)
    >>> day_datetime = utc_ms_to_utc_datetime(day_utc_ms_from_utc_ms(ums))
    >>> day_datetime_from_utc_ms(ums) == day_datetime
    True
    """
    dt = utc_ms_to_utc_datetime(ums)
    return datetime.datetime(dt.year, dt.month, dt.day)


#################### Display


def seconds_to_mmss_str(s):
    return '{:.0f}m{:02.0f}s'.format(s / 60, s % 60)


#################### Deprecated


def unix_time_ms_to_datetime(ums):
    raise DeprecationWarning('Use utc_ms_to_local_datetime instead')


def datetime_to_unix_time_ms(date):
    raise DeprecationWarning('Use utc_datetime_to_utc_ms instead')




def utc_datetime_to_iso_string(utc_datetime):
    """
    Convert a UTC datetime object to an ISO 8601 formatted string.
    
    Parameters:
        utc_datetime (datetime): A datetime object in UTC.
        
    Returns:
        str: ISO 8601 formatted string representing the input datetime.
    
    Examples:
    >>> from datetime import datetime
    >>> utc_datetime_to_iso_string(datetime(2023, 12, 25, 15, 30))
    '2023-12-25T15:30:00'
    """
    return utc_datetime.isoformat()


def iso_string_to_utc_datetime(iso_string):
    """
    Convert an ISO 8601 formatted string to a UTC datetime object.
    
    Parameters:
        iso_string (str): ISO 8601 formatted string.
        
    Returns:
        datetime: A datetime object in UTC corresponding to the input string.
    
    Examples:
    >>> iso_string_to_utc_datetime('2023-12-25T15:30:00')
    datetime.datetime(2023, 12, 25, 15, 30)
    """
    from dateutil.parser import parse
    return parse(iso_string)


def add_days_to_utc_datetime(utc_datetime, days):
    """
    Add a specified number of days to a UTC datetime object.
    
    Parameters:
        utc_datetime (datetime): A datetime object in UTC.
        days (int): Number of days to add.
        
    Returns:
        datetime: A datetime object in UTC after adding the specified days.
    
    Examples:
    >>> from datetime import datetime
    >>> add_days_to_utc_datetime(datetime(2023, 12, 25), 10)
    datetime.datetime(2024, 1, 4, 0, 0)
    """
    return utc_datetime + datetime.timedelta(days=days)


def format_datetime_to_custom_string(date_time, format_string="%Y-%m-%d %H:%M:%S"):
    """
    Format a datetime object into a custom formatted string based on the provided format.
    
    Parameters:
        date_time (datetime): A datetime object.
        format_string (str): Format string to use for formatting the datetime object.
        
    Returns:
        str: Formatted datetime string.
    
    Examples:
    >>> from datetime import datetime
    >>> format_datetime_to_custom_string(datetime(2023, 12, 25, 15, 30), "%d-%m-%Y %H:%M")
    '25-12-2023 15:30'
    """
    return date_time.strftime(format_string)
