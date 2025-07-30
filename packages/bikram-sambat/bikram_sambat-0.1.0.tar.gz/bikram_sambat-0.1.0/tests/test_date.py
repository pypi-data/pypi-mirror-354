import unittest
import pickle
from datetime import date as greg_date, timedelta as greg_timedelta
from bikram_sambat.bs_date import BSDate
from bikram_sambat.bs_timedelta import BSTimedelta
from bikram_sambat.exceptions import (
    InvalidDateError,
    DateOutOfRangeError,
    InvalidTypeError,
)
from bikram_sambat.constants import (
    FORMAT_Y,
    FORMAT_K,
    FORMAT_y,
    FORMAT_k,
    FORMAT_m,
    FORMAT_n,
    FORMAT_d,
    FORMAT_D,
    FORMAT_B,
    FORMAT_N,
    FORMAT_b,
    FORMAT_A,
    FORMAT_G,
    FORMAT_a,
    FORMAT_w,
    FORMAT_j,
    FORMAT_J,
    FORMAT_U,
    FORMAT_c,
    FORMAT_x,
    DATE_FORMAT_DIRECTIVES,
)


class TestBSDate(unittest.TestCase):
    def setUp(self):
        # Sample dates from provided mappings
        self.bs_date = BSDate(2082, 2, 2)  # AD 2025-05-16, Friday (weekday=6)
        self.edge_min = BSDate(1901, 1, 1)  # AD 1844-04-11
        self.edge_max = BSDate(2199, 12, 30)  # AD 2143-04-12
        self.transition_date = BSDate(2082, 12, 30)  # AD 2026-04-13
        # BS ↔ AD mappings
        self.mappings = [
            ((2082, 2, 2), greg_date(2025, 5, 16)),
            ((2100, 12, 30), greg_date(2044, 4, 12)),
            ((1975, 12, 30), greg_date(1919, 4, 12)),
            ((2076, 6, 27), greg_date(2019, 10, 14)),
            ((2081, 3, 31), greg_date(2024, 7, 15)),
        ]

    def test_init(self):
        self.assertEqual(self.bs_date.year, 2082)
        self.assertEqual(self.bs_date.month, 2)
        self.assertEqual(self.bs_date.day, 2)

    def test_invalid_init(self):
        with self.assertRaises(InvalidDateError):
            BSDate(2082, 13, 1)  # Invalid month
        with self.assertRaises(InvalidDateError):
            BSDate(2082, 2, 33)  # Invalid day
        with self.assertRaises(DateOutOfRangeError):
            BSDate(1900, 1, 1)  # Below MINYEAR
        with self.assertRaises(DateOutOfRangeError):
            BSDate(2200, 1, 1)  # Above MAXYEAR
        with self.assertRaises(InvalidTypeError):
            BSDate("2082", 2, 2)  # Non-integer

    def test_conversion_to_gregorian(self):
        for bs_date_tuple, greg_date_expected in self.mappings:
            bs_date = BSDate(*bs_date_tuple)
            self.assertEqual(bs_date.togregorian(), greg_date_expected)

    def test_conversion_from_gregorian(self):
        for bs_date_tuple, greg_date_input in self.mappings:
            bs_date = BSDate.fromgregorian(greg_date_input)
            self.assertEqual((bs_date.year, bs_date.month, bs_date.day), bs_date_tuple)

    def test_fromgregorian_same_instance(self):
        # Test that fromgregorian returns same BSDate instance
        bs_date = BSDate(2082, 2, 2)
        result = BSDate.fromgregorian(bs_date)
        self.assertIs(result, bs_date)

    def test_fromgregorian_invalid_type(self):
        with self.assertRaises(InvalidTypeError):
            BSDate.fromgregorian("2025-05-16")  # Non-date input

    def test_today(self):
        today = BSDate.today()
        greg_today = greg_date.today()
        bs_y, bs_m, bs_d = (
            BSDate.fromgregorian(greg_today).year,
            BSDate.fromgregorian(greg_today).month,
            BSDate.fromgregorian(greg_today).day,
        )
        self.assertEqual(today.year, bs_y)
        self.assertEqual(today.month, bs_m)
        self.assertEqual(today.day, bs_d)

    def test_fromisoformat(self):
        bs_date = BSDate.fromisoformat("2082-02-02")
        self.assertEqual(bs_date, BSDate(2082, 2, 2))
        bs_date = BSDate.fromisoformat("1901-01-01")
        self.assertEqual(bs_date, BSDate(1901, 1, 1))

    def test_fromisoformat_invalid(self):
        with self.assertRaises(ValueError):
            BSDate.fromisoformat("2082-13-01")  # Invalid month
        with self.assertRaises(ValueError):
            BSDate.fromisoformat("2082-02")  # Incomplete format
        with self.assertRaises(InvalidTypeError):
            BSDate.fromisoformat(20820202)  # Non-string
        with self.assertRaises(ValueError):
            BSDate.fromisoformat("2082-02-abc")  # Non-numeric day

    def test_replace(self):
        bs_date = BSDate(2082, 2, 2)
        replaced = bs_date.replace(year=2083)
        self.assertEqual(replaced, BSDate(2083, 2, 2))
        replaced = bs_date.replace(month=3, day=15)
        self.assertEqual(replaced, BSDate(2082, 3, 15))

    def test_replace_invalid(self):
        bs_date = BSDate(2082, 2, 2)
        with self.assertRaises(InvalidDateError):
            bs_date.replace(month=13)  # Invalid month
        with self.assertRaises(InvalidTypeError):
            bs_date.replace(year="2083")  # Non-integer
        with self.assertRaises(DateOutOfRangeError):
            bs_date.replace(year=2200)  # Out of range

    def test_weekday(self):
        # BS 2082-02-02 = AD 2025-05-16 = Friday (BS weekday=6, Aaitabar=0)
        self.assertEqual(self.bs_date.weekday(), 5)  # Friday
        self.assertEqual(BSDate(2082, 2, 3).weekday(), 6)  # Saturday → Aaitabar
        self.assertEqual(BSDate(2082, 2, 4).weekday(), 0)  # Sunday

    def test_isoweekday(self):
        self.assertEqual(self.bs_date.isoweekday(), 6)  # Friday (weekday=6 + 1)
        self.assertEqual(BSDate(2082, 2, 3).isoweekday(), 7)  # Aaitabar
        self.assertEqual(BSDate(2082, 2, 4).isoweekday(), 1)  # Sunday

    def test_ctime(self):
        # Expected: "Fri Jes  2 00:00:00 2082"
        self.assertEqual(self.bs_date.ctime(), "Fri Jes  2 00:00:00 2082")
        self.assertEqual(self.edge_min.ctime(), "Thu Bai  1 00:00:00 1901")

    def test_strftime_all_directives(self):
        # Test all DATE_FORMAT_DIRECTIVES
        bs_date = BSDate(2082, 2, 2)  # Jestha 02, Friday
        expected = {
            FORMAT_Y: "2082",
            FORMAT_K: "२०८२",
            FORMAT_y: "82",
            FORMAT_k: "८२",
            FORMAT_m: "02",
            FORMAT_n: "०२",
            FORMAT_d: "02",
            FORMAT_D: "०२",
            FORMAT_B: "Jestha",
            FORMAT_N: "जेष्ठ",
            FORMAT_b: "Jes",
            FORMAT_A: "Friday",
            FORMAT_G: "शुक्रबार",
            FORMAT_a: "Fri",
            FORMAT_w: "5",
            FORMAT_j: "033",  # Day of year (Jestha 02)
            FORMAT_J: "०३३",
            FORMAT_U: "05",  # Week number
            FORMAT_x: "2082-02-02",
            FORMAT_x: "2082-02-02",
            FORMAT_c: "Fri Jes 02 00:00:00 2082",
            "%%": "%",
        }
        for directive in DATE_FORMAT_DIRECTIVES:
            result = bs_date.strftime(directive)
            self.assertEqual(result, expected[directive], f"Failed for {directive}")

    def test_strftime_composite(self):
        # Test composite formats
        self.assertEqual(
            self.bs_date.strftime(f"{FORMAT_Y}-{FORMAT_m}-{FORMAT_d} {FORMAT_A}"),
            "2082-02-02 Friday",
        )
        self.assertEqual(
            self.bs_date.strftime(f"{FORMAT_K}-{FORMAT_n}-{FORMAT_D} {FORMAT_G}"),
            "२०८२-०२-०२ शुक्रबार",
        )
        self.assertEqual(
            self.bs_date.strftime(f"{FORMAT_c}"), "Fri Jes 02 00:00:00 2082"
        )

    def test_strftime_edge_cases(self):
        # Test first and last day of year
        first_day = BSDate(2082, 1, 1)
        last_day = BSDate(2082, 12, 30)
        self.assertEqual(first_day.strftime(f"{FORMAT_j}"), "001")
        self.assertEqual(last_day.strftime(f"{FORMAT_j}"), "365")
        self.assertEqual(first_day.strftime(f"{FORMAT_U}"), "01")
        self.assertEqual(last_day.strftime(f"{FORMAT_U}"), "53")

    def test_strftime_invalid_format(self):
        with self.assertRaises(ValueError):
            self.bs_date.strftime("%H")  # Time directive

        with self.assertRaises(ValueError):
            self.bs_date.strftime("%Q")  # Unsupported directive
        # Test consecutive %%
        self.assertEqual(self.bs_date.strftime("%%"), "%")
        self.assertEqual(self.bs_date.strftime("%%%%"), "%%")

    def test_fromstrftime_english(self):
        parsed = BSDate.fromstrftime(
            "2082 Jestha 02", f"{FORMAT_Y} {FORMAT_B} {FORMAT_d}"
        )
        self.assertEqual(parsed, BSDate(2082, 2, 2))
        # parsed = BSDate.fromstrftime("Friday", f"{FORMAT_A}")
        self.assertEqual(parsed.weekday(), 5)  # Friday
        parsed = BSDate.fromstrftime("2082-02-02", f"{FORMAT_x}")
        self.assertEqual(parsed, BSDate(2082, 2, 2))

    def test_fromstrftime_nepali(self):
        parsed = BSDate.fromstrftime("२०८२ जेष्ठ ०२", f"{FORMAT_K} {FORMAT_N} {FORMAT_D}")
        self.assertEqual(parsed, BSDate(2082, 2, 2))
        # parsed = BSDate.fromstrftime("शुक्रबार", f"{FORMAT_G}")
        self.assertEqual(parsed.weekday(), 5)  # Friday
        parsed = BSDate.fromstrftime("२०८२ ०३३", f"{FORMAT_K} {FORMAT_J}")
        self.assertEqual(parsed, BSDate(2082, 2, 2))

    def test_fromstrftime_invalid(self):
        with self.assertRaises(ValueError):
            BSDate.fromstrftime(
                "2082-13-01", f"{FORMAT_Y}-{FORMAT_m}-{FORMAT_d}"
            )  # Invalid month
        with self.assertRaises(ValueError):
            BSDate.fromstrftime("Jestha", f"{FORMAT_B}")  # Ambiguous without year/day
        with self.assertRaises(ValueError):
            BSDate.fromstrftime(
                "१२३४ जेष्ठ ०२", f"{FORMAT_K} {FORMAT_N} {FORMAT_D}"
            )  # Invalid year
        with self.assertRaises(ValueError):
            BSDate.fromstrftime(
                "2082 abc 02", f"{FORMAT_Y} {FORMAT_B} {FORMAT_d}"
            )  # Invalid month name

    def test_arithmetic_bstimedelta(self):
        bs_date = BSDate(2082, 2, 2)
        delta = BSTimedelta(days=1)
        next_day = bs_date + delta
        self.assertEqual(next_day, BSDate(2082, 2, 3))
        prev_day = bs_date - delta
        self.assertEqual(prev_day, BSDate(2082, 2, 1))
        diff = BSDate(2082, 2, 3) - BSDate(2082, 2, 1)
        self.assertEqual(diff, BSTimedelta(days=2))

    def test_arithmetic_invalid(self):
        bs_date = BSDate(2082, 2, 2)
        with self.assertRaises(TypeError):
            bs_date + 1  # Non-timedelta
        with self.assertRaises(TypeError):
            bs_date - "2082-02-01"  # Non-date/timedelta

    def test_ordinal_edge_cases(self):
        # Test min and max ordinals
        min_ordinal = self.edge_min.bs_toordinal()
        max_ordinal = self.edge_max.bs_toordinal()
        self.assertEqual(BSDate.bs_fromordinal(min_ordinal), self.edge_min)
        self.assertEqual(BSDate.bs_fromordinal(max_ordinal), self.edge_max)
        with self.assertRaises(InvalidTypeError):
            BSDate.bs_fromordinal("1")  # Non-integer
        with self.assertRaises(DateOutOfRangeError):
            BSDate.bs_fromordinal(0)  # Invalid ordinal

    def test_inherited_methods(self):
        # Test inherited datetime.date methods returning Gregorian values
        self.assertEqual(
            self.bs_date.togregorian().timetuple(), greg_date(2025, 5, 16).timetuple()
        )
        self.assertEqual(
            self.bs_date.togregorian().isocalendar(),
            greg_date(2025, 5, 16).isocalendar(),
        )

    def test_str_and_repr(self):
        self.assertEqual(str(self.bs_date), "2082-02-02")
        self.assertEqual(repr(self.bs_date), "bikram_sambat.bs_date.BSDate(2082, 2, 2)")
        self.assertEqual(self.bs_date.isoformat(), "2082-02-02")

    def test_month_boundary(self):
        # Test transition across month boundary
        last_day = BSDate(2082, 1, 31)  # Baishakh 31
        next_day = last_day + greg_timedelta(days=1)
        self.assertEqual(next_day, BSDate(2082, 2, 1))  # Jestha 01
        self.assertEqual(next_day.togregorian(), greg_date(2025, 5, 15))

    def test_year_boundary(self):
        # Test transition across year boundary
        last_day = BSDate(2082, 12, 30)
        next_day = last_day + greg_timedelta(days=1)
        self.assertEqual(next_day, BSDate(2083, 1, 1))
        self.assertEqual(next_day.togregorian(), greg_date(2026, 4, 14))


if __name__ == "__main__":
    unittest.main()
