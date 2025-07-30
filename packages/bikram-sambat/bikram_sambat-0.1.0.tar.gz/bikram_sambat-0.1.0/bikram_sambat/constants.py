"""Defines constants used throughout the bikram_sambat package.

This module serves as a central repository for static data, including `strftime`
format directives, names for months and weekdays in both English and Nepali,
and mappings for converting between standard and Nepali numerals.

Attributes:
    FORMAT_* (str): A collection of `strftime`-style format codes used for
        parsing and formatting dates and times. Includes both standard codes
        (e.g., `%Y`, `%m`, `%d`) and custom BS-specific codes for Nepali
        numerals and names (e.g., `%K`, `%n`, `%D`, `%N`, `%G`).

    DATE_FORMAT_DIRECTIVES (list[str]): A list of all valid format codes
        for use with `BSDate.strftime`.
    TIME_FORMAT_DIRECTIVES (list[str]): A list of all valid format codes
        for use with `BSTime.strftime`.
    DATETIME_FORMAT_DIRECTIVES (list[str]): A list of all valid format codes
        for use with `BSDatetime.strftime`.

    NEPALI_DIGITS (dict[str, str]): A mapping from Nepali Unicode numerals
        (e.g., '९') to standard ASCII numerals (e.g., '9').
    STANDARD_DIGITS (dict[str, str]): A reverse mapping from standard ASCII
        numerals to Nepali Unicode numerals.

    MONTH_NAMES_FULL (list[str]): A list of the full English names of the
        12 months in the Bikram Sambat calendar (e.g., "Baishakh").
    MONTH_NAMES_SHORT (list[str]): A list of the 3-letter abbreviated
        English month names (e.g., "Bai").
    MONTH_NAMES_FULL_NEPALI (list[str]): A list of the full Nepali Unicode
        names of the 12 months (e.g., "वैशाख").

    WEEKDAY_NAMES_FULL (list[str]): A list of the full English names of the
        weekdays, starting with Sunday.
    WEEKDAY_NAMES_SHORT (list[str]): A list of the 3-letter abbreviated
        English weekday names (e.g., "Sun").
    WEEKDAY_NAMES_FULL_NEPALI (list[str]): A list of the full Nepali Unicode
        names of the weekdays (e.g., "आइतबार").

    AM_PM_ENGLISH (list[str]): A list containing the English AM/PM designators
        ["AM", "PM"].
    AM_PM_NEPALI (list[str]): A list containing the Nepali AM/PM designators
        ["पहिले", "पछिल्लो"].
"""

# Format directives
FORMAT_A = "%A"  # Full weekday name (e.g., Sunday)
FORMAT_a = "%a"  # Abbreviated weekday name (e.g., Sun)
FORMAT_G = "%G"  # Full weekday name in Nepali Unicode (e.g., आइतबार)
FORMAT_w = "%w"  # Weekday number (0=Sunday, 6=Saturday)
FORMAT_d = "%d"  # Day of month (e.g., 15)
FORMAT_D = "%D"  # Day of month in Nepali Unicode (e.g., १५)
FORMAT_b = "%b"  # Abbreviated month name (e.g., Bai)
FORMAT_B = "%B"  # Full month name (e.g., Baishakh)
FORMAT_N = "%N"  # Full month name in Nepali Unicode (e.g., वैशाख)
FORMAT_m = "%m"  # Month number (e.g., 05)
FORMAT_n = "%n"  # Month number in Nepali Unicode (e.g., ०५)
FORMAT_y = "%y"  # Year without century (e.g., 82)
FORMAT_k = "%k"  # Year without century in Nepali Unicode (e.g., ८२)
FORMAT_Y = "%Y"  # Year with century (e.g., 2082)
FORMAT_K = "%K"  # Year with century in Nepali Unicode (e.g., २०८२)
FORMAT_H = "%H"  # Hour (24-hour, e.g., 15)
FORMAT_h = "%h"  # Hour (24-hour, Nepali Unicode, e.g., १५)
FORMAT_I = "%I"  # Hour (12-hour, e.g., 03)
FORMAT_i = "%i"  # Hour (12-hour, Nepali Unicode, e.g., ०३)
FORMAT_p = "%p"  # AM/PM (e.g., AM, PM)
FORMAT_P = "%P"  # AM/PM in Nepali Unicode (e.g., पहिले, पछिल्लो)
FORMAT_M = "%M"  # Minute (e.g., 30)
FORMAT_l = "%l"  # Minute in Nepali Unicode (e.g., ३०)
FORMAT_S = "%S"  # Second (e.g., 45)
FORMAT_s = "%s"  # Second in Nepali Unicode (e.g., ४५)
FORMAT_f = "%f"  # Microsecond (e.g., 123456)
FORMAT_t = "%t"  # Microsecond in Nepali Unicode (e.g., १२३४५६)
FORMAT_z = "%z"  # UTC offset (e.g., +0545)
FORMAT_Z = "%Z"  # Timezone name (e.g., Asia/Kathmandu)
FORMAT_j = "%j"  # Day of year (e.g., 165)
FORMAT_J = "%J"  # Day of year in Nepali Unicode (e.g., १६५)
FORMAT_U = "%U"  # Week number (Sunday-based, e.g., 23)
FORMAT_c = "%c"  # Standard datetime format (e.g., Sun Bai 15 15:30:45 2082)
FORMAT_x = "%x"  # Standard date format (e.g., 2082-05-15)
FORMAT_X = "%X"  # Standard time format (e.g., 15:30:45)


# List of valid format directives for each type
DATE_FORMAT_DIRECTIVES = [
    FORMAT_Y,  # Year with century (e.g., 2082)
    FORMAT_K,  # Year with century, Nepali Unicode (e.g., २०८२)
    FORMAT_y,  # Year without century (e.g., 82)
    FORMAT_k,  # Year without century, Nepali Unicode (e.g., ८२)
    FORMAT_m,  # Month number (e.g., 05)
    FORMAT_n,  # Month number, Nepali Unicode (e.g., ०५)
    FORMAT_d,  # Day of month (e.g., 15)
    FORMAT_D,  # Day of month, Nepali Unicode (e.g., १५)
    FORMAT_B,  # Full month name, English (e.g., Baishakh)
    FORMAT_N,  # Full month name, Nepali Unicode (e.g., वैशाख)
    FORMAT_b,  # Abbreviated month name, English (e.g., Bai)
    FORMAT_c,  # Standard datetime format (e.g., Sun Bai 15 15:30:45 2082)
    FORMAT_A,  # Full weekday name, English (e.g., Sunday)
    FORMAT_G,  # Full weekday name, Nepali Unicode (e.g., आइतबार)
    FORMAT_a,  # Abbreviated weekday name, English (e.g., Sun)
    FORMAT_w,  # Weekday number (0=Sunday, 6=Saturday)
    FORMAT_j,  # Day of year (e.g., 165)
    FORMAT_J,  # Day of year, Nepali Unicode (e.g., १६५)
    FORMAT_U,  # Week number, Sunday-based (e.g., 23)
    FORMAT_x,  # Standard date format (e.g., 2082-05-15)
    "%%",  # Literal %
]

TIME_FORMAT_DIRECTIVES = [
    FORMAT_H,  # Hour, 24-hour (e.g., 15)
    FORMAT_h,  # Hour, 24-hour, Nepali Unicode (e.g., १५)
    FORMAT_I,  # Hour, 12-hour (e.g., 03)
    FORMAT_i,  # Hour, 12-hour, Nepali Unicode (e.g., ०३)
    FORMAT_M,  # Minute (e.g., 30)
    FORMAT_l,  # Minute, Nepali Unicode (e.g., ३०)
    FORMAT_S,  # Second (e.g., 45)
    FORMAT_s,  # Second, Nepali Unicode (e.g., ४५)
    FORMAT_f,  # Microsecond (e.g., 123456)
    FORMAT_t,  # Microsecond, Nepali Unicode (e.g., १२३४५६)
    FORMAT_p,  # AM/PM, English (e.g., PM)
    FORMAT_P,  # AM/PM, Nepali Unicode (e.g., पछिल्लो)
    FORMAT_z,  # UTC offset (e.g., +0545)
    FORMAT_Z,  # Timezone name (e.g., Asia/Kathmandu)
    FORMAT_X,  # Standard time format (e.g., 15:30:45)
    "%%",  # Literal %
]

DATETIME_FORMAT_DIRECTIVES = [
    FORMAT_Y,  # Year with century (e.g., 2082)
    FORMAT_K,  # Year with century, Nepali Unicode (e.g., २०८२)
    FORMAT_y,  # Year without century (e.g., 82)
    FORMAT_k,  # Year without century, Nepali Unicode (e.g., ८२)
    FORMAT_m,  # Month number (e.g., 05)
    FORMAT_n,  # Month number, Nepali Unicode (e.g., ०५)
    FORMAT_d,  # Day of month (e.g., 15)
    FORMAT_D,  # Day of month, Nepali Unicode (e.g., १५)
    FORMAT_B,  # Full month name, English (e.g., Baishakh)
    FORMAT_N,  # Full month name, Nepali Unicode (e.g., वैशाख)
    FORMAT_b,  # Abbreviated month name, English (e.g., Bai)
    FORMAT_A,  # Full weekday name, English (e.g., Sunday)
    FORMAT_G,  # Full weekday name, Nepali Unicode (e.g., आइतबार)
    FORMAT_a,  # Abbreviated weekday name, English (e.g., Sun)
    FORMAT_w,  # Weekday number (0=Sunday, 6=Saturday)
    FORMAT_j,  # Day of year (e.g., 165)
    FORMAT_J,  # Day of year, Nepali Unicode (e.g., १६५)
    FORMAT_U,  # Week number, Sunday-based (e.g., 23)
    FORMAT_H,  # Hour, 24-hour (e.g., 15)
    FORMAT_h,  # Hour, 24-hour, Nepali Unicode (e.g., १५)
    FORMAT_I,  # Hour, 12-hour (e.g., 03)
    FORMAT_i,  # Hour, 12-hour, Nepali Unicode (e.g., ०३)
    FORMAT_M,  # Minute (e.g., 30)
    FORMAT_l,  # Minute, Nepali Unicode (e.g., ३०)
    FORMAT_S,  # Second (e.g., 45)
    FORMAT_s,  # Second, Nepali Unicode (e.g., ४५)
    FORMAT_f,  # Microsecond (e.g., 123456)
    FORMAT_t,  # Microsecond, Nepali Unicode (e.g., १२३४५६)
    FORMAT_p,  # AM/PM, English (e.g., PM)
    FORMAT_P,  # AM/PM, Nepali Unicode (e.g., पछिल्लो)
    FORMAT_z,  # UTC offset (e.g., +0545)
    FORMAT_Z,  # Timezone name (e.g., Asia/Kathmandu)
    FORMAT_X,  # Standard time format (e.g., 15:30:45)
    FORMAT_x,  # Standard date format (e.g., 2082-05-15)
    FORMAT_c,  # Standard datetime format (e.g., Sun Bai 15 15:30:45 2082)
    "%%",  # Literal %
]
# Nepali digits mapping
NEPALI_DIGITS = {
    "०": "0",
    "१": "1",
    "२": "2",
    "३": "3",
    "४": "4",
    "५": "5",
    "६": "6",
    "७": "7",
    "८": "8",
    "९": "9",
}
STANDARD_DIGITS = {v: k for k, v in NEPALI_DIGITS.items()}

# Month names (English default)
MONTH_BAISHAKH = "Baishakh"
MONTH_JESTHA = "Jestha"
MONTH_ASHADH = "Ashadh"
MONTH_SHRAWAN = "Shrawan"
MONTH_BHADRA = "Bhadra"
MONTH_ASHWIN = "Ashwin"
MONTH_KARTIK = "Kartik"
MONTH_MANGSIR = "Mangsir"
MONTH_POUSH = "Poush"
MONTH_MAGH = "Magh"
MONTH_FALGUN = "Falgun"
MONTH_CHAITRA = "Chaitra"

MONTH_NAMES_FULL = [
    MONTH_BAISHAKH,
    MONTH_JESTHA,
    MONTH_ASHADH,
    MONTH_SHRAWAN,
    MONTH_BHADRA,
    MONTH_ASHWIN,
    MONTH_KARTIK,
    MONTH_MANGSIR,
    MONTH_POUSH,
    MONTH_MAGH,
    MONTH_FALGUN,
    MONTH_CHAITRA,
]
MONTH_NAMES_SHORT = [name[:3] for name in MONTH_NAMES_FULL]

# Month names (Nepali Unicode)
MONTH_BAISHAKH_NEPALI = "वैशाख"
MONTH_JESTHA_NEPALI = "जेष्ठ"
MONTH_ASHADH_NEPALI = "असार"
MONTH_SHRAWAN_NEPALI = "श्रावण"
MONTH_BHADRA_NEPALI = "भदौ"
MONTH_ASHWIN_NEPALI = "आश्विन"
MONTH_KARTIK_NEPALI = "कार्तिक"
MONTH_MANGSIR_NEPALI = "मंसिर"
MONTH_POUSH_NEPALI = "पौष"
MONTH_MAGH_NEPALI = "माघ"
MONTH_FALGUN_NEPALI = "फाल्गुण"
MONTH_CHAITRA_NEPALI = "चैत्र"

MONTH_NAMES_FULL_NEPALI = [
    MONTH_BAISHAKH_NEPALI,
    MONTH_JESTHA_NEPALI,
    MONTH_ASHADH_NEPALI,
    MONTH_SHRAWAN_NEPALI,
    MONTH_BHADRA_NEPALI,
    MONTH_ASHWIN_NEPALI,
    MONTH_KARTIK_NEPALI,
    MONTH_MANGSIR_NEPALI,
    MONTH_POUSH_NEPALI,
    MONTH_MAGH_NEPALI,
    MONTH_FALGUN_NEPALI,
    MONTH_CHAITRA_NEPALI,
]
MONTH_NAMES_SHORT_NEPALI = [name[:3] for name in MONTH_NAMES_FULL_NEPALI]

# Weekday names (English default)
WEEKDAY_SUNDAY = "Sunday"
WEEKDAY_MONDAY = "Monday"
WEEKDAY_TUESDAY = "Tuesday"
WEEKDAY_WEDNESDAY = "Wednesday"
WEEKDAY_THURSDAY = "Thursday"
WEEKDAY_FRIDAY = "Friday"
WEEKDAY_SATURDAY = "Saturday"

WEEKDAY_NAMES_FULL = [
    WEEKDAY_SUNDAY,
    WEEKDAY_MONDAY,
    WEEKDAY_TUESDAY,
    WEEKDAY_WEDNESDAY,
    WEEKDAY_THURSDAY,
    WEEKDAY_FRIDAY,
    WEEKDAY_SATURDAY,
]
WEEKDAY_NAMES_SHORT = [name[:3] for name in WEEKDAY_NAMES_FULL]

# Weekday names (Nepali Unicode)
WEEKDAY_SUNDAY_NEPALI = "आइतबार"
WEEKDAY_MONDAY_NEPALI = "सोमबार"
WEEKDAY_TUESDAY_NEPALI = "मंगलवार"
WEEKDAY_WEDNESDAY_NEPALI = "बुधबार"
WEEKDAY_THURSDAY_NEPALI = "बिहीबार"
WEEKDAY_FRIDAY_NEPALI = "शुक्रबार"
WEEKDAY_SATURDAY_NEPALI = "शनिबार"

WEEKDAY_NAMES_FULL_NEPALI = [
    WEEKDAY_SUNDAY_NEPALI,
    WEEKDAY_MONDAY_NEPALI,
    WEEKDAY_TUESDAY_NEPALI,
    WEEKDAY_WEDNESDAY_NEPALI,
    WEEKDAY_THURSDAY_NEPALI,
    WEEKDAY_FRIDAY_NEPALI,
    WEEKDAY_SATURDAY_NEPALI,
]
WEEKDAY_NAMES_SHORT_NEPALI = [name[:3] for name in WEEKDAY_NAMES_FULL_NEPALI]

# AM/PM
AM_ENGLISH = "AM"
PM_ENGLISH = "PM"
AM_NEPALI = "पहिले"
PM_NEPALI = "पछिल्लो"
AM_PM_ENGLISH = [AM_ENGLISH, PM_ENGLISH]
AM_PM_NEPALI = [AM_NEPALI, PM_NEPALI]
