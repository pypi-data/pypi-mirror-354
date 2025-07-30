"""Defines the BSTimedelta class for representing time durations.

This module provides a timedelta object that is a subclass of the standard
`datetime.timedelta`, extending it with custom string formatting capabilities,
including support for Nepali numerals.
"""

import datetime as _dt

from .exceptions import InvalidTypeError
from .constants import STANDARD_DIGITS


class BSTimedelta(_dt.timedelta):
    """Represents a duration, the difference between two dates or times.

    `BSTimedelta` is a subclass of the standard `datetime.timedelta` and supports
    all the same operations and arguments. Its main enhancement is a more
    descriptive `__str__` method that can optionally display durations using
    Nepali numerals. All arithmetic operations will correctly return a new
    `BSTimedelta` instance.

    Args:
        days (float): Number of days. Defaults to 0.
        seconds (float): Number of seconds. Defaults to 0.
        microseconds (float): Number of microseconds. Defaults to 0.
        milliseconds (float): Number of milliseconds. Defaults to 0.
        minutes (float): Number of minutes. Defaults to 0.
        hours (float): Number of hours. Defaults to 0.
        weeks (float): Number of weeks. Defaults to 0.

    Example:
        >>> delta = BSTimedelta(days=5, hours=10)
        >>> print(delta)
        5 days, 10:00:00
        >>> print(delta.__str__(use_nepali_digits=True))
        ५ दिन, १०:००:००
    """

    def __new__(
        cls,
        days=0,
        seconds=0,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0,
    ):
        for name, value in [
            ("days", days),
            ("seconds", seconds),
            ("microseconds", microseconds),
            ("milliseconds", milliseconds),
            ("minutes", minutes),
            ("hours", hours),
            ("weeks", weeks),
        ]:
            if value != 0 and not isinstance(value, (int, float)):
                raise InvalidTypeError(
                    f"unsupported type for timedelta {name} component: {type(value).__name__}"
                )
        return super().__new__(
            cls, days, seconds, microseconds, milliseconds, minutes, hours, weeks
        )

    def __repr__(self) -> str:
        """Returns the official, unambiguous string representation of the BSTimedelta."""

        args = []
        if self.days:
            args.append(f"days={self.days}")
        if self.seconds:
            args.append(f"seconds={self.seconds}")
        if self.microseconds:
            args.append(f"microseconds={self.microseconds}")
        return (
            f"{self.__class__.__module__}.{self.__class__.__name__}({', '.join(args)})"
        )

    def __str__(self, use_nepali_digits: bool = False) -> str:
        """Returns a user-friendly string representation of the timedelta.

        Formats the duration into a "X day(s), H:MM:SS.f" style. It can also
        render all numerical components in Nepali Unicode characters.

        Args:
            use_nepali_digits (bool): If True, all numbers in the output string
                will be represented using Nepali numerals. Defaults to False.

        Returns:
            str: The formatted string representation of the duration.
        """
        if self.total_seconds() == 0:
            return "0:00:00"

        is_negative = self < _dt.timedelta(0)
        # For calculations, work with the absolute value of the timedelta
        delta = -self if is_negative else self

        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        parts = []
        if days:
            days_str = str(days)
            if use_nepali_digits:
                nepali_days = "".join(STANDARD_DIGITS[c] for c in days_str)
                parts.append(f"{nepali_days} दिन{'हरू' if days != 1 else ''}")
            else:
                parts.append(f"{days_str} day{'s' if days != 1 else ''}")

        time_values = {
            "hours": str(hours),
            "minutes": str(minutes).zfill(2),
            "seconds": str(seconds).zfill(2),
        }

        if use_nepali_digits:
            for key, value in time_values.items():
                time_values[key] = "".join(STANDARD_DIGITS[c] for c in value)

        time_str = f"{time_values['hours']}:{time_values['minutes']}:{time_values['seconds']}"

        if delta.microseconds:
            micro_str = str(delta.microseconds).zfill(6)
            if use_nepali_digits:
                micro_str = "".join(STANDARD_DIGITS[c] for c in micro_str)
            time_str += f".{micro_str}"

        parts.append(time_str)
        result = ", ".join(parts)

        return f"-{result}" if is_negative else result
    
    # def __str__(self, use_nepali_digits: bool = False) -> str:
    #     """Returns a user-friendly string representation of the timedelta.

    #     Formats the duration into a "X day(s), H:MM:SS.f" style. It can also
    #     render all numerical components in Nepali Unicode characters.

    #     Args:
    #         use_nepali_digits (bool): If True, all numbers in the output string
    #             will be represented using Nepali numerals. Defaults to False.

    #     Returns:
    #         str: The formatted string representation of the duration.
    #     """
    #     if not self:
    #         return "0:00:00"
    #     days = abs(self.days)
    #     hours, remainder = divmod(abs(self.seconds), 3600)
    #     minutes, seconds = divmod(remainder, 60)
    #     parts = []
    #     if days:
    #         if use_nepali_digits:
    #             days_str = "".join(STANDARD_DIGITS[c] for c in str(days))
    #             parts.append(f"{days_str} दिन{'हरू' if days != 1 else ''}")
    #         else:
    #             parts.append(f"{days} day{'s' if days != 1 else ''}")
    #     hours_str = str(hours).lstrip("0") or "0"
    #     if use_nepali_digits:
    #         hours_str = "".join(STANDARD_DIGITS[c] for c in hours_str)
    #         minutes_str = "".join(STANDARD_DIGITS[c] for c in str(minutes).zfill(2))
    #         seconds_str = "".join(STANDARD_DIGITS[c] for c in str(seconds).zfill(2))
    #     else:
    #         minutes_str = str(minutes).zfill(2)
    #         seconds_str = str(seconds).zfill(2)
    #     time_str = f"{hours_str}:{minutes_str}:{seconds_str}"
    #     if self.microseconds:
    #         micro_str = str(abs(self.microseconds)).zfill(6)
    #         if use_nepali_digits:
    #             micro_str = "".join(STANDARD_DIGITS[c] for c in micro_str)
    #         time_str += f".{micro_str}"
    #     parts.append(time_str)
    #     result = ", ".join(parts)
    #     return f"-{result}" if self < BSTimedelta() else result

    def __add__(self, other):
        """Adds another timedelta, returning a new BSTimedelta instance."""
        result = super().__add__(other)
        return self.__class__(
            days=result.days, seconds=result.seconds, microseconds=result.microseconds
        )

    def __sub__(self, other):
        """Subtracts another timedelta, returning a new BSTimedelta instance."""

        result = super().__sub__(other)
        return self.__class__(
            days=result.days, seconds=result.seconds, microseconds=result.microseconds
        )

    def __mul__(self, other):
        """Multiplies by a float or int, returning a new BSTimedelta instance."""

        result = super().__mul__(other)
        return self.__class__(
            days=result.days, seconds=result.seconds, microseconds=result.microseconds
        )

    def __truediv__(self, other):  # type: ignore
        """Divides by another timedelta or number, returning a BSTimedelta if applicable."""

        if isinstance(other, (int, float)):
            result = super().__truediv__(other)
            return self.__class__(
                days=result.days,
                seconds=result.seconds,
                microseconds=result.microseconds,
            )
        return super().__truediv__(other)

    def __reduce__(self):
        """Supports pickling of the BSTimedelta object for serialization."""

        return (self.__class__, (self.days, self.seconds, self.microseconds))
