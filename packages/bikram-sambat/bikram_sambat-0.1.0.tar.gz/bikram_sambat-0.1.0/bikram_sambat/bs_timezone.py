"""Provides timezone utilities and objects for the bikram_sambat package.

This module acts as a convenient wrapper around the `pytz` library, offering
pre-configured timezone objects for common regions like Nepal, India, and UTC.
It also provides access to the full list of IANA timezones and a function
to retrieve any `pytz` timezone by name.

This module is designed to be imported as `tz` for concise usage.

Attributes:
    nepal (_dt.tzinfo): The Nepal Standard Time (NPT) timezone object.
    utc (_dt.tzinfo): The Coordinated Universal Time (UTC) timezone object.
    india (_dt.tzinfo): The Indian Standard Time (IST) timezone object.
    get_timezone (Callable[[str], _dt.tzinfo]): A function to get a timezone
        by its IANA name (e.g., 'America/New_York').
    all_timezones_list (list[str]): A list of all available IANA timezone names.
    tzinfo_base (type): An alias for `datetime.tzinfo`, useful for type hinting.

Example:
    >>> from bikram_sambat import datetime, tz
    >>>
    >>> # Create a naive datetime
    >>> bs_dt = datetime(2081, 4, 15, 10, 30, 0)
    >>>
    >>> # Localize it to Nepal time
    >>> nepal_dt = tz.nepal.localize(bs_dt)
    >>> print(nepal_dt)
    2081-04-15 10:30:00+05:45
    >>>
    >>> # Convert to UTC
    >>> utc_dt = nepal_dt.astimezone(tz.utc)
    >>> print(utc_dt)
    2081-04-15 04:45:00+00:00
"""

import datetime as _dt
import pytz
from typing import List


class _BikramSambatTimezoneManager:
    """An internal manager for instantiating and holding timezone objects.

    This class is an implementation detail and should not be used directly by
    end-users. It ensures that core timezone objects are created only once
    and handles the dependency on `pytz`. The module-level variables
    (`nepal`, `utc`, etc.) are the intended public interface.
    """

    __slots__ = ("_nepal_tz", "_utc_tz", "_india_tz")

    def __init__(self):
        """Initializes the timezone manager and loads core timezones.

        Raises:
            ImportError: If the `pytz` library is not installed.
        """
        try:
            self._nepal_tz = pytz.timezone("Asia/Kathmandu")
            self._india_tz = pytz.timezone("Asia/Kolkata")
        except pytz.exceptions.UnknownTimeZoneError:
            raise ImportError(
                "pytz is required for timezone support. Install with 'pip install pytz'."
            )
        self._utc_tz = pytz.UTC

    @property
    def nepal(self) -> _dt.tzinfo:
        """Gets the Nepal timezone object (`Asia/Kathmandu`)."""
        return self._nepal_tz

    @property
    def india(self) -> _dt.tzinfo:
        """Gets the India timezone object (`Asia/Kolkata`)."""
        return self._india_tz

    @property
    def utc(self) -> _dt.tzinfo:
        """Gets the UTC timezone object."""
        return self._utc_tz

    def get(self, name: str) -> _dt.tzinfo:
        """Gets a timezone by its IANA name.

        This is a direct proxy to `pytz.timezone()`.

        Args:
            name (str): The IANA timezone name (e.g., 'America/New_York').

        Returns:
            _dt.tzinfo: The corresponding `pytz` timezone object.

        Raises:
            pytz.exceptions.UnknownTimeZoneError: If the timezone name is not found.
        """
        return pytz.timezone(name)

    @property
    def all_timezones(self) -> List[str]:
        """Gets a list of all available IANA timezone names."""
        return pytz.all_timezones


_manager = _BikramSambatTimezoneManager()


nepal: _dt.tzinfo = _manager.nepal
"""_dt.tzinfo: The Nepal Standard Time (NPT) timezone object (`Asia/Kathmandu`)."""

utc: _dt.tzinfo = _manager.utc
"""_dt.tzinfo: The Coordinated Universal Time (UTC) timezone object."""

india: _dt.tzinfo = _manager.india
"""_dt.tzinfo: The Indian Standard Time (IST) timezone object (`Asia/Kolkata`)."""

get_timezone = _manager.get
"""Callable[[str], _dt.tzinfo]: Function to get a timezone by its IANA name."""

all_timezones_list = _manager.all_timezones
"""List[str]: A list of all available IANA timezone names."""

tzinfo_base: type = _dt.tzinfo
"""type: An alias for `datetime.tzinfo`, useful for type hinting."""

__all__ = ["nepal", "utc", "india", "get_timezone", "all_timezones_list", "tzinfo_base"]
