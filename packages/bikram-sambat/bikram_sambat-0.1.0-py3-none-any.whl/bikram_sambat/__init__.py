"""A comprehensive Python library for the Bikram Sambat (BS) calendar system.

`bikram_sambat` provides a full suite of date and time objects that are drop-in
replacements for Python's standard `datetime` library. It enables intuitive
and accurate handling of the Nepali calendar, including date creation, arithmetic,
formatting, and conversion to and from the Gregorian (AD) calendar.

The library is designed to be easy to use for developers familiar with Python's
`datetime` module, while also providing powerful, BS-specific features like
Nepali numerals and names in formatted strings.

Key Features:
    - `date`, `time`, and `datetime` objects that are subclasses of their
      standard Python counterparts.
    - Seamless conversion between Bikram Sambat and Gregorian dates.
    - Full support for timezone-aware datetimes using `pytz`.
    - Rich formatting and parsing capabilities (`strftime`, `fromstrftime`) with
      support for both English and Nepali (Unicode) strings.
    - All arithmetic operations (`+`, `-`) work as expected with `timedelta`.
    - Clean, modern, and fully-documented API.

Getting Started:
    Here is a quick example of how to use the library:

    >>> from bikram_sambat import date, datetime, timedelta, tz
    >>> import datetime as pydt

    >>> # Create a BS date
    >>> bs_date = date(2081, 4, 15)
    >>> print(f"BS Date: {bs_date}")
    BS Date: 2081-04-15

    >>> # Convert to Gregorian
    >>> greg_date = bs_date.togregorian()
    >>> print(f"Gregorian Date: {greg_date}")
    Gregorian Date: 2024-07-30

    >>> # Create a timezone-aware BS datetime in Nepal
    >>> bs_dt_aware = datetime(2081, 5, 1, 10, 30, tzinfo=tz.nepal)
    >>> print(f"Aware BS Datetime: {bs_dt_aware}")
    Aware BS Datetime: 2081-05-01T10:30:00+05:45

    >>> # Format in Nepali
    >>> formatted = bs_dt_aware.strftime("%G, %N %D, %K साल, %i:%l %P")
    >>> print(f"Formatted in Nepali: {formatted}")
    Formatted in Nepali: बुधवार, भदौ १६, २०८१ साल, १०:३० पहिले

    >>> # Perform arithmetic
    >>> event_date = date(2082, 1, 1)
    >>> days_until_event = event_date - date.today()
    >>> print(f"Days until new year 2082: {days_until_event.days}")
"""

# Core classes
from .bs_date import BSDate as date
from .bs_time import BSTime as time
from .bs_datetime import BSDatetime as datetime
from .bs_timedelta import BSTimedelta as timedelta

# Exceptions
from .exceptions import (
    BikramSambatError,
    DateOutOfRangeError,
    InvalidDateError,
    InvalidTypeError,
)

from . import bs_timezone as tz
from .bs_timezone import (
    nepal,
    utc,
    india,
    get_timezone,
    all_timezones_list,
    tzinfo_base,
)


from . import constants


__all__ = [
    # Core classes
    "date",
    "time",
    "datetime",
    "timedelta",
    # Exceptions
    "BikramSambatError",
    "DateOutOfRangeError",
    "InvalidDateError",
    "InvalidTypeError",
    # Timezone utilities
    "tz",
    "nepal",
    "utc",
    "india",
    "get_timezone",
    "all_timezones_list",
    "tzinfo_base",
    # Constants module
    "constants",
]

__version__ = "0.1.0"
