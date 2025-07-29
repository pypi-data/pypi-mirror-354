import sys
from datetime import datetime, time, timezone, tzinfo
from typing import Literal, TypeVar

T_WithTime = TypeVar('T_WithTime', datetime, time)

def parse_timezone(tz: tzinfo|str|Literal['localtime']|None = None) -> tzinfo:
    # ZoneInfo: introduced in Python 3.9
    try:
        from zoneinfo import ZoneInfo
    except ImportError:
        ZoneInfo = None

    if tz is None or tz == 'localtime':
        if not ZoneInfo or sys.platform == 'win32':
            # tzlocal: used to parse timezones from strings on Windows (Windows does not maintain a database of timezones and `tzdata` only is not enough)
            try:
                import tzlocal  # type: ignore
            except ModuleNotFoundError:
                raise ModuleNotFoundError(f"Module 'tzlocal' is required on Windows or on Python < 3.9 to retrieve local timezone") from None
            return tzlocal.get_localzone()
        else:
            return ZoneInfo('localtime')
    elif isinstance(tz, tzinfo):
        return tz
    elif tz == 'UTC':
        return timezone.utc
    elif isinstance(tz, str):
        if not ZoneInfo:
            # pytz: used to parse timezones on Python < 3.9 (no ZoneInfo available)
            try:
                import pytz  # type: ignore
            except ModuleNotFoundError:
                raise ModuleNotFoundError(f"Module 'pytz' is required on Python < 3.9 to parse timezones from strings") from None
            return pytz.timezone(tz)
        if sys.platform == 'win32':
            # tzdata: used to parse timezones from strings through ZoneInfo on Windows (Windows does not maintain a database of timezones)
            try:
                import tzdata
            except ModuleNotFoundError:
                raise ModuleNotFoundError(f"Module 'tzdata' is required on Windows to parse timezones from strings") from None
        return ZoneInfo(tz)
    else:
        raise TypeError(f"Invalid timezone type: {tz} ({type(tz).__name__})")
    

def get_timezone_key(tz: tzinfo|Literal['localtime']|None = None) -> str:
    if tz is None or tz == 'localtime':
        tz = parse_timezone()
    key = getattr(tz, 'key', None)
    if key:
        return key
    raise ValueError(f"{type(tz).__name__} object has no key")


def make_aware(value: T_WithTime, tz: tzinfo|str|None = None) -> T_WithTime:
    """
    Make a datetime aware in the given timezone (use `tz=None` or `tz='localtime'` for the system local timezone or `tz='UTC' for UTC`).
    """
    if value is None:
        return None
    
    if value.tzinfo: # already aware
        return value
    
    tz = parse_timezone(tz)
    if hasattr(tz, 'localize'):
        # See: https://stackoverflow.com/a/6411149
        return tz.localize(value) # type: ignore
    else:
        return value.replace(tzinfo=tz)


def make_naive(value: datetime, tz: tzinfo|str|None = None) -> datetime:
    """
    Make a datetime naive and expressed in the given timezone (use `tz=None` or `tz='localtime'` for the system local timezone or `tz='UTC' for UTC`).
    """
    if value is None:
        return None

    if not value.tzinfo: # already naive
        return value
    
    value = value.astimezone(None if tz is None or tz == 'localtime' else parse_timezone(tz))
    value = value.replace(tzinfo=None)
    return value


def now_aware(tz: tzinfo|str|None = None, *, no_microseconds = False):
    """
    Get the current aware datetime in the given timezone (use `tz=None` or `tz='localtime'` for the system local timezone or `tz='UTC' for UTC`).
    """
    now = datetime.now().astimezone(None if tz is None or tz == 'localtime' else parse_timezone(tz))
    if no_microseconds:
        now = now.replace(microsecond=0)
    return now


def now_naive(tz: tzinfo|str|None = None, *, no_microseconds = False):
    """
    Get the current naive datetime in the given timezone (use `tz=None` or `tz='localtime'` for the system local timezone or `tz='UTC' for UTC`).
    """
    if tz is None or tz == 'localtime':
        now = datetime.now()
    else:
        tz = parse_timezone(tz)
        now = datetime.now(tz=tz).replace(tzinfo=None)

    if no_microseconds:
        now = now.replace(microsecond=0)
    return now
