"""Defines custom exception classes for the bikram_sambat package.

These exceptions provide specific error details for issues like invalid dates,
out-of-range values, and type mismatches. They all inherit from a common
base, BikramSambatError, allowing for easy and specific error handling.
"""


class BikramSambatError(Exception):
    """The base exception class for all errors raised by the bikram_sambat library.

    This exception can be used as a catch-all for any error originating from
    this package. However, it is generally recommended to catch the more
    specific subclasses for finer-grained error handling.
    """

    pass


class DateOutOfRangeError(BikramSambatError, ValueError):
    """Raised when a date is outside the supported BS calendar range.

    This error is raised for dates that are syntactically plausible but fall
    outside the operational range of the calendar data (e.g., a year before
    1901 or after 2199).

    Inherits from:
        ValueError: For compatibility with checks for invalid value semantics.
        BikramSambatError: To be part of the package's exception hierarchy.
    """

    pass


class InvalidDateError(BikramSambatError, ValueError):
    """Raised for a date that is logically impossible.

    This error indicates that a component of the date is invalid, such as a
    month outside the 1-12 range or a day that does not exist for the given
    month and year (e.g., Baishakh 32).

    Inherits from:
        ValueError: For compatibility with checks for invalid value semantics.
        BikramSambatError: To be part of the package's exception hierarchy.
    """

    pass


class InvalidTypeError(BikramSambatError, TypeError):
    """Raised when a function argument receives an unexpected type.

    For example, this would be raised if an integer is expected for a year
    but a string is provided instead.

    Inherits from:
        TypeError: For compatibility with standard Python type checks.
        BikramSambatError: To be part of the package's exception hierarchy.
    """

    pass
