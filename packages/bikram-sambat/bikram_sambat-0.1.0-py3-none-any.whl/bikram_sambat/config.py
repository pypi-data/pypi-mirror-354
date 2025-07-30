"""Defines the core configuration parameters for the bikram_sambat package.

These constants control the operational boundaries of the library, such as the
supported year range, and provide the reference anchor dates required for
conversions between the Bikram Sambat (BS) and Gregorian (AD) calendars.

Attributes:
    BS_EPOCH_START_YEAR (int): The first year of the Bikram Sambat calendar
        for which the library has data, often used as the base for ordinal
        calculations.
    BS_MIN_SUPPORTED_YEAR (int): The earliest Bikram Sambat year officially
        supported. Operations on dates before this year will raise a
        `DateOutOfRangeError`.
    BS_MAX_SUPPORTED_YEAR (int): The latest Bikram Sambat year officially
        supported. Operations on dates after this year will raise a
        `DateOutOfRangeError`.
    BS_REFERENCE_DATE_AD (_dt.date): The Gregorian (AD) date that serves as a
        fixed anchor point for all conversion calculations. This date is the
        known equivalent of `BS_REFERENCE_DATE_BS_TUPLE`.
    BS_REFERENCE_DATE_BS_TUPLE (tuple[int, int, int]): The Bikram Sambat (BS)
        date, as a (year, month, day) tuple, that corresponds to the
        `BS_REFERENCE_DATE_AD`. This pair of reference dates is fundamental
        to the conversion algorithm.
"""

import datetime as _dt

BS_EPOCH_START_YEAR = 1901
"""int: The start year of the BS epoch used in this library."""

BS_MIN_SUPPORTED_YEAR = 1901
"""int: The minimum supported BS year (inclusive)."""

BS_MAX_SUPPORTED_YEAR = 2199
"""int: The maximum supported BS year (inclusive)."""

# This pair of reference dates defines the anchor for all conversions.
# The algorithm calculates the number of days between a given date and its
# respective reference date to bridge the two calendar systems.
# Specifically, 1901-01-01 BS is equivalent to 1844-04-11 AD.

BS_REFERENCE_DATE_AD = _dt.date(1844, 4, 11)
"""_dt.date: The Gregorian (AD) component of the reference anchor date."""

BS_REFERENCE_DATE_BS_TUPLE = (1901, 1, 1)
"""tuple[int, int, int]: The Bikram Sambat (BS) component of the reference anchor date."""