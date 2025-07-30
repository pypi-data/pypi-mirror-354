"""Defines the BSDatetime class for timezone-aware date and time objects.

This module provides the `BSDatetime` object, a subclass of `datetime.datetime`,
which seamlessly integrates `BSDate` and `BSTime` functionality. It is designed
to be a full-featured, timezone-aware datetime object for the Bikram Sambat
calendar system.
"""

import re


import datetime as _dt
from typing import Optional, Union
import pytz

from .bs_date import BSDate
from .bs_timedelta import BSTimedelta
from .exceptions import InvalidTypeError
from .conversion import ad_to_bs, bs_to_ad
from .constants import (
    STANDARD_DIGITS,
    MONTH_NAMES_FULL,
    MONTH_NAMES_SHORT,
    MONTH_NAMES_FULL_NEPALI,
    WEEKDAY_NAMES_FULL,
    WEEKDAY_NAMES_SHORT,
    WEEKDAY_NAMES_FULL_NEPALI,
    AM_PM_ENGLISH,
    AM_PM_NEPALI,
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
    DATETIME_FORMAT_DIRECTIVES,
)


class BSDatetime(_dt.datetime):
    """A timezone-aware Bikram Sambat (BS) datetime object.

    `BSDatetime` is a subclass of the standard `datetime.datetime` and is designed
    to be a full replacement for it when working with BS dates. It combines the
    features of `BSDate` and `BSTime`, providing a complete object that handles
    both date and time components in the BS calendar.

    Key features include:
    - Date components (`.year`, `.month`, `.day`) are in Bikram Sambat.
    - Full support for timezone-aware operations, including `pytz` localization.
    - BS-specific formatting and parsing via `strftime()` and `fromstrftime()`.
    - Correct arithmetic with `timedelta` objects.
    - Compatibility with frameworks like Django that expect a `datetime` object.

    Args:
        year (int): The Bikram Sambat year.
        month (int): The Bikram Sambat month (1-12).
        day (int): The Bikram Sambat day.
        hour (int): The hour (0-23). Defaults to 0.
        minute (int): The minute (0-59). Defaults to 0.
        second (int): The second (0-59). Defaults to 0.
        microsecond (int): The microsecond (0-999999). Defaults to 0.
        tzinfo (_dt.tzinfo, optional): A `pytz` or `datetime.tzinfo` object.
            Defaults to None (creating a naive datetime).
        fold (int): Used to disambiguate wall times during a repeated hour
            (e.g., during a DST transition). 0 or 1. Defaults to 0.

    Raises:
        InvalidTypeError: If arguments have an incorrect type.
        DateOutOfRangeError: If the BS date is outside the supported calendar range.
        InvalidDateError: If the BS date is invalid (e.g., day 32).

    Example:
        >>> from bikram_sambat import datetime, tz, timedelta
        >>> import pytz

        >>> # Create a naive BS datetime
        >>> dt_naive = datetime(2081, 4, 15, 10, 30, 0)
        >>> print(dt_naive)
        2081-04-15T10:30:00

        >>> # Create a timezone-aware BS datetime in Nepal
        >>> dt_aware = datetime(2081, 4, 15, 10, 30, 0, tzinfo=tz.nepal)
        >>> print(dt_aware)
        2081-04-15T10:30:00+05:45

        >>> # Convert to a different timezone
        >>> us_eastern = pytz.timezone('America/New_York')
        >>> dt_us = dt_aware.astimezone(us_eastern)
        >>> print(dt_us.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
        2081-04-15 00:45:00 EDT-0400
    """


    _bs_year: int
    _bs_date_part: BSDate
    _bs_month: int
    _bs_day: int

    def __new__(
        cls,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
        tzinfo: Optional[_dt.tzinfo] = None,
        *,
        fold: int = 0,
    ):
        bs_date_obj = BSDate(year, month, day)
        greg_date_equiv = bs_date_obj.togregorian()
        if tzinfo is not None and not isinstance(tzinfo, (pytz.BaseTzInfo, _dt.tzinfo)):
            raise InvalidTypeError("tzinfo must be a pytz or datetime.tzinfo object")
        # Localize pytz timezone if provided
        if tzinfo is not None and isinstance(tzinfo, pytz.BaseTzInfo):
            temp_dt = _dt.datetime(
                greg_date_equiv.year,
                greg_date_equiv.month,
                greg_date_equiv.day,
                hour,
                minute,
                second,
                microsecond,
            )
            try:
                localized_dt = tzinfo.localize(temp_dt, is_dst=None)
            except pytz.exceptions.AmbiguousTimeError:
                localized_dt = tzinfo.localize(temp_dt, is_dst=(fold == 0))
            except pytz.exceptions.NonExistentTimeError:
                localized_dt = tzinfo.localize(temp_dt, is_dst=(fold == 0))
            tzinfo = localized_dt.tzinfo
        instance = super().__new__(
            cls,
            greg_date_equiv.year,
            greg_date_equiv.month,
            greg_date_equiv.day,
            hour,
            minute,
            second,
            microsecond,
            tzinfo,
            fold=fold,
        )
        instance._bs_date_part = bs_date_obj
        instance._bs_year = year
        instance._bs_month = month
        instance._bs_day = day
        return instance

    @property
    def year(self) -> int:
        return self._bs_year

    @property
    def month(self) -> int:
        return self._bs_month

    @property
    def day(self) -> int:
        return self._bs_day

    def date(self) -> BSDate:
        """Returns a `BSDate` object representing the date part of the datetime.

        Example:
            >>> dt = datetime(2081, 4, 15, 10, 30)
            >>> dt.date()
            bikram_sambat.date.BSDate(2081, 4, 15)
        """
        return BSDate(
            self._bs_date_part.year, self._bs_date_part.month, self._bs_date_part.day
        )

    def __repr__(self) -> str:
        time_str = ""
        if self.hour or self.minute or self.second or self.microsecond:
            time_str = f", {self.hour}, {self.minute}, {self.second}"
            if self.microsecond:
                time_str += f", {self.microsecond}"
        if self.tzinfo is not None:
            time_str += f", tzinfo={self.tzinfo!r}"
        if self.fold:
            time_str += f", fold={self.fold}"
        return f"{self.__class__.__name__}({self.year}, {self.month}, {self.day}{time_str})"

    def __str__(self) -> str:
        return self.isoformat()

    def isoformat(self, sep: str = "T", timespec: str = "auto") -> str:
        """Returns the datetime in BS ISO 8601 format.

        The date part will be the BS date. The format is `YYYY-MM-DDTHH:MM:SS.ffffff`.
        If the object is timezone-aware, the UTC offset is also appended.

        Args:
            sep (str): The separator between the date and time. Defaults to 'T'.
            timespec (str): Specifies the precision of the time part. Can be
                'auto', 'hours', 'minutes', 'seconds', 'milliseconds', or
                'microseconds'. Defaults to 'auto'.

        Example:
            >>> dt = datetime(2081, 4, 15, 10, 30, 5, 123456, tzinfo=tz.nepal)
            >>> dt.isoformat()
            '2081-04-15T10:30:05.123456+0545'
        """
        bs_date_str = f"{self.year:04d}-{self.month:02d}-{self.day:02d}"
        if timespec == "auto":
            time_str = f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
            if self.microsecond:
                time_str += f".{self.microsecond:06d}"
        elif timespec == "hours":
            time_str = f"{self.hour:02d}"
        elif timespec == "minutes":
            time_str = f"{self.hour:02d}:{self.minute:02d}"
        elif timespec == "seconds":
            time_str = f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
        elif timespec == "milliseconds":
            time_str = f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}.{self.microsecond//1000:03d}"
        elif timespec == "microseconds":
            time_str = f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}.{self.microsecond:06d}"
        else:
            raise ValueError(f"Unknown timespec value: {timespec}")
        result = f"{bs_date_str}{sep}{time_str}"
        if self.tzinfo is not None:
            offset_str = self._get_tz_offset_str()
            if offset_str:
                result += offset_str
        return result

    def _get_tz_offset_str(self) -> str:
        """Helper to compute %z string value with DST handling."""
        if self.tzinfo is None:
            return ""
        ref_date = self.to_datetime().replace(tzinfo=None)
        tz = self.tzinfo
        if isinstance(tz, pytz.BaseTzInfo):
            try:
                aware = tz.localize(ref_date, is_dst=(self.fold == 0))
            except pytz.exceptions.AmbiguousTimeError:
                aware = tz.localize(ref_date, is_dst=(self.fold == 0))
            except pytz.exceptions.NonExistentTimeError:
                aware = tz.localize(ref_date, is_dst=(self.fold == 0))
        else:
            aware = ref_date.replace(tzinfo=tz)
        offset_delta = aware.utcoffset()
        if offset_delta is None:
            return ""
        total_seconds = offset_delta.total_seconds()
        sign = "+" if total_seconds >= 0 else "-"
        abs_total_mins = abs(int(total_seconds // 60))
        hours, mins = divmod(abs_total_mins, 60)
        return f"{sign}{hours:02d}{mins:02d}"

    def _get_tz_name_str(self) -> str:
        """Helper to compute %Z string value."""
        if self.tzinfo is not None:
            return str(self.tzinfo)
        return ""

    def strftime(self, format: str) -> str:
        """Formats the datetime using a format string with BS-specific directives.

        This method supports a rich set of directives for both date and time,
        including Nepali numerals and names.

        Args:
            format (str): The `strftime`-style format string.

        Returns:
            str: The formatted datetime string.

        Example:
            >>> dt = datetime(2081, 4, 15, 22, 10, tzinfo=tz.nepal)
            >>> dt.strftime('%Y %B %d, %I:%M %p %Z')
            '2081 Shrawan 15, 10:10 PM Asia/Kathmandu'
            >>> dt.strftime('%K %N %D, %i:%l %P')
            '२०८१ श्रावण १५, १०:१० पछिल्लो'
        """
        if not isinstance(format, str):
            raise InvalidTypeError("Format must be a string")

        # Handle %% as literal %
        temp_fmt = format.replace("%%", "__PERCENT__")

        # Validate format directives
        directives = re.findall(r"%[A-Za-z]|%%", temp_fmt)
        for directive in directives:
            if directive not in DATETIME_FORMAT_DIRECTIVES:
                raise ValueError(
                    f"Format directive '{directive}' not supported in DateTime.strftime"
                )

        bs_weekday_val = self.weekday()
        year_start = BSDate(self.year, 1, 1)
        day_of_year = self._bs_date_part.bs_toordinal() - year_start.bs_toordinal() + 1
        week_number = (
            self._bs_date_part.bs_toordinal()
            - year_start.bs_toordinal()
            + year_start.weekday()
        ) // 7 + 1

        format_code_map = {
            FORMAT_Y: lambda: f"{self.year:04d}",
            FORMAT_K: lambda: "".join(STANDARD_DIGITS[c] for c in f"{self.year:04d}"),
            FORMAT_y: lambda: f"{self.year % 100:02d}",
            FORMAT_k: lambda: "".join(
                STANDARD_DIGITS[c] for c in f"{self.year % 100:02d}"
            ),
            FORMAT_m: lambda: f"{self.month:02d}",
            FORMAT_n: lambda: "".join(STANDARD_DIGITS[c] for c in f"{self.month:02d}"),
            FORMAT_d: lambda: f"{self.day:02d}",
            FORMAT_D: lambda: "".join(STANDARD_DIGITS[c] for c in f"{self.day:02d}"),
            FORMAT_B: lambda: MONTH_NAMES_FULL[self.month - 1],
            FORMAT_N: lambda: MONTH_NAMES_FULL_NEPALI[self.month - 1],
            FORMAT_b: lambda: MONTH_NAMES_SHORT[self.month - 1],
            FORMAT_A: lambda: WEEKDAY_NAMES_FULL[bs_weekday_val],
            FORMAT_G: lambda: WEEKDAY_NAMES_FULL_NEPALI[bs_weekday_val],
            FORMAT_a: lambda: WEEKDAY_NAMES_SHORT[bs_weekday_val],
            FORMAT_w: lambda: str(bs_weekday_val),
            FORMAT_j: lambda: str(day_of_year).zfill(3),
            FORMAT_J: lambda: "".join(
                STANDARD_DIGITS[c] for c in str(day_of_year).zfill(3)
            ),
            FORMAT_U: lambda: str(week_number).zfill(2),
            FORMAT_H: lambda: f"{self.hour:02d}",
            FORMAT_h: lambda: "".join(STANDARD_DIGITS[c] for c in f"{self.hour:02d}"),
            FORMAT_I: lambda: f"{(self.hour % 12) or 12:02d}",
            FORMAT_i: lambda: "".join(
                STANDARD_DIGITS[c] for c in f"{(self.hour % 12) or 12:02d}"
            ),
            FORMAT_p: lambda: AM_PM_ENGLISH[0] if self.hour < 12 else AM_PM_ENGLISH[1],
            FORMAT_P: lambda: AM_PM_NEPALI[0] if self.hour < 12 else AM_PM_NEPALI[1],
            FORMAT_M: lambda: f"{self.minute:02d}",
            FORMAT_l: lambda: "".join(STANDARD_DIGITS[c] for c in f"{self.minute:02d}"),
            FORMAT_S: lambda: f"{self.second:02d}",
            FORMAT_s: lambda: "".join(STANDARD_DIGITS[c] for c in f"{self.second:02d}"),
            FORMAT_f: lambda: f"{self.microsecond:06d}",
            FORMAT_t: lambda: "".join(
                STANDARD_DIGITS[c] for c in f"{self.microsecond:06d}"
            ),
            FORMAT_z: self._get_tz_offset_str,
            FORMAT_Z: self._get_tz_name_str,
            FORMAT_c: lambda: f"{WEEKDAY_NAMES_SHORT[bs_weekday_val]} {MONTH_NAMES_SHORT[self.month-1]} {self.day:02d} {self.hour:02d}:{self.minute:02d}:{self.second:02d} {self.year} {self._get_tz_offset_str()}".strip(),
            FORMAT_x: lambda: f"{self.year:04d}-{self.month:02d}-{self.day:02d}",
            FORMAT_X: lambda: f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}",
            "%%": "%",
        }

        output = temp_fmt

        for directive, value_func in format_code_map.items():
            if callable(value_func):
                output = output.replace(directive, value_func())  # type: ignore
            else:
                output = output.replace(directive, value_func)
        output = output.replace("__PERCENT__", "%")

        return output

    def ctime(self) -> str:
        """Returns a string representation like 'Sun Bai 15 15:30:45 2082 +0545'.

        This is equivalent to `strftime("%c")`.
        """
        return self.strftime("%c")

    @classmethod
    def now(cls, tz: Optional[_dt.tzinfo] = None) -> "BSDatetime":
        """Creates a `BSDatetime` instance for the current local date and time.

        If `tz` is provided, the datetime will be aware of that timezone.
        Otherwise, it will be a naive datetime based on the system's locale.

        Args:
            tz (_dt.tzinfo, optional): A timezone object.

        Example:
            >>> # Get current Nepal time
            >>> nepal_now = datetime.now(tz.nepal)
            >>> print(nepal_now.strftime('%Y-%m-%d %H:%M:%S %Z'))
        """
        greg_now = _dt.datetime.now(tz)
        bs_y, bs_m, bs_d = ad_to_bs(greg_now.date())
        return cls(
            bs_y,
            bs_m,
            bs_d,
            greg_now.hour,
            greg_now.minute,
            greg_now.second,
            greg_now.microsecond,
            greg_now.tzinfo,
            fold=greg_now.fold,
        )

    @classmethod
    def utcnow(cls) -> "BSDatetime":
        """Creates a `BSDatetime` instance for the current UTC date and time.

        The returned object is timezone-aware with its `tzinfo` set to `tz.utc`.

        Example:
            >>> utc_now = datetime.utcnow()
            >>> print(utc_now.tzinfo)
            UTC
        """
        greg_utcnow = _dt.datetime.now(pytz.UTC)
        bs_y, bs_m, bs_d = ad_to_bs(greg_utcnow.date())
        return cls(
            bs_y,
            bs_m,
            bs_d,
            greg_utcnow.hour,
            greg_utcnow.minute,
            greg_utcnow.second,
            greg_utcnow.microsecond,
            greg_utcnow.tzinfo,
            fold=greg_utcnow.fold,
        )

    @classmethod
    def fromisoformat(cls, date_string: str) -> "BSDatetime":
        """Creates a `BSDatetime` from a BS ISO 8601 formatted string.

        Parses strings like `'2081-04-15T10:30:00+05:45'` or `'2081-04-15'`.

        Example:
            >>> dt = datetime.fromisoformat('2081-04-15T22:10:00+05:45')
            >>> dt.year, dt.hour, dt.tzname()
            (2081, 22, 'Asia/Kathmandu')
        """
        if not isinstance(date_string, str):
            raise InvalidTypeError("fromisoformat: argument must be str")
        sep = "T" if "T" in date_string else " "
        date_part, time_part = (
            date_string.split(sep, 1) if sep in date_string else (date_string, "")
        )
        try:
            year, month, day = map(int, date_part.split("-"))
        except ValueError:
            raise ValueError(f"Invalid date format in ISO string: '{date_string}'")
        hour = minute = second = microsecond = 0
        tzinfo = None
        fold = 0

        if time_part:
            tz_part = ""
            # Check for timezone indicator (Z, +HHMM, -HH:MM)
            if time_part.endswith("Z"):
                tz_part = "Z"
                time_part = time_part[:-1]  # Remove Z
            elif "+" in time_part or "-" in time_part:
                # Find the last + or - not part of time (after last :)
                idx = max(time_part.rfind("+"), time_part.rfind("-"))
                if idx > time_part.rfind(":"):
                    tz_part = time_part[idx:]
                    time_part = time_part[:idx]

            # Now parse time components
            time_components = time_part.split(":")
            if len(time_components) >= 1:
                hour = int(time_components[0])
            if len(time_components) >= 2:
                minute = int(time_components[1])
            if len(time_components) >= 3:
                sec_parts = time_components[2].split(".")
                second = int(sec_parts[0])  # Now sec_parts[0] = "45", not "45Z"
                if len(sec_parts) > 1:
                    microsecond = int(sec_parts[1].ljust(6, "0")[:6])

            # Parse timezone
            if tz_part:
                from .strptime import _find_timezone_for_offset

                if tz_part == "Z":
                    tzinfo = pytz.UTC
                else:
                    try:
                        if len(tz_part) < 3:  # At least +HH
                            raise ValueError(f"Invalid timezone format: {tz_part}")
                        sign = 1 if tz_part[0] == "+" else -1
                        if ":" in tz_part:
                            tz_parts = tz_part[1:].split(":")
                            tz_hour = int(tz_parts[0])
                            tz_minute = int(tz_parts[1]) if len(tz_parts) > 1 else 0
                        else:
                            tz_hour = int(tz_part[1:3]) if len(tz_part) >= 3 else 0
                            tz_minute = int(tz_part[3:5]) if len(tz_part) >= 5 else 0
                        offset_minutes = sign * (tz_hour * 60 + tz_minute)
                        if abs(offset_minutes) > 1440:  # Max 24 hours
                            raise ValueError(
                                f"Timezone offset {tz_part} exceeds 24 hours"
                            )
                        tzinfo = _find_timezone_for_offset(
                            offset_minutes, year, month, day
                        )
                    except (ValueError, IndexError) as e:
                        raise ValueError(f"Invalid timezone format: {tz_part}") from e

        return cls(
            year, month, day, hour, minute, second, microsecond, tzinfo, fold=fold
        )

    @classmethod
    def fromstrftime(cls, date_string: str, format: str) -> "BSDatetime":
        """Parses a string into a `BSDatetime` object according to a format.

        This is the reverse of `strftime`. It can parse strings containing
        both English and Nepali names and numerals.

        Example:
            >>> date_str = "2081 Shrawan 15, 10:10 PM"
            >>> format_str = "%Y %B %d, %I:%M %p"
            >>> datetime.fromstrftime(date_str, format_str)
            bikram_sambat.datetime.BSDatetime(2081, 4, 15, 22, 10)
        """
        from .strptime import _strptime_datetime

        return _strptime_datetime(cls, date_string, format)

    @classmethod
    def combine(  # type: ignore
        cls, date: BSDate, time: _dt.time, tzinfo: Union[bool, _dt.tzinfo] = True
    ) -> "BSDatetime":  # type: ignore
        """Creates a new `BSDatetime` by combining a `BSDate` and a `datetime.time`.

        Args:
            date (BSDate): The date part.
            time (_dt.time): The time part.
            tzinfo (Union[bool, _dt.tzinfo]): If True (default), use `time.tzinfo`.
                If a tzinfo object, use it. If False, the result is naive.

        Example:
            >>> from bikram_sambat import date
            >>> import datetime as pydt
            >>> d = date(2081, 4, 15)
            >>> t = pydt.time(10, 30, tzinfo=tz.nepal)
            >>> datetime.combine(d, t)
            bikram_sambat.datetime.BSDatetime(2081, 4, 15, 10, 30, tzinfo=<DstTzInfo 'Asia/Kathmandu' NPT+5:45:00 STD>)
        """
        if not isinstance(date, BSDate):
            raise InvalidTypeError("date argument must be a BSDate instance")
        if not isinstance(time, _dt.time):
            raise InvalidTypeError("time argument must be a datetime.time instance")
        final_tzinfo = (
            time.tzinfo if tzinfo is True else tzinfo if tzinfo is not False else None
        )
        return cls(
            date.year,
            date.month,
            date.day,
            time.hour,
            time.minute,
            time.second,
            time.microsecond,
            final_tzinfo,
            fold=time.fold,
        )

    def replace(  # type: ignore
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
        second: Optional[int] = None,
        microsecond: Optional[int] = None,
        tzinfo: Union[bool, _dt.tzinfo, None] = True,
        *,
        fold: Optional[int] = None,
    ) -> "BSDatetime":
        """Returns a new `BSDatetime` with specified components replaced."""
        new_year = self.year if year is None else year
        new_month = self.month if month is None else month
        new_day = self.day if day is None else day
        new_hour = self.hour if hour is None else hour
        new_minute = self.minute if minute is None else minute
        new_second = self.second if second is None else second
        new_microsecond = self.microsecond if microsecond is None else microsecond
        new_tzinfo = self.tzinfo if tzinfo is True else tzinfo
        new_fold = self.fold if fold is None else fold
        return self.__class__(
            new_year,
            new_month,
            new_day,
            new_hour,
            new_minute,
            new_second,
            new_microsecond,
            new_tzinfo,  # type: ignore
            fold=new_fold,
        )

    def astimezone(self, tz: Optional[_dt.tzinfo] = None) -> "BSDatetime":
        """Converts the datetime to a different timezone.

        If the instance is naive, it is treated as system local time.
        The `tz` argument can be any `datetime.tzinfo` or `pytz` timezone object.

        Args:
            tz (_dt.tzinfo, optional): The target timezone. If None, converts
                to the system's local timezone.

        Returns:
            BSDatetime: A new, timezone-aware `BSDatetime` instance.

        Example:
            >>> dt_nepal = datetime(2081, 4, 15, 10, 30, tzinfo=tz.nepal)
            >>> dt_utc = dt_nepal.astimezone(tz.utc)
            >>> print(dt_utc)
            2081-04-15T04:45:00+00:00
        """
        greg_dt = self.to_datetime()
        converted_greg_dt = greg_dt.astimezone(tz)
        return self.from_datetime(converted_greg_dt)

    def __add__(self, other):
        """Adds a timedelta, returning a new `BSDatetime`."""
        if isinstance(other, (_dt.timedelta, BSTimedelta)):
            delta = _dt.timedelta(
                days=other.days, seconds=other.seconds, microseconds=other.microseconds
            )
            greg_dt = self.to_datetime()
            result_greg_dt = greg_dt + delta
            return self.from_datetime(result_greg_dt)
        return NotImplemented

    def __sub__(self, other):
        """Subtracts a timedelta or another datetime.

        If `other` is a `timedelta`, returns a new `BSDatetime`.
        If `other` is a `BSDatetime` or `datetime.datetime`, returns a `BSTimedelta`.
        """
        if isinstance(other, (_dt.timedelta, BSTimedelta)):
            delta = _dt.timedelta(
                days=other.days, seconds=other.seconds, microseconds=other.microseconds
            )
            greg_dt = self.to_datetime()
            result_greg_dt = greg_dt - delta
            return self.from_datetime(result_greg_dt)
        if isinstance(other, (BSDatetime, _dt.datetime)):
            other_greg = other.to_datetime() if isinstance(other, BSDatetime) else other
            delta = self.to_datetime() - other_greg
            return BSTimedelta(
                days=delta.days, seconds=delta.seconds, microseconds=delta.microseconds
            )
        return NotImplemented

    def weekday(self) -> int:
        return self._bs_date_part.weekday()

    def isoweekday(self) -> int:
        return self._bs_date_part.isoweekday()

    def bs_date_toordinal(self) -> int:
        return self._bs_date_part.bs_toordinal()

    @classmethod
    def from_datetime(cls, greg_dt: _dt.datetime) -> "BSDatetime":
        """Creates a `BSDatetime` from a standard `datetime.datetime` (Gregorian) object.

        This is the primary way to convert a Gregorian datetime to a BS datetime.
        Timezone information is preserved.

        Args:
            greg_dt (_dt.datetime): The Gregorian datetime object to convert.

        Returns:
            BSDatetime: The equivalent `BSDatetime` object.
        """
        if not isinstance(greg_dt, _dt.datetime):
            raise InvalidTypeError("Input must be a datetime.datetime object.")
        bs_y, bs_m, bs_d = ad_to_bs(greg_dt.date())
        tzinfo = greg_dt.tzinfo
        if tzinfo is not None and isinstance(tzinfo, pytz.BaseTzInfo):
            temp_dt = _dt.datetime(
                greg_dt.year,
                greg_dt.month,
                greg_dt.day,
                greg_dt.hour,
                greg_dt.minute,
                greg_dt.second,
                greg_dt.microsecond,
            )
            try:
                localized_dt = tzinfo.localize(temp_dt, is_dst=None)
            except pytz.exceptions.AmbiguousTimeError:
                localized_dt = tzinfo.localize(temp_dt, is_dst=(greg_dt.fold == 0))
            except pytz.exceptions.NonExistentTimeError:
                localized_dt = tzinfo.localize(temp_dt, is_dst=(greg_dt.fold == 0))
            tzinfo = localized_dt.tzinfo
        return cls(
            bs_y,
            bs_m,
            bs_d,
            greg_dt.hour,
            greg_dt.minute,
            greg_dt.second,
            greg_dt.microsecond,
            tzinfo=tzinfo,
            fold=greg_dt.fold,
        )

    def to_datetime(self) -> _dt.datetime:
        """Converts the `BSDatetime` object to a standard `datetime.datetime` object.

        This is the primary way to convert a BS datetime to a Gregorian datetime.
        Timezone information is preserved.

        Returns:
            _dt.datetime: The equivalent Gregorian datetime object.
        """
        greg_date = bs_to_ad(self.year, self.month, self.day)
        tzinfo = self.tzinfo
        if tzinfo is not None and isinstance(tzinfo, pytz.BaseTzInfo):
            temp_dt = _dt.datetime(
                greg_date.year,
                greg_date.month,
                greg_date.day,
                self.hour,
                self.minute,
                self.second,
                self.microsecond,
            )
            try:
                localized_dt = tzinfo.localize(temp_dt, is_dst=None)
            except pytz.exceptions.AmbiguousTimeError:
                localized_dt = tzinfo.localize(temp_dt, is_dst=(self.fold == 0))
            except pytz.exceptions.NonExistentTimeError:
                localized_dt = tzinfo.localize(temp_dt, is_dst=(self.fold == 0))
            tzinfo = localized_dt.tzinfo
        return _dt.datetime(
            greg_date.year,
            greg_date.month,
            greg_date.day,
            self.hour,
            self.minute,
            self.second,
            self.microsecond,
            tzinfo=tzinfo,
            fold=self.fold,
        )

    def __getnewargs_ex__(self):
        args = (
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            self.second,
            self.microsecond,
        )
        kwargs = {}
        if self.tzinfo is not None:
            args = args + (self.tzinfo,)
        if self.fold != 0:
            kwargs["fold"] = self.fold
        return args, kwargs

    def __reduce_ex__(self, protocol):
        args, kwargs = self.__getnewargs_ex__()
        return (type(self), args, kwargs)

    def togregorian(self) -> _dt.datetime:
        """Alias for `to_datetime()`. Converts to a standard `datetime.datetime` object."""
        greg_date = bs_to_ad(self.year, self.month, self.day)
        tzinfo = self.tzinfo
        if tzinfo is not None and isinstance(tzinfo, pytz.BaseTzInfo):
            temp_dt = _dt.datetime(
                greg_date.year,
                greg_date.month,
                greg_date.day,
                self.hour,
                self.minute,
                self.second,
                self.microsecond,
            )
            try:
                localized_dt = tzinfo.localize(temp_dt, is_dst=(self.fold == 0))
            except pytz.exceptions.AmbiguousTimeError:
                localized_dt = tzinfo.localize(temp_dt, is_dst=(self.fold == 0))
            except pytz.exceptions.NonExistentTimeError:
                localized_dt = tzinfo.localize(temp_dt, is_dst=(self.fold == 0))
            tzinfo = localized_dt.tzinfo
        return _dt.datetime(
            greg_date.year,
            greg_date.month,
            greg_date.day,
            self.hour,
            self.minute,
            self.second,
            self.microsecond,
            tzinfo=tzinfo,
            fold=self.fold,
        )

    @classmethod
    def fromgregorian(cls, greg_dt: _dt.datetime) -> "BSDatetime":
        """Alias for `from_datetime()`. Creates a `BSDatetime` from a `datetime.datetime`."""
        if not isinstance(greg_dt, _dt.datetime):
            raise InvalidTypeError("Input must be a datetime.datetime object.")
        bs_year, bs_month, bs_day = ad_to_bs(greg_dt.date())
        tzinfo = greg_dt.tzinfo
        if tzinfo is not None and isinstance(tzinfo, pytz.BaseTzInfo):
            temp_dt = _dt.datetime(
                greg_dt.year,
                greg_dt.month,
                greg_dt.day,
                greg_dt.hour,
                greg_dt.minute,
                greg_dt.second,
                greg_dt.microsecond,
            )
            try:
                # Try localizing with is_dst=None to detect ambiguity
                greg_dt_localized = tzinfo.localize(temp_dt, is_dst=None)
            except pytz.exceptions.AmbiguousTimeError:
                # Resolve ambiguity using fold: fold=0 → DST (EDT), fold=1 → non-DST (EST)
                greg_dt_localized = tzinfo.localize(temp_dt, is_dst=(greg_dt.fold == 0))
            tzinfo = greg_dt_localized.tzinfo
        return cls(
            bs_year,
            bs_month,
            bs_day,
            greg_dt.hour,
            greg_dt.minute,
            greg_dt.second,
            greg_dt.microsecond,
            tzinfo=tzinfo,  # Use localized tzinfo
            fold=greg_dt.fold,
        )
