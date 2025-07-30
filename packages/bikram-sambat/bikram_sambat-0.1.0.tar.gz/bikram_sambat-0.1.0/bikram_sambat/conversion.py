"""Provides the core date conversion logic between Gregorian (AD) and Bikram Sambat (BS).

This module is the computational engine of the library. It uses an anchor-based
approach, calculating the number of days between a given date and a known
reference point (see `config.py`) to convert between the two calendar systems.
The conversions are performed using ordinal dates, which represent a date as a
single integer count of days.

The module pre-computes and caches data structures at load time to ensure
high-performance lookups and conversions. The functions prefixed with an
underscore `_` are internal helpers, while the others form the primary
conversion API used by other modules in the package.
"""

import datetime as _dt
import bisect

from .data.calendar_data import (
    YEAR_MONTH_DAYS_BS,
    CUMULATIVE_DAYS_BS,
    BS_DAYS_IN_YEAR,
    BS_YEAR_START_ORDINAL,
)
from . import config
from .exceptions import DateOutOfRangeError, InvalidDateError, InvalidTypeError

# --- Module-level Pre-computation for Performance ---
# The following code block pre-processes the raw calendar data to create
# sorted lists and lookup tables. This allows for the use of efficient
# binary search algorithms (via `bisect`), making ordinal-to-date conversions
# significantly faster than linear scans.
_sorted_bs_years = []
_sorted_bs_year_start_ordinals = []

# Populate sorted lists. Iterating over sorted keys of BS_YEAR_START_ORDINAL
# ensures that _sorted_bs_years and _sorted_bs_year_start_ordinals are co-sorted.
for year_key in sorted(BS_YEAR_START_ORDINAL.keys()):
    _sorted_bs_years.append(year_key)
    _sorted_bs_year_start_ordinals.append(BS_YEAR_START_ORDINAL[year_key])

# Determine the minimum and maximum supported BS ordinals based on available data.
_MIN_BS_ORDINAL_SUPPORTED = _sorted_bs_year_start_ordinals[0]
_last_supported_bs_year_in_data = _sorted_bs_years[-1]
_MAX_BS_ORDINAL_SUPPORTED = (
    _sorted_bs_year_start_ordinals[-1]
    + BS_DAYS_IN_YEAR[_last_supported_bs_year_in_data]
    - 1
)

# Calculate reference ordinals once at module load.
_REF_GREGORIAN_ORDINAL = config.BS_REFERENCE_DATE_AD.toordinal()

# _bs_ymd_to_ordinal_for_ref is a temporary helper to avoid calling the full _bs_ymd_to_ordinal
# before it's defined, and also to make it clear this is for the reference setup.
# It assumes valid reference BS date parts from config.
_ref_bs_year, _ref_bs_month, _ref_bs_day = config.BS_REFERENCE_DATE_BS_TUPLE
_REF_BS_ORDINAL = (
    BS_YEAR_START_ORDINAL[_ref_bs_year]
    - 1
    + CUMULATIVE_DAYS_BS[_ref_bs_year][_ref_bs_month - 1]
    + _ref_bs_day
)


# --- Internal Helper Functions ---


def _validate_bs_date(year: int, month: int, day: int) -> None:
    """Validates if a BS year, month, and day form a real, existing date.

    Checks the date against the supported year range and the specific number
    of days in the given month of that year.

    Args:
        year (int): The Bikram Sambat year.
        month (int): The Bikram Sambat month (1-12).
        day (int): The Bikram Sambat day.

    Raises:
        DateOutOfRangeError: If the year is outside the configured supported range.
        InvalidDateError: If the month is invalid or the day does not exist
            for the given month and year.
    """
    if not (config.BS_MIN_SUPPORTED_YEAR <= year <= config.BS_MAX_SUPPORTED_YEAR):
        raise DateOutOfRangeError(
            f"BS year {year} is out of the supported range "
            f"({config.BS_MIN_SUPPORTED_YEAR}–{config.BS_MAX_SUPPORTED_YEAR})."
        )
    if year not in YEAR_MONTH_DAYS_BS:
        # This should ideally be caught by the above check if config and data are aligned.
        raise InvalidDateError(f"Calendar data for BS year {year} is not available.")

    if not (1 <= month <= 12):
        raise InvalidDateError(f"BS month {month} must be between 1 and 12.")

    try:
        days_in_month = YEAR_MONTH_DAYS_BS[year][month - 1]
    except IndexError:
        # Should not happen if month is 1-12 and YEAR_MONTH_DAYS_BS[year] is a list of 12.
        raise InvalidDateError(
            f"Internal error accessing month data for BS {year}-{month:02d}."
        )

    if not (1 <= day <= days_in_month):
        raise InvalidDateError(
            f"BS day {day} is out of range for BS {year}-{month:02d}. "
            f"Valid days: 1–{days_in_month}."
        )


def _bs_ymd_to_ordinal(year: int, month: int, day: int) -> int:
    """Converts a Bikram Sambat (BS) date to its corresponding BS ordinal.

    A BS ordinal is the number of days elapsed since the beginning of the
    BS calendar epoch defined in the calendar data.

    Note:
        This is a low-level function that assumes the input date has already
        been validated.

    Args:
        year (int): The BS year.
        month (int): The BS month (1-12).
        day (int): The BS day.

    Returns:
        int: The BS ordinal for the given date.
    """
    # BS_YEAR_START_ORDINAL[year] is the ordinal of the first day of 'year'.
    # (BS_YEAR_START_ORDINAL[year] - 1) is the count of days *before* 'year' starts.
    days_before_year_start = BS_YEAR_START_ORDINAL[year] - 1
    days_before_month_start_in_year = CUMULATIVE_DAYS_BS[year][month - 1]
    return days_before_year_start + days_before_month_start_in_year + day


def _bs_ordinal_to_ymd(bs_ordinal: int) -> tuple[int, int, int]:
    """Converts a BS ordinal number back to a BS (year, month, day) tuple.

    This function uses an efficient binary search (`bisect`) on pre-computed
    data to quickly locate the year and month corresponding to the ordinal.

    Args:
        bs_ordinal (int): The BS ordinal to convert.

    Returns:
        tuple[int, int, int]: A tuple containing the (year, month, day).

    Raises:
        DateOutOfRangeError: If the provided `bs_ordinal` is outside the
            range of the available calendar data.
    """
    if not (_MIN_BS_ORDINAL_SUPPORTED <= bs_ordinal <= _MAX_BS_ORDINAL_SUPPORTED):
        min_year_in_data = _sorted_bs_years[0]
        if bs_ordinal < _MIN_BS_ORDINAL_SUPPORTED:
            raise DateOutOfRangeError(
                f"BS ordinal {bs_ordinal} is too small. Minimum supported ordinal is "
                f"{_MIN_BS_ORDINAL_SUPPORTED} (for BS year {min_year_in_data})."
            )
        else:  # bs_ordinal > _MAX_BS_ORDINAL_SUPPORTED
            raise DateOutOfRangeError(
                f"BS ordinal {bs_ordinal} is too large. Maximum supported ordinal is "
                f"{_MAX_BS_ORDINAL_SUPPORTED} (for BS year {_last_supported_bs_year_in_data})."
            )

    # Find the year using binary search on pre-sorted start ordinals.
    # bisect_right returns an insertion point; the year is at index - 1.
    year_idx = bisect.bisect_right(_sorted_bs_year_start_ordinals, bs_ordinal)
    year = _sorted_bs_years[year_idx - 1]

    day_of_year = bs_ordinal - BS_YEAR_START_ORDINAL[year] + 1

    # Find the month using binary search on pre-calculated cumulative days for the year.
    month_days_cumulative_for_year = CUMULATIVE_DAYS_BS[year]
    # day_of_year is 1-based; cumulative days are 0-based sums *before* month start.
    month_idx = bisect.bisect_right(month_days_cumulative_for_year, day_of_year - 1)
    month = month_idx  # Result of bisect_right is 1-based month index.

    day = day_of_year - month_days_cumulative_for_year[month - 1]

    return year, month, day


# --- Public Conversion API ---


def ad_to_bs(greg_date: _dt.date) -> tuple[int, int, int]:
    """Converts a Gregorian (AD) date to a Bikram Sambat (BS) date.

    Args:
        greg_date (_dt.date): The Gregorian `datetime.date` object to convert.

    Returns:
        tuple[int, int, int]: The equivalent BS date as a (year, month, day) tuple.

    Raises:
        InvalidTypeError: If `greg_date` is not a `datetime.date` object.
        DateOutOfRangeError: If the given Gregorian date converts to a BS
            date that is outside the library's supported range.
    """
    if not isinstance(greg_date, _dt.date):
        raise InvalidTypeError("Input 'greg_date' must be a datetime.date object.")

    try:
        target_gregorian_ordinal = greg_date.toordinal()
        # print(f"target_gregorian_ordinal, {target_gregorian_ordinal}")
    except (
        ValueError
    ) as e:  # Handles dates outside Gregorian's own supported range (e.g. year 0)
        raise DateOutOfRangeError(f"Input Gregorian date {greg_date} is invalid: {e}")

    day_difference = target_gregorian_ordinal - _REF_GREGORIAN_ORDINAL
    # print(f"day_difference, {day_difference}")

    target_bs_ordinal = _REF_BS_ORDINAL + day_difference
    # print(f"target_bs_ordinal, {target_bs_ordinal}")

    try:
        bs_year, bs_month, bs_day = _bs_ordinal_to_ymd(target_bs_ordinal)
        # print(f"bs_year, {bs_year}, bs_month, {bs_month}, bs_day({bs_day})")
    except DateOutOfRangeError as e:
        # Provide context for the conversion failure.
        raise DateOutOfRangeError(
            f"Gregorian date {greg_date} converts to a BS ordinal ({target_bs_ordinal}) "
            f"that is outside the supported BS date range. Original error: {e}"
        )

    # Final check to ensure the resulting BS year is within user-configured limits,
    # although _bs_ordinal_to_ymd should already handle data boundaries.
    if not (config.BS_MIN_SUPPORTED_YEAR <= bs_year <= config.BS_MAX_SUPPORTED_YEAR):
        raise DateOutOfRangeError(
            f"Converted BS date {bs_year}-{bs_month:02d}-{bs_day:02d} "
            f"is outside the configured supported range of "
            f"{config.BS_MIN_SUPPORTED_YEAR}–{config.BS_MAX_SUPPORTED_YEAR}."
        )
    return bs_year, bs_month, bs_day


def bs_to_ad(bs_year: int, bs_month: int, bs_day: int) -> _dt.date:
    """Converts a Bikram Sambat (BS) date to a Gregorian (AD) date.

    Args:
        bs_year (int): The BS year.
        bs_month (int): The BS month (1-12).
        bs_day (int): The BS day.

    Returns:
        _dt.date: The equivalent Gregorian `datetime.date` object.

    Raises:
        InvalidTypeError: If year, month, or day are not integers.
        InvalidDateError: If the provided BS date is not a valid, existing date.
        DateOutOfRangeError: If the year is outside the supported range or if
            the conversion results in a Gregorian date that is out of its
            own valid range.
    """
    if not all(isinstance(x, int) for x in (bs_year, bs_month, bs_day)):
        raise InvalidTypeError("BS year, month, and day must be integers.")

    _validate_bs_date(bs_year, bs_month, bs_day)

    target_bs_ordinal = _bs_ymd_to_ordinal(bs_year, bs_month, bs_day)
    day_difference = target_bs_ordinal - _REF_BS_ORDINAL
    target_gregorian_ordinal = _REF_GREGORIAN_ORDINAL + day_difference

    try:
        return _dt.date.fromordinal(target_gregorian_ordinal)
    except ValueError as e:  # Gregorian ordinal out of its own valid range.
        raise DateOutOfRangeError(
            f"BS date {bs_year}-{bs_month:02d}-{bs_day:02d} (ordinal {target_bs_ordinal}) "
            f"results in an invalid Gregorian ordinal ({target_gregorian_ordinal}). "
            f"Original error: {e}"
        )


def ad_datetime_to_bs(
    greg_dt: _dt.datetime,
) -> tuple[int, int, int, int, int, int, int, _dt.tzinfo | None]:
    """Converts a Gregorian (AD) datetime object to a BS datetime tuple.

    The time components (hour, minute, etc.) and timezone are preserved.

    Args:
        greg_dt (_dt.datetime): The Gregorian `datetime.datetime` object to convert.

    Returns:
        tuple[int, int, int, int, int, int, int, _dt.tzinfo | None]: A tuple
        containing the BS (year, month, day, hour, minute, second,
        microsecond, tzinfo).

    Raises:
        InvalidTypeError: If `greg_dt` is not a `datetime.datetime` object.
    """
    if not isinstance(greg_dt, _dt.datetime):
        raise InvalidTypeError("Input 'greg_dt' must be a datetime.datetime object.")

    # Convert the date part
    bs_year, bs_month, bs_day = ad_to_bs(greg_dt.date())

    return (
        bs_year,
        bs_month,
        bs_day,
        greg_dt.hour,
        greg_dt.minute,
        greg_dt.second,
        greg_dt.microsecond,
        greg_dt.tzinfo,
    )


def bs_datetime_to_ad(
    bs_year: int,
    bs_month: int,
    bs_day: int,
    hour: int = 0,
    minute: int = 0,
    second: int = 0,
    microsecond: int = 0,
    tzinfo: _dt.tzinfo | None = None,
) -> _dt.datetime:
    """Converts BS datetime components to a Gregorian (AD) datetime object.

    Args:
        bs_year (int): The BS year.
        bs_month (int): The BS month (1-12).
        bs_day (int): The BS day.
        hour (int): The hour (0-23). Defaults to 0.
        minute (int): The minute (0-59). Defaults to 0.
        second (int): The second (0-59). Defaults to 0.
        microsecond (int): The microsecond (0-999999). Defaults to 0.
        tzinfo (_dt.tzinfo | None): The timezone info object. Defaults to None.

    Returns:
        _dt.datetime: The equivalent Gregorian `datetime.datetime` object.

    Raises:
        InvalidTypeError: If any arguments have an incorrect type.
        InvalidDateError: If the provided BS date or time components are not valid.
        DateOutOfRangeError: If the BS year is outside the supported range.
    """
    if not all(isinstance(x, int) for x in (hour, minute, second, microsecond)):
        raise InvalidTypeError(
            "Time components (hour, minute, second, microsecond) must be integers."
        )
    if tzinfo is not None and not isinstance(tzinfo, _dt.tzinfo):
        raise InvalidTypeError("tzinfo must be a datetime.tzinfo object or None.")

    # Convert the date part; this also validates the BS date components.
    greg_date_part = bs_to_ad(bs_year, bs_month, bs_day)

    try:
        return _dt.datetime(
            greg_date_part.year,
            greg_date_part.month,
            greg_date_part.day,
            hour,
            minute,
            second,
            microsecond,
            tzinfo,
        )
    except ValueError as e:  # Handles invalid time components like hour=25
        raise InvalidDateError(f"Invalid time component provided. Original error: {e}")
