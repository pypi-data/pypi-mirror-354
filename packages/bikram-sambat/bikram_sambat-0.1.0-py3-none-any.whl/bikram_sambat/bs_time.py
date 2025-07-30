"""Defines the BSTime class for representing time-of-day.

This module provides a timezone-aware `BSTime` object, which is a subclass of
the standard `datetime.time`. It supports all the functionality of the parent
class but adds BS-specific formatting capabilities, such as rendering time
components in Nepali numerals.
"""

import re
import datetime as _dt
from typing import Any, Optional, Dict, Callable

import pytz

from .exceptions import InvalidTypeError
from .constants import (
    NEPALI_DIGITS,
    STANDARD_DIGITS,
    AM_PM_ENGLISH,
    AM_PM_NEPALI,
    FORMAT_H,
    FORMAT_h,
    FORMAT_I,
    FORMAT_i,
    FORMAT_M,
    FORMAT_l,
    FORMAT_S,
    FORMAT_s,
    FORMAT_f,
    FORMAT_t,
    FORMAT_p,
    FORMAT_P,
    FORMAT_z,
    FORMAT_Z,
    FORMAT_X,
    TIME_FORMAT_DIRECTIVES,
)


class BSTime(_dt.time):
    """Represents a time of day, independent of any particular day.

    `BSTime` is a subclass of the standard `datetime.time` class and is fully
    compatible with it. It extends the base class with enhanced formatting
    options via the `strftime` method, which supports Nepali numerals (e.g., `%h`)
    and Nepali AM/PM designators (e.g., `%P`).

    The constructor accepts all the same arguments as `datetime.time`, including
    `tzinfo` for creating timezone-aware time objects.

    Args:
        hour (int): The hour (0-23). Defaults to 0.
        minute (int): The minute (0-59). Defaults to 0.
        second (int): The second (0-59). Defaults to 0.
        microsecond (int): The microsecond (0-999999). Defaults to 0.
        tzinfo (_dt.tzinfo, optional): The timezone object. Defaults to None.
        fold (int): Used to disambiguate wall times during a repeated hour
            (e.g., during a DST transition). 0 or 1. Defaults to 0.

    Attributes:
        min (BSTime): The earliest representable `BSTime`, `00:00:00`.
        max (BSTime): The latest representable `BSTime`, `23:59:59.999999`.
    """

    __slots__ = ()

    def __new__(
        cls,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
        tzinfo: Optional[_dt.tzinfo] = None,
        *,
        fold: int = 0,
    ):
        """Creates a new BSTime instance.

        Raises:
            InvalidTypeError: If `tzinfo` is not a valid tzinfo object.
        """
        if tzinfo is not None:
            if not isinstance(tzinfo, _dt.tzinfo):
                raise InvalidTypeError("tzinfo must be a tzinfo object or None")
            if not isinstance(tzinfo, (pytz.BaseTzInfo, _dt.timezone)):
                raise InvalidTypeError(
                    "tzinfo must be a pytz or datetime.timezone object"
                )
        return super().__new__(
            cls, hour, minute, second, microsecond, tzinfo, fold=fold
        )

    def __repr__(self) -> str:
        """Returns the official, unambiguous string representation of the BSTime."""
        components = [str(self.hour), str(self.minute)]
        if self.second or self.microsecond:
            components.append(str(self.second))
        if self.microsecond:
            components.append(str(self.microsecond))

        res = "%s.%s(%s)" % (
            self.__class__.__module__,
            self.__class__.__name__,
            ", ".join(components),
        )

        # Append tzinfo and fold if they exist
        if self.tzinfo is not None:
            res = res[:-1] + ", tzinfo=%r)" % self.tzinfo
        if self.fold:  # datetime.time includes fold only if it's non-zero (typically 1)
            res = res[:-1] + ", fold=%d)" % self.fold

        return res

    def __str__(self) -> str:
        """Returns the ISO 8601 string representation of the time."""
        return self.isoformat()

    def __getnewargs_ex__(self):
        """Supports pickling and copying of the BSTime object."""
        args = (self.hour, self.minute, self.second, self.microsecond)
        kwargs = {}
        if self.tzinfo is not None:
            args = args + (self.tzinfo,)
        if self.fold != 0:
            kwargs["fold"] = self.fold
        return args, kwargs

    def __reduce_ex__(self, protocol):
        """Supports an older pickling protocol."""

        return (
            type(self),
            (
                self.hour,
                self.minute,
                self.second,
                self.microsecond,
                self.tzinfo,
                # self.fold,
            ),
        )

    def _get_tz_offset_str(self) -> str:
        """Computes the UTC offset string (e.g., '+0545') for the `%z` directive.

        Returns:
            str: The formatted UTC offset, or an empty string if naive.
        """
        if self.tzinfo is None:
            return ""
        # Use current date for accurate DST handling
        ref_date = _dt.datetime.now().replace(
            hour=self.hour,
            minute=self.minute,
            second=self.second,
            microsecond=self.microsecond,
        )
        tz = self.tzinfo
        if isinstance(tz, pytz.BaseTzInfo):
            aware = tz.localize(ref_date)
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
        """Computes the timezone name string (e.g., 'Asia/Kathmandu') for the `%Z` directive.

        Returns:
            str: The timezone name, or an empty string if naive.
        """
        if self.tzinfo is not None:
            return str(self.tzinfo)
        return ""

    def strftime(self, format: str) -> str:
        """Formats the time according to a format string with BS-specific directives.

        This method supports all standard `strftime` directives for time, plus
        custom directives for Nepali numerals and AM/PM indicators.

        Example:
            >>> t = BSTime(15, 30, tzinfo=pytz.timezone("Asia/Kathmandu"))
            >>> t.strftime("%H:%M %P")
            '15:30 पछिल्लो'
            >>> t.strftime("%I:%M %p in Nepali is %i:%l")
            '03:30 PM in Nepali is ०३:३०'

        Args:
            format (str): The `strftime`-style format string.

        Returns:
            str: The formatted time string.

        Raises:
            InvalidTypeError: If the format is not a string.
            ValueError: If the format string contains an unsupported directive.
        """
        if not isinstance(format, str):
            raise InvalidTypeError("format must be a string")

        temp_fmt = format.replace("%%", "__PERCENT__")

        directives = re.findall(r"%[A-Za-z]|%%", temp_fmt)
        for directive in directives:
            if directive not in TIME_FORMAT_DIRECTIVES:
                raise ValueError(
                    f"Format directive '{directive}' not supported in Time.strftime"
                )
        format_code_map = {
            FORMAT_H: lambda: f"{self.hour:02d}",
            FORMAT_h: lambda: "".join(STANDARD_DIGITS[c] for c in f"{self.hour:02d}"),
            FORMAT_I: lambda: f"{(self.hour % 12) or 12:02d}",
            FORMAT_i: lambda: "".join(
                STANDARD_DIGITS[c] for c in f"{(self.hour % 12) or 12:02d}"
            ),
            FORMAT_M: lambda: f"{self.minute:02d}",
            FORMAT_l: lambda: "".join(STANDARD_DIGITS[c] for c in f"{self.minute:02d}"),
            FORMAT_S: lambda: f"{self.second:02d}",
            FORMAT_s: lambda: "".join(STANDARD_DIGITS[c] for c in f"{self.second:02d}"),
            FORMAT_f: lambda: f"{self.microsecond:06d}",
            FORMAT_t: lambda: "".join(
                STANDARD_DIGITS[c] for c in f"{self.microsecond:06d}"
            ),
            FORMAT_p: lambda: AM_PM_ENGLISH[0] if self.hour < 12 else AM_PM_ENGLISH[1],
            FORMAT_P: lambda: AM_PM_NEPALI[0] if self.hour < 12 else AM_PM_NEPALI[1],
            FORMAT_X: lambda: f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}",
            # %z and %Z need special handling as their values depend on tzinfo
            FORMAT_z: self._get_tz_offset_str,  # Use method reference
            FORMAT_Z: self._get_tz_name_str,  # Use method reference
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

    @classmethod
    def fromstrftime(cls, time_string: str, format: str) -> "BSTime":
        """Parses a string into a BSTime object according to a format.

        This class method provides a flexible way to create `BSTime` instances
        from strings, including those with Nepali numerals or names.

        Example:
            >>> BSTime.fromstrftime("15:30 पछिल्लो", "%H:%M %P")
            bikram_sambat.time.BSTime(15, 30)

        Args:
            time_string (str): The string to parse.
            format (str): The `strftime` format that the `time_string` follows.

        Returns:
            BSTime: A new `BSTime` instance.
        """
        from .strptime import _strptime_time

        return _strptime_time(cls, time_string, format)

    def utcoffset(self, dt=None) -> Optional[_dt.timedelta]:
        """Returns the UTC offset if the time is timezone-aware.

        Returns:
            Optional[_dt.timedelta]: The UTC offset as a `timedelta` object,
            or None if the instance is naive.
        """
        if self.tzinfo is None:
            return None

        # Let’s use “today” in that zone so DST & historical rules apply.
        ref = _dt.datetime.now(self.tzinfo)
        return self.tzinfo.utcoffset(ref)

    def tzname(self, dt=None) -> Optional[str]:
        """Returns the timezone name if the time is timezone-aware.

        Returns:
            Optional[str]: The timezone name as a string, or None if the
            instance is naive.
        """
        if self.tzinfo is None:
            return None

        # Again, pick “now” so DST vs standard name is correct.
        ref = _dt.datetime.now(self.tzinfo)
        return self.tzinfo.tzname(ref)


BSTime.min = BSTime(0, 0, 0, 0)
"""BSTime: The earliest representable `BSTime`, `00:00:00`."""

BSTime.max = BSTime(23, 59, 59, 999999)
"""BSTime: The latest representable `BSTime`, `23:59:59.999999`."""
