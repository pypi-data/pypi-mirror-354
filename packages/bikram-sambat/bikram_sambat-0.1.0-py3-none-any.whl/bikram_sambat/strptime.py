"""Provides string parsing utilities for Bikram Sambat (BS) dates and times.

This module is the backend for the `fromstrftime` class methods on the `BSDate`,
`BSTime`, and `BSDatetime` objects. It is responsible for converting a string
representation of a date/time into a corresponding object, based on a
provided format string.

The implementation is inspired by Python's standard `_strptime` module, using
regular expressions to match and extract date/time components. It supports all
BS-specific format directives, including those for Nepali numerals and names.

Note:
    This is an internal module and its functions are not part of the public API.
"""

import re
import locale
import pytz

import datetime as _dt
from typing import Tuple
from functools import lru_cache

try:
    from _thread import allocate_lock as _thread_allocate_lock
except ImportError:
    from _dummy_thread import allocate_lock as _thread_allocate_lock

from .bs_date import BSDate
from .bs_time import BSTime
from .bs_datetime import BSDatetime
from .constants import (
    FORMAT_A,
    FORMAT_a,
    FORMAT_G,
    FORMAT_w,
    FORMAT_d,
    FORMAT_D,
    FORMAT_b,
    FORMAT_B,
    FORMAT_N,
    FORMAT_m,
    FORMAT_n,
    FORMAT_y,
    FORMAT_k,
    FORMAT_Y,
    FORMAT_K,
    FORMAT_H,
    FORMAT_h,
    FORMAT_I,
    FORMAT_i,
    FORMAT_p,
    FORMAT_P,
    FORMAT_M,
    FORMAT_l,
    FORMAT_S,
    FORMAT_s,
    FORMAT_f,
    FORMAT_t,
    FORMAT_z,
    FORMAT_Z,
    FORMAT_j,
    FORMAT_J,
    FORMAT_U,
    FORMAT_c,
    FORMAT_x,
    FORMAT_X,
    NEPALI_DIGITS,
    MONTH_NAMES_FULL,
    MONTH_NAMES_SHORT,
    MONTH_NAMES_FULL_NEPALI,
    WEEKDAY_NAMES_FULL,
    WEEKDAY_NAMES_SHORT,
    WEEKDAY_NAMES_FULL_NEPALI,
    AM_PM_ENGLISH,
    AM_PM_NEPALI,
)


class _TimeRE:
    """A regular expression-based parser for date/time format strings.

    This class compiles format strings (e.g., "%Y-%m-%d") into regular
    expressions that can be used to parse date/time strings. It caches the
    compiled regex patterns to improve performance for repeated calls with the
    same format.
    """

    def __init__(self):
        """Initializes the regex compiler and cache."""

        self._cache = {}
        self.locale_time = locale.getlocale(locale.LC_TIME)

    def __seqToRE(self, seq: list, directive: str) -> str:
        """Converts a sequence of strings into a regex OR-pattern.

        Args:
            seq (list): A list of strings (e.g., month or weekday names).
            directive (str): The name for the regex capturing group.

        Returns:
            str: A regex pattern string.
        """
        return r"(?P<{}>{})".format(directive, "|".join(re.escape(s) for s in seq if s))

    @lru_cache(maxsize=128)
    def compile(self, format: str) -> re.Pattern:
        """Compiles a format string into a regular expression object.

        This method translates each format directive (e.g., %Y, %m) into its
        corresponding regex pattern and combines them into a single pattern
        for matching. Results are cached using `lru_cache`.

        Args:
            format (str): The `strftime`-style format string.

        Returns:
            re.Pattern: The compiled regular expression object.
        """
        if format in self._cache:
            return self._cache[format]

        directives = {
            FORMAT_a[1:]: self.__seqToRE(WEEKDAY_NAMES_SHORT, "a"),
            FORMAT_A[1:]: self.__seqToRE(WEEKDAY_NAMES_FULL, "A"),
            FORMAT_G[1:]: self.__seqToRE(WEEKDAY_NAMES_FULL_NEPALI, "G"),
            FORMAT_w[1:]: r"(?P<w>[0-6])",
            FORMAT_d[1:]: r"(?P<d>3[0-2]|[0-2]\d|[1-9])",
            FORMAT_D[1:]: r"(?P<D>3[0-2]|[0-2]\d|[1-9])",
            FORMAT_b[1:]: self.__seqToRE(MONTH_NAMES_SHORT, "b"),
            FORMAT_B[1:]: self.__seqToRE(MONTH_NAMES_FULL, "B"),
            FORMAT_N[1:]: self.__seqToRE(MONTH_NAMES_FULL_NEPALI, "N"),
            FORMAT_m[1:]: r"(?P<m>1[0-2]|0[1-9]|[1-9])",
            FORMAT_n[1:]: r"(?P<n>1[0-2]|0[1-9]|[1-9])",
            FORMAT_y[1:]: r"(?P<y>\d\d)",
            FORMAT_k[1:]: r"(?P<k>\d\d)",
            FORMAT_Y[1:]: r"(?P<Y>\d{4})",
            FORMAT_K[1:]: r"(?P<Y>\d{4})",
            FORMAT_H[1:]: r"(?P<H>2[0-3]|[0-1]\d|\d)",
            FORMAT_h[1:]: r"(?P<H>2[0-3]|[0-1]\d|\d)",
            FORMAT_I[1:]: r"(?P<I>1[0-2]|0[1-9]|[1-9])",
            FORMAT_i[1:]: r"(?P<I>1[0-2]|0[1-9]|[1-9])",
            FORMAT_p[1:]: self.__seqToRE(AM_PM_ENGLISH, "p"),
            FORMAT_P[1:]: self.__seqToRE(AM_PM_NEPALI, "P"),
            FORMAT_M[1:]: r"(?P<M>[0-5]\d|\d)",
            FORMAT_l[1:]: r"(?P<M>[0-5]\d|\d)",
            FORMAT_S[1:]: r"(?P<S>6[0-1]|[0-5]\d|\d)",
            FORMAT_s[1:]: r"(?P<S>6[0-1]|[0-5]\d|\d)",
            FORMAT_f[1:]: r"(?P<f>[0-9]{1,6})",
            FORMAT_t[1:]: r"(?P<f>[0-9]{1,6})",
            FORMAT_z[1:]: r"(?P<z>[+-]\d\d[0-5]\d)",
            FORMAT_Z[1:]: r"(?P<Z>[A-Za-z_/]+)",
            FORMAT_j[
                1:
            ]: r"(?P<j>36[0-6]|3[0-5]\d|[1-2]\d\d|0[1-9]\d|00[1-9]|[1-9]\d|0[1-9]|[1-9])",
            FORMAT_J[
                1:
            ]: r"(?P<j>36[0-6]|3[0-5]\d|[1-2]\d\d|0[1-9]\d|00[1-9]|[1-9]\d|0[1-9]|[1-9])",
            FORMAT_U[1:]: r"(?P<U>5[0-3]|[0-4]\d|\d)",
            FORMAT_c[1:]: r"(?P<c>%a %b %d %H:%M:%S %Y)",
            FORMAT_x[1:]: r"(?P<x>\d{4}-(?:1[0-2]|0[1-9])-(?:3[0-2]|[0-2]\d|[1-9]))",
            FORMAT_X[1:]: r"(?P<X>%H:%M:%S)",
            "%": r"%",
        }

        pattern = format
        for nepali_digit, standard_digit in NEPALI_DIGITS.items():
            pattern = pattern.replace(nepali_digit, standard_digit)
        for directive, regex in directives.items():
            pattern = pattern.replace(f"%{directive}", regex)

        compiled = re.compile(pattern, re.IGNORECASE)
        self._cache[format] = compiled
        return compiled


_cache_lock = _thread_allocate_lock()
_TimeRE_cache = _TimeRE()
_regex_cache = {}


@lru_cache(maxsize=128)
def _find_timezone_for_offset(
    offset_minutes: int, year: int, month: int, day: int
) -> pytz.BaseTzInfo:
    """Finds a pytz timezone that matches a given offset for a reference date.

    This function iterates through all known IANA timezones to find one whose
    UTC offset on the given reference date matches the provided offset. This
    is necessary to handle daylight saving time correctly. If no named timezone
    matches, it returns a `pytz.FixedOffset`.

    Args:
        offset_minutes (int): The UTC offset in minutes (can be positive or negative).
        year (int): The reference year to check the offset against.
        month (int): The reference month.
        day (int): The reference day.

    Returns:
        pytz.BaseTzInfo: A `pytz` timezone object, either a named one
        (e.g., `Asia/Kathmandu`) or a `FixedOffset`.

    Raises:
        ValueError: If the `offset_minutes` value is invalid.
    """
    if abs(offset_minutes) > 1440:
        raise ValueError(f"Timezone offset {offset_minutes} minutes exceeds 24 hours")
    try:
        ref_date = _dt.datetime(year, month, day)
        for tz_name in pytz.all_timezones:
            tz_obj = pytz.timezone(tz_name)
            offset = tz_obj.utcoffset(ref_date)
            if offset is not None and offset.total_seconds() // 60 == offset_minutes:
                return tz_obj
        # Fallback to FixedOffset for non-standard offsets
        return pytz.FixedOffset(offset_minutes)
    except (ValueError, OverflowError) as e:
        raise ValueError(
            f"Cannot create timezone for offset {offset_minutes} minutes"
        ) from e


def _strptime(data_string: str, format: str) -> Tuple[Tuple, int]:
    """The core parsing engine for BS date/time strings.

    This function matches a data string against a format string, extracts all
    date and time components, and returns them in a structured tuple. It handles
    both English and Nepali names and numerals.

    Args:
        data_string (str): The string to parse (e.g., "2081-04-15").
        format (str): The `strftime`-style format to parse with (e.g., "%Y-%m-%d").

    Returns:
        Tuple[Tuple, int]: A 2-item tuple containing:
            - A tuple of parsed date/time components:
              `(year, month, day, hour, minute, second, weekday,
               julian_day, tz_info, tz_name, gmtoff_seconds)`
            - An integer representing the fractional seconds (microseconds).

    Raises:
        ValueError: If `data_string` does not match the `format`.
        TypeError: If arguments are not strings.
    """
    if not isinstance(data_string, str) or not isinstance(format, str):
        raise TypeError("strptime() arguments must be strings")

    # Convert Nepali digits to standard
    for nepali_digit, standard_digit in NEPALI_DIGITS.items():
        data_string = data_string.replace(nepali_digit, standard_digit)

    with _cache_lock:
        if len(_regex_cache) > 5:
            _regex_cache.clear()
        if format not in _regex_cache:
            _regex_cache[format] = _TimeRE_cache.compile(format)
        format_regex = _regex_cache[format]

    found = format_regex.match(data_string)
    if not found or len(data_string) != found.end():
        raise ValueError(f"time data {data_string!r} does not match format {format!r}")

    year = None
    month = day = 1
    hour = minute = second = fraction = 0
    tz = -1
    tzoffset = None
    weekday = julian = None
    week_of_year = -1
    found_dict = found.groupdict()

    for key, value in found_dict.items():
        if key == "y":
            year = int(value)
            if year <= 89:
                year += 2000
            else:
                year += 1900
        elif key == "Y" or key == "K":
            year = int(value)
        elif key == "m" or key == "n":
            month = int(value)
        elif key in ("B", "N"):
            month = (
                MONTH_NAMES_FULL.index(value) + 1
                if value in MONTH_NAMES_FULL
                else MONTH_NAMES_FULL_NEPALI.index(value) + 1
            )
        elif key == "b":
            month = MONTH_NAMES_SHORT.index(value.lower()) + 1
        elif key == "d" or key == "D":
            day = int(value)
        elif key == "H" or key == "h":
            hour = int(value)
        elif key == "I" or key == "i":
            hour = int(value)
            ampm = found_dict.get("p", found_dict.get("P", "")).lower()
            if ampm in ("", AM_PM_ENGLISH[0].lower(), AM_PM_NEPALI[0].lower()):
                if hour == 12:
                    hour = 0
            elif ampm in (AM_PM_ENGLISH[1].lower(), AM_PM_NEPALI[1].lower()):
                if hour != 12:
                    hour += 12
        elif key == "M" or key == "l":
            minute = int(value)
        elif key == "S" or key == "s":
            second = int(value)
        elif key == "f" or key == "t":
            fraction = int(value.ljust(6, "0")[:6])
        elif key in ("A", "a", "G"):
            weekday = (
                WEEKDAY_NAMES_FULL.index(value)
                if value in WEEKDAY_NAMES_FULL
                else WEEKDAY_NAMES_FULL_NEPALI.index(value)
            )
        elif key == "w":
            weekday = int(value)
            if weekday == 0:
                weekday = 6
            else:
                weekday -= 1
        elif key == "j" or key == "J":
            julian = int(value)
        elif key == "U":
            week_of_year = int(value)
        elif key == "z":
            tzoffset = int(value[1:3]) * 60 + int(value[3:5])
            if value[0] == "-":
                tzoffset = -tzoffset
        elif key == "Z":
            import pytz

            try:
                tz = pytz.timezone(value)
            except pytz.exceptions.UnknownTimeZoneError:
                tz = -1
        elif key == "x":
            year, month, day = map(int, value.split("-"))

    if year is None:
        year = BSDate.today().year
    if julian and not (month != 1 or day != 1):
        bs_date = BSDate.bs_fromordinal(julian + BSDate(year, 1, 1).bs_toordinal() - 1)
        year, month, day = bs_date.year, bs_date.month, bs_date.day
    elif week_of_year != -1 and weekday is not None:
        first_weekday = BSDate(year, 1, 1).weekday()
        week_0_length = (7 - first_weekday) % 7
        if week_of_year == 0:
            julian = 1 + weekday - first_weekday
        else:
            days_to_week = week_0_length + (7 * (week_of_year - 1))
            julian = 1 + days_to_week + weekday
        bs_date = BSDate.bs_fromordinal(julian + BSDate(year, 1, 1).bs_toordinal() - 1)
        year, month, day = bs_date.year, bs_date.month, bs_date.day

    if weekday is None:
        weekday = BSDate(year, month, day).weekday()
    gmtoff = tzoffset * 60 if tzoffset is not None else None
    tzname = found_dict.get("Z")
    if tz != -1:
        tzname = tz.zone if hasattr(tz, "zone") else str(tz)
        # Don't override gmtoff if we have a pytz timezone, let it handle DST
        if hasattr(tz, "utcoffset"):
            gmtoff = None  # Let the timezone object handle the offset

    return (
        year,
        month,
        day,
        hour,
        minute,
        second,
        weekday,
        julian or 0,
        tz,
        tzname,
        gmtoff,
    ), fraction


def _strptime_datetime(cls, data_string: str, format: str) -> "BSDatetime":
    """Parses a string into a BSDatetime object.

    This is the internal implementation for `BSDatetime.fromstrftime`.

    Args:
        cls: The `BSDatetime` class to instantiate.
        data_string (str): The string to parse.
        format (str): The format string.

    Returns:
        BSDatetime: A new `BSDatetime` instance.
    """
    tt, fraction = _strptime(data_string, format)
    year, month, day, hour, minute, second, weekday, julian, tz, tzname, gmtoff = tt
    args = [year, month, day, hour, minute, second, fraction]

    # Handle timezone
    if tz != -1 and tz is not None:
        # Use parsed pytz timezone from %Z (e.g., "Asia/Kathmandu")
        args.append(tz)
    elif gmtoff is not None:
        # Map offset to IANA timezone or FixedOffset
        offset_minutes = gmtoff // 60
        tz_obj = _find_timezone_for_offset(offset_minutes, year, month, day)
        args.append(tz_obj)

    return cls(*args)


def _strptime_date(cls, data_string: str, format: str) -> "BSDate":
    """Parses a string into a BSDate object.

    This is the internal implementation for `BSDate.fromstrftime`.

    Args:
        cls: The `BSDate` class to instantiate.
        data_string (str): The string to parse.
        format (str): The format string.

    Returns:
        BSDate: A new `BSDate` instance.
    """
    if format in (FORMAT_B, FORMAT_N, FORMAT_A, FORMAT_G, FORMAT_a):
        raise ValueError(f"Format {format} is ambiguous without year and day")
    tt, _ = _strptime(data_string, format)
    return cls(tt[0], tt[1], tt[2])


def _strptime_time(cls, data_string: str, format: str) -> "BSTime":
    """Parses a string into a BSTime object.

    This is the internal implementation for `BSTime.fromstrftime`.

    Args:
        cls: The `BSTime` class to instantiate.
        data_string (str): The string to parse.
        format (str): The format string.

    Returns:
        BSTime: A new `BSTime` instance.
    """
    tt, fraction = _strptime(data_string, format)
    year, month, day, hour, minute, second, weekday, julian, tz, tzname, gmtoff = tt
    args = [hour, minute, second, fraction]

    # Handle timezone
    if tz != -1 and tz is not None:
        # Use the actual timezone object (e.g., pytz timezone)
        args.append(tz)
    elif gmtoff is not None:
        # Create a simple timezone from offset
        tzdelta = _dt.timedelta(seconds=gmtoff)
        timezone_obj = (
            _dt.timezone(tzdelta, tzname) if tzname else _dt.timezone(tzdelta)
        )
        args.append(timezone_obj)

    return cls(*args)
