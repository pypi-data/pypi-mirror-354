from os import getenv
from datetime import datetime, timedelta, UTC

from .default import DEFAULT


class Config:
    """
    Globally adjustable module defaults. Values can be adjusted by setting the appropriate environment variable, OR
    by overriding the Config class value BEFORE calling any functions from the module.

    Ie:
        from shortcuts.date import Config

        Config.naive = False
    """

    # return naive datetime object
    naive: bool = getenv('SHORTCUTS_DATE_NAIVE', 'true').lower() == 'true'

    # return utc time instead of local time
    utc: bool = getenv('SHORTCUTS_DATE_UTC', 'false').lower() == 'true'


def _time_value(naive, utc, add=False, subtract=False, **intervals):
    """
    Internal utility function that returns requested datetime object, optionally adding/subtracting interval values
    """

    # set defaults
    if naive is DEFAULT:
        naive = Config.naive

    if utc is DEFAULT:
        utc = Config.utc

    # generate requested datetime value
    if utc:
        value = datetime.now(UTC)

        if naive:
            value = value.replace(tzinfo=None)

    else:
        value = datetime.now()

        if not naive:
            value = value.astimezone()

    # add/subtract intervals
    if add:
        value = value + timedelta(**intervals)

    elif subtract:
        value = value - timedelta(**intervals)

    return value


def time_now(
        naive: bool = DEFAULT,
        utc: bool = DEFAULT
) -> datetime:
    """
    Get current datetime.

    Args:
        naive: Whether to return naive or timezone-aware datetime. Defaults to Config.naive value
        utc: Whether to return local or utc datetime. Defaults to Config.utc value

    Returns:
        datetime object
    """
    return _time_value(naive=naive, utc=utc)


def time_in(
        seconds: int = 0,
        minutes: int = 0,
        hours: int = 0,
        days: int = 0,
        weeks: int = 0,
        microseconds: int = 0,
        milliseconds: int = 0,
        naive: bool = DEFAULT,
        utc: bool = DEFAULT
) -> datetime:
    """
    Get a future datetime object, ie: until = time_in(minutes=10)

    Args:
        seconds: Number of seconds to add
        minutes: Number of minutes to add
        hours: Number of hours to add
        days: Number of days to add
        weeks: Number of weeks to add
        microseconds: Number of microseconds to add
        milliseconds: Number of milliseconds to add
        naive: Whether to return naive or timezone-aware datetime. Defaults to Config.naive value
        utc: Whether to return local or utc datetime. Defaults to Config.utc value

    Returns:
        datetime object
    """

    return _time_value(
        naive=naive,
        utc=utc,
        add=True,
        seconds=seconds,
        minutes=minutes,
        hours=hours,
        days=days,
        weeks=weeks,
        microseconds=microseconds,
        milliseconds=milliseconds
    )


def time_ago(
        seconds: int = 0,
        minutes: int = 0,
        hours: int = 0,
        days: int = 0,
        weeks: int = 0,
        microseconds: int = 0,
        milliseconds: int = 0,
        naive: bool = DEFAULT,
        utc: bool = DEFAULT
) -> datetime:
    """
    Get a past datetime object, ie: since = time_ago(minutes=5)

    Args:
        seconds: Number of seconds to subtract
        minutes: Number of minutes to subtract
        hours: Number of hours to subtract
        days: Number of days to subtract
        weeks: Number of weeks to subtract
        microseconds: Number of microseconds to subtract
        milliseconds: Number of milliseconds to subtract
        naive: Whether to return naive or timezone-aware datetime. Defaults to Config.naive value
        utc: Whether to return local or utc datetime. Defaults to Config.utc value

    Returns:
        datetime object
    """

    return _time_value(
        naive=naive,
        utc=utc,
        subtract=True,
        seconds=seconds,
        minutes=minutes,
        hours=hours,
        days=days,
        weeks=weeks,
        microseconds=microseconds,
        milliseconds=milliseconds
    )
