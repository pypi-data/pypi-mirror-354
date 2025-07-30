"""Defines the BSDate class for representing dates in the Bikram Sambat calendar.

This module provides the `BSDate` object, a subclass of the standard `datetime.date`.
It is designed to be a drop-in replacement, allowing for intuitive date
manipulation, formatting, and arithmetic, all within the context of the
Bikram Sambat calendar system.
"""

import re
from typing import SupportsIndex, cast

import datetime as _dt
from .bs_timedelta import BSTimedelta
from .exceptions import InvalidDateError, InvalidTypeError, DateOutOfRangeError
from .conversion import ad_to_bs, bs_to_ad, _bs_ymd_to_ordinal, _bs_ordinal_to_ymd
from . import config
from .data.calendar_data import YEAR_MONTH_DAYS_BS

from .constants import (
    NEPALI_DIGITS,
    STANDARD_DIGITS,
    MONTH_NAMES_FULL,
    MONTH_NAMES_SHORT,
    MONTH_NAMES_FULL_NEPALI,
    WEEKDAY_NAMES_FULL,
    WEEKDAY_NAMES_SHORT,
    WEEKDAY_NAMES_FULL_NEPALI,
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
    FORMAT_K,
    FORMAT_Y,
    FORMAT_k,
    FORMAT_j,
    FORMAT_J,
    FORMAT_U,
    FORMAT_c,
    FORMAT_x,
    MONTH_NAMES_FULL,
    MONTH_NAMES_SHORT,
    WEEKDAY_NAMES_FULL,
    WEEKDAY_NAMES_SHORT,
    DATE_FORMAT_DIRECTIVES,
)


class BSDate(_dt.date):
    """An immutable date object representing a date in the Bikram Sambat (BS) calendar.

    `BSDate` is a subclass of `datetime.date` and supports all of its methods.
    However, key attributes and methods are overridden to reflect the BS calendar:

    - Attributes like `.year`, `.month`, and `.day` return the BS date components.
    - Methods like `weekday()` and `strftime()` operate according to the BS calendar.
    - Arithmetic operations (`+`, `-`) work correctly for BS dates.

    It provides a seamless way to work with Nepali dates while maintaining
    compatibility with the standard Python `datetime` ecosystem.

    Args:
        year (int): The Bikram Sambat year.
        month (int): The Bikram Sambat month (1-12).
        day (int): The Bikram Sambat day.

    Attributes:
        year (int): The BS year.
        month (int): The BS month.
        day (int): The BS day.

    Raises:
        InvalidTypeError: If year, month, or day are not integers.
        DateOutOfRangeError: If the year is outside the supported range (1901-2199).
        InvalidDateError: If the month is invalid or the day does not exist for
            the given month and year.

    Example:
        >>> from bikram_sambat import date, timedelta
        >>> import datetime

        >>> # Create a BSDate instance
        >>> bs_date = date(2081, 4, 15)
        >>> print(bs_date)
        2081-04-15

        >>> # Access properties
        >>> print(f"Year: {bs_date.year}, Month: {bs_date.month}")
        Year: 2081, Month: 4

        >>> # Perform date arithmetic
        >>> new_bs_date = bs_date + timedelta(days=10)
        >>> print(new_bs_date)
        2081-04-25

        >>> # Calculate the difference between two dates
        >>> diff = date(2082, 1, 1) - date(2081, 1, 1)
        >>> print(f"Days in year 2081: {diff.days}")
        Days in year 2081: 366

        >>> # Convert to a standard Gregorian date
        >>> greg_date = bs_date.togregorian()
        >>> print(greg_date)
        2024-07-30
    """

    _bs_year: int
    _bs_month: int
    _bs_day: int

    def __new__(cls, year: int, month: int, day: int):
        if not all(isinstance(x, int) for x in (year, month, day)):
            raise InvalidTypeError("year, month, day must be integers")
        if not (config.BS_MIN_SUPPORTED_YEAR <= year <= config.BS_MAX_SUPPORTED_YEAR):
            raise DateOutOfRangeError(
                f"BS year {year} outside {config.BS_MIN_SUPPORTED_YEAR}–{config.BS_MAX_SUPPORTED_YEAR}"
            )
        if year not in YEAR_MONTH_DAYS_BS:
            raise InvalidDateError(f"Calendar data for BS year {year} unavailable")
        if not (1 <= month <= 12):
            raise InvalidDateError(f"BS month {month} must be 1–12")
        days_in_bs_month = YEAR_MONTH_DAYS_BS[year][month - 1]
        if not (1 <= day <= days_in_bs_month):
            raise InvalidDateError(
                f"BS day {day} out of range for {year}-{month:02d} (1–{days_in_bs_month})"
            )
        try:
            greg_date = bs_to_ad(year, month, day)
        except (DateOutOfRangeError, InvalidDateError) as e:
            raise InvalidDateError(f"Invalid BS date {year}-{month:02d}-{day:02d}: {e}")
        instance = super().__new__(cls, greg_date.year, greg_date.month, greg_date.day)
        instance._bs_year = year
        instance._bs_month = month
        instance._bs_day = day
        return instance

    @property
    def year(self) -> int:
        """Returns the BS year as an integer."""
        return self._bs_year

    @property
    def month(self) -> int:
        """Returns the BS month as an integer (1-12)."""
        return self._bs_month

    @property
    def day(self) -> int:
        """Returns the BS day as an integer."""
        return self._bs_day

    def isoformat(self) -> str:
        """Returns the date in ISO 8601 format, 'YYYY-MM-DD'."""
        return f"{self._bs_year:04d}-{self._bs_month:02d}-{self._bs_day:02d}"

    def __repr__(self) -> str:
        """Returns the official, unambiguous string representation of the BSDate."""
        return f"{self.__class__.__module__}.{self.__class__.__name__}({self._bs_year}, {self._bs_month}, {self._bs_day})"

    def __str__(self) -> str:
        """Returns the date in ISO 8601 format, 'YYYY-MM-DD'."""
        return self.isoformat()

    @classmethod
    def today(cls) -> "BSDate":
        """Returns the current local BSDate.

        Example:
            >>> today_bs = BSDate.today()
            >>> print(f"Today's BS date is {today_bs}")
        """
        greg_today = _dt.date.today()
        bs_y, bs_m, bs_d = ad_to_bs(greg_today)
        return cls(bs_y, bs_m, bs_d)

    @classmethod
    def fromisoformat(cls, date_string: str) -> "BSDate":
        """Creates a BSDate from an ISO 8601 formatted string ('YYYY-MM-DD').

        Example:
            >>> date.fromisoformat('2081-04-15')
            bikram_sambat.date.BSDate(2081, 4, 15)
        """
        if not isinstance(date_string, str):
            raise InvalidTypeError("fromisoformat: argument must be str")
        try:
            year, month, day = map(int, date_string.split("-"))
            return cls(year, month, day)
        except ValueError:
            raise ValueError(f"Invalid ISO format string: '{date_string}'")

    @classmethod
    def fromgregorian(cls, greg_date_input: _dt.date) -> "BSDate":
        """Creates a BSDate from a standard `datetime.date` (Gregorian) object.

        This is the primary way to convert from a Gregorian date to a BS date.

        Args:
            greg_date_input (_dt.date): The Gregorian date to convert.

        Returns:
            BSDate: The equivalent `BSDate` object.

        Example:
            >>> import datetime
            >>> greg_date = datetime.date(2024, 7, 15)
            >>> bs_date = date.fromgregorian(greg_date)
            >>> print(bs_date)
            2081-03-31
        """
        if isinstance(greg_date_input, cls):
            return greg_date_input
        if not isinstance(greg_date_input, _dt.date):
            raise InvalidTypeError(
                f"Input must be datetime.date, got {type(greg_date_input).__name__}"
            )
        bs_y, bs_m, bs_d = ad_to_bs(greg_date_input)
        return cls(bs_y, bs_m, bs_d)

    def togregorian(self) -> _dt.date:
        """Converts the BSDate object to a standard `datetime.date` (Gregorian) object.

        This is the primary way to convert from a BS date to a Gregorian date.

        Returns:
            _dt.date: The equivalent Gregorian date object.

        Example:
            >>> bs_date = date(2081, 3, 31)
            >>> greg_date = bs_date.togregorian()
            >>> print(greg_date)
            2024-07-15
        """
        return _dt.date(super().year, super().month, super().day)

    def __add__(self, other):
        """Adds a timedelta to the date, returning a new BSDate."""
        if not isinstance(other, (_dt.timedelta, BSTimedelta)):
            return NotImplemented
        o = self.bs_toordinal() + other.days
        return self.bs_fromordinal(o)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        """Subtracts a timedelta or another BSDate.

        If `other` is a `timedelta`, returns a new `BSDate`.
        If `other` is a `BSDate`, returns a `BSTimedelta`.
        """
        if isinstance(other, (_dt.timedelta, BSTimedelta)):
            return self.__add__(-other)
        if isinstance(other, type(self)):
            return BSTimedelta(days=self.bs_toordinal() - other.bs_toordinal())
        return NotImplemented

    def __reduce__(self):
        return (self.__class__, (self._bs_year, self._bs_month, self._bs_day))

    def replace(
        self,
        year: SupportsIndex = -1,
        month: SupportsIndex = -1,
        day: SupportsIndex = -1,
    ) -> "BSDate":
        """Returns a new BSDate with one or more components replaced.

        Example:
            >>> d = date(2081, 4, 15)
            >>> d.replace(day=1)
            bikram_sambat.date.BSDate(2081, 4, 1)
        """
        new_year = self._bs_year if year == -1 else year
        new_month = self._bs_month if month == -1 else month
        new_day = self._bs_day if day == -1 else day
        if not all(isinstance(x, int) for x in (new_year, new_month, new_day)):
            raise InvalidTypeError("year, month, day must be integers")

        new_year = cast(int, new_year)
        new_month = cast(int, new_month)
        new_day = cast(int, new_day)

        return self.__class__(new_year, new_month, new_day)

    def weekday(self) -> int:
        """Returns the day of the week as an integer (Sunday=0, Saturday=6)."""
        greg_weekday = super().weekday()  # Monday=0, Sunday=6
        return (greg_weekday + 1) % 7  # Aaitabar(Sunday)=0, Sanicharbar=6

    def isoweekday(self) -> int:
        """Returns the day of the week as an integer (Sunday=1, Saturday=7)."""
        return self.weekday() + 1  # Aaitabar=1, Sanicharbar=7

    def ctime(self) -> str:
        return f"{WEEKDAY_NAMES_SHORT[self.weekday()]} {MONTH_NAMES_SHORT[self.month-1]} {self.day:2d} 00:00:00 {self.year}"

    def bs_toordinal(self) -> int:
        return _bs_ymd_to_ordinal(self._bs_year, self._bs_month, self._bs_day)

    @classmethod
    def bs_fromordinal(cls, ordinal: int) -> "BSDate":
        if not isinstance(ordinal, int):
            raise InvalidTypeError("Ordinal must be an integer")
        bs_y, bs_m, bs_d = _bs_ordinal_to_ymd(ordinal)
        return cls(bs_y, bs_m, bs_d)

    def strftime(self, format: str) -> str:
        """Formats the date according to a format string with BS-specific directives.

        This method supports all standard `strftime` directives for dates, plus
        custom directives for Nepali numerals and names.

        Args:
            format (str): The `strftime`-style format string.

        Returns:
            str: The formatted date string.

        Raises:
            ValueError: If the format string contains an unsupported directive.

        Example:
            >>> d = date(2081, 4, 15)
            >>> # English formatting
            >>> d.strftime("%A, %B %d, %Y")
            'Tuesday, Shrawan 15, 2081'
            >>> # Nepali formatting
            >>> d.strftime("%G, %N %D, %K")
            'मंगलवार, श्रावण १५, २०८१'
        """
        if not isinstance(format, str):
            raise InvalidTypeError("format must be a string")

        # Handle %% as literal %
        temp_fmt = format.replace("%%", "__PERCENT__")

        # Extract all % directives (valid and invalid)
        directives = re.findall(r"%[A-Za-z]|%%", temp_fmt)
        # Validate each directive
        for directive in directives:
            if directive not in DATE_FORMAT_DIRECTIVES:
                raise ValueError(
                    f"Format directive '{directive}' not supported in BSDate.strftime"
                )
        bs_weekday_val = self.weekday()
        # Calculate day of year
        year_start = BSDate(self.year, 1, 1)
        day_of_year = self.bs_toordinal() - year_start.bs_toordinal() + 1
        # Calculate week number (Sunday-based)
        week_number = (
            self.bs_toordinal() - year_start.bs_toordinal() + year_start.weekday()
        ) // 7 + 1
        format_map = {
            FORMAT_Y: f"{self.year:04d}",
            FORMAT_K: "".join(STANDARD_DIGITS[c] for c in f"{self.year:04d}"),
            FORMAT_y: f"{self.year % 100:02d}",
            FORMAT_k: "".join(STANDARD_DIGITS[c] for c in f"{self.year % 100:02d}"),
            FORMAT_m: f"{self.month:02d}",
            FORMAT_n: "".join(STANDARD_DIGITS[c] for c in f"{self.month:02d}"),
            FORMAT_d: f"{self.day:02d}",
            FORMAT_D: "".join(STANDARD_DIGITS[c] for c in f"{self.day:02d}"),
            FORMAT_B: MONTH_NAMES_FULL[self.month - 1],
            FORMAT_N: MONTH_NAMES_FULL_NEPALI[self.month - 1],
            FORMAT_b: MONTH_NAMES_SHORT[self.month - 1],
            FORMAT_A: WEEKDAY_NAMES_FULL[bs_weekday_val],
            FORMAT_G: WEEKDAY_NAMES_FULL_NEPALI[bs_weekday_val],
            FORMAT_a: WEEKDAY_NAMES_SHORT[bs_weekday_val],
            FORMAT_w: str(bs_weekday_val),
            FORMAT_j: str(day_of_year).zfill(3),
            FORMAT_J: "".join(STANDARD_DIGITS[c] for c in str(day_of_year).zfill(3)),
            FORMAT_U: str(week_number).zfill(2),
            FORMAT_c: f"{WEEKDAY_NAMES_SHORT[bs_weekday_val]} {MONTH_NAMES_SHORT[self.month-1]} {self.day:02d} 00:00:00 {self.year}",
            FORMAT_x: f"{self.year:04d}-{self.month:02d}-{self.day:02d}",
            "%%": "%",
        }
        output = temp_fmt
        for directive, value in format_map.items():
            output = output.replace(directive, value)

        output = output.replace("__PERCENT__", "%")
        return output

    @classmethod
    def fromstrftime(cls, date_string: str, format: str) -> "BSDate":
        """Parses a string into a BSDate object according to a format.

        This is the reverse of `strftime`. It can parse strings containing
        both English and Nepali names and numerals.

        Args:
            date_string (str): The string to parse.
            format (str): The format that the `date_string` follows.

        Returns:
            BSDate: A new `BSDate` instance.

        Example:
            >>> date_str = "मंगलवार, श्रावण १५, २०८१"
            >>> format_str = "%G, %N %D, %K"
            >>> date.fromstrftime(date_str, format_str)
            bikram_sambat.date.BSDate(2081, 4, 15)
        """
        from .strptime import _strptime_date

        return _strptime_date(cls, date_string, format)
