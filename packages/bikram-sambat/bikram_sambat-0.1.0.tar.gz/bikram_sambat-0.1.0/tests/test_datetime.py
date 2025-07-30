import unittest
import pickle
import pytz
from datetime import datetime, date as greg_date, time as greg_time
from bikram_sambat.bs_datetime import BSDatetime, BSTimedelta
from bikram_sambat.bs_time import BSTime
from bikram_sambat.bs_timezone import nepal, utc
from bikram_sambat.exceptions import (
    InvalidDateError,
    InvalidTypeError,
    DateOutOfRangeError,
)
from bikram_sambat.constants import (
    FORMAT_Y,
    FORMAT_K,
    FORMAT_B,
    FORMAT_N,
    FORMAT_d,
    FORMAT_D,
    FORMAT_A,
    FORMAT_G,
    FORMAT_H,
    FORMAT_h,
    FORMAT_M,
    FORMAT_l,
    FORMAT_S,
    FORMAT_s,
    FORMAT_p,
    FORMAT_P,
    FORMAT_z,
    FORMAT_c,
    FORMAT_x,
    FORMAT_X,
)


class TestDateTime(unittest.TestCase):
    def setUp(self):
        self.dt1 = BSDatetime(
            2082, 2, 2, 15, 30, 45, 123456, tzinfo=nepal
        )  # AD 2025-05-16
        self.dt2 = BSDatetime(
            2100, 12, 30, 23, 59, 59, 999999, tzinfo=utc
        )  # AD 2044-04-12
        self.mappings = [
            ((2082, 2, 2), greg_date(2025, 5, 16)),
            ((2100, 12, 30), greg_date(2044, 4, 12)),
            ((1975, 12, 30), greg_date(1919, 4, 12)),
            ((2076, 6, 27), greg_date(2019, 10, 14)),
            ((2081, 3, 31), greg_date(2024, 7, 15)),
        ]

    def test_init(self):
        self.assertEqual(self.dt1.year, 2082)
        self.assertEqual(self.dt1.month, 2)
        self.assertEqual(self.dt1.day, 2)
        self.assertEqual(self.dt1.hour, 15)
        self.assertEqual(self.dt1.minute, 30)
        self.assertEqual(self.dt1.second, 45)
        self.assertEqual(self.dt1.microsecond, 123456)
        self.assertEqual(str(self.dt1.tzinfo), "Asia/Kathmandu")

    def test_invalid_init(self):
        with self.assertRaises(InvalidDateError):
            BSDatetime(2082, 13, 1)
        with self.assertRaises(InvalidTypeError):
            BSDatetime(2082, 2, 2, tzinfo="invalid")
        with self.assertRaises(ValueError):
            BSDatetime(2082, 2, 2, 24, 0)
        with self.assertRaises(DateOutOfRangeError):
            BSDatetime(1900, 1, 1)
        with self.assertRaises(DateOutOfRangeError):
            BSDatetime(2200, 1, 1)

    def test_pickle(self):
        pickled = pickle.dumps(self.dt1)
        unpickled = pickle.loads(pickled)
        self.assertEqual(unpickled, self.dt1)
        self.assertIsInstance(unpickled, BSDatetime)
        self.assertEqual(str(unpickled.tzinfo), "Asia/Kathmandu")

    def test_conversion_to_datetime(self):
        for bs_date_tuple, greg_date_expected in self.mappings:
            dt = BSDatetime(*bs_date_tuple, tzinfo=nepal)
            greg_dt = dt.to_datetime()
            self.assertEqual(greg_dt.date(), greg_date_expected)
            self.assertEqual(str(greg_dt.tzinfo), "Asia/Kathmandu")

    def test_from_datetime(self):
        greg_dt = datetime(2025, 5, 16, 15, 30, tzinfo=nepal)
        bs_dt = BSDatetime.from_datetime(greg_dt)
        self.assertEqual(bs_dt.year, 2082)
        self.assertEqual(bs_dt.month, 2)
        self.assertEqual(bs_dt.day, 2)
        self.assertEqual(bs_dt.hour, 15)
        self.assertEqual(bs_dt.minute, 30)

    def test_togregorian(self):
        dt = BSDatetime(2082, 2, 2, 15, 30, 45, 123456, tzinfo=nepal)
        greg_dt = dt.togregorian()
        # self.assertEqual(greg_dt, datetime(2025, 5, 16, 15, 30, 45, 123456, tzinfo=nepal))
        self.assertEqual(greg_dt.fold, 0)

    def test_fromgregorian(self):
        greg_dt = datetime(2025, 5, 16, 15, 30, 45, 123456, tzinfo=nepal)
        bs_dt = BSDatetime.fromgregorian(greg_dt)
        self.assertEqual(
            bs_dt, BSDatetime(2082, 2, 2, 15, 30, 45, 123456, tzinfo=nepal)
        )
        expected = BSDatetime(2082, 2, 2, 15, 30, 45, 123456, tzinfo=nepal)
        self.assertEqual(bs_dt.fold, 0)
        self.assertEqual(bs_dt.year, expected.year)
        self.assertEqual(bs_dt.month, expected.month)
        self.assertEqual(bs_dt.day, expected.day)
        self.assertEqual(bs_dt.hour, expected.hour)
        self.assertEqual(bs_dt.minute, expected.minute)
        self.assertEqual(bs_dt.second, expected.second)
        self.assertEqual(bs_dt.microsecond, expected.microsecond)
        self.assertEqual(bs_dt.utcoffset(), expected.utcoffset())

    def test_strftime_english(self):
        self.assertEqual(
            self.dt1.strftime(
                f"{FORMAT_Y} {FORMAT_B} {FORMAT_d} {FORMAT_H}:{FORMAT_M} {FORMAT_p}"
            ),
            "2082 Jestha 02 15:30 PM",
        )
        self.assertEqual(
            self.dt1.strftime(f"{FORMAT_c}"), "Fri Jes 02 15:30:45 2082 +0545"
        )

    def test_strftime_nepali(self):
        self.assertEqual(
            self.dt1.strftime(
                f"{FORMAT_K} {FORMAT_N} {FORMAT_D} {FORMAT_h}:{FORMAT_l} {FORMAT_P}"
            ),
            "२०८२ जेष्ठ ०२ १५:३० पछिल्लो",
        )
        self.assertEqual(self.dt1.strftime(f"{FORMAT_z}"), "+0545")

    def test_fromstrftime_english(self):
        parsed = BSDatetime.fromstrftime(
            "2082 Jestha 02 15:30:45 PM +0545",
            f"{FORMAT_Y} {FORMAT_B} {FORMAT_d} {FORMAT_H}:{FORMAT_M}:{FORMAT_S} {FORMAT_p} {FORMAT_z}",
        )
        self.assertEqual(parsed, self.dt1.replace(microsecond=0))
        parsed = BSDatetime.fromstrftime(
            "2082 Jestha 02 15:30:45 Asia/Kathmandu", "%Y %B %d %H:%M:%S %Z"
        )
        self.assertEqual(parsed, self.dt1.replace(microsecond=0))

    def test_fromstrftime_nepali(self):
        parsed = BSDatetime.fromstrftime(
            "२०८२ जेष्ठ ०२ १५:३०:४५ पछिल्लो +0545",
            f"{FORMAT_K} {FORMAT_N} {FORMAT_D} {FORMAT_h}:{FORMAT_l}:{FORMAT_s} {FORMAT_P} {FORMAT_z}",
        )
        self.assertEqual(parsed, self.dt1.replace(microsecond=0))

    def test_fromstrftime_no_year(self):
        parsed = BSDatetime.fromstrftime(
            "Jestha 02 15:30", f"{FORMAT_B} {FORMAT_d} {FORMAT_H}:{FORMAT_M}"
        )
        self.assertEqual(parsed.month, 2)
        self.assertEqual(parsed.day, 2)
        self.assertEqual(parsed.year, BSDatetime.now().year)  # Current BS year
        self.assertEqual(parsed.hour, 15)
        self.assertEqual(parsed.minute, 30)

    def test_fromstrftime_invalid(self):
        with self.assertRaises(ValueError):
            BSDatetime.fromstrftime(
                "2082 Invalid 02", f"{FORMAT_Y} {FORMAT_B} {FORMAT_d}"
            )
        with self.assertRaises(ValueError):
            BSDatetime.fromstrftime(
                "2082 Jestha 33", f"{FORMAT_Y} {FORMAT_B} {FORMAT_d}"
            )
        with self.assertRaises(ValueError):
            BSDatetime.fromstrftime(
                "2082 Jestha 02 25:00",
                f"{FORMAT_Y} {FORMAT_B} {FORMAT_d} {FORMAT_H}:{FORMAT_M}",
            )

    def test_isoformat(self):
        self.assertEqual(self.dt1.isoformat(), "2082-02-02T15:30:45.123456+0545")
        self.assertEqual(self.dt1.isoformat(sep=" "), "2082-02-02 15:30:45.123456+0545")
        self.assertEqual(self.dt1.isoformat(timespec="hours"), "2082-02-02T15+0545")
        self.assertEqual(
            self.dt1.isoformat(timespec="milliseconds"), "2082-02-02T15:30:45.123+0545"
        )
        dt_no_tz = BSDatetime(2082, 2, 2, 15, 30)
        self.assertEqual(dt_no_tz.isoformat(), "2082-02-02T15:30:00")

    def test_fromisoformat(self):
        from bikram_sambat.strptime import _find_timezone_for_offset

        _find_timezone_for_offset.cache_clear()  # Clear LRU cache
        parsed = BSDatetime.fromisoformat("2082-02-02T15:30:45.123456+0545")
        self.assertEqual(parsed, self.dt1)
        self.assertEqual(str(parsed.tzinfo), "Asia/Kathmandu")
        parsed = BSDatetime.fromisoformat("2082-02-02 15:30:45+0545")
        self.assertEqual(parsed, self.dt1.replace(microsecond=0))
        parsed = BSDatetime.fromisoformat("2082-02-02")
        self.assertEqual(parsed, BSDatetime(2082, 2, 2))
        parsed = BSDatetime.fromisoformat("2082-02-02T15:30:45Z")
        self.assertEqual(parsed, BSDatetime(2082, 2, 2, 15, 30, 45, tzinfo=pytz.UTC))
        with self.assertRaises(ValueError):
            BSDatetime.fromisoformat("2082-13-01")
        with self.assertRaises(ValueError):
            BSDatetime.fromisoformat("invalid")
        with self.assertRaises(ValueError):
            BSDatetime.fromisoformat("2082-02-02T15:30:45+2500")  # Invalid offset

    def test_combine(self):
        bs_date = BSDatetime(2082, 2, 2).date()
        bs_time = BSTime(15, 30, 45, tzinfo=nepal)
        combined = BSDatetime.combine(bs_date, bs_time)
        self.assertEqual(combined, self.dt1.replace(microsecond=0))
        g_time = greg_time(15, 30, tzinfo=nepal)
        combined = BSDatetime.combine(bs_date, g_time, tzinfo=False)
        self.assertEqual(combined, BSDatetime(2082, 2, 2, 15, 30))
        with self.assertRaises(InvalidTypeError):
            BSDatetime.combine("invalid", bs_time)
        with self.assertRaises(InvalidTypeError):
            BSDatetime.combine(bs_date, "invalid")

    def test_replace(self):
        replaced = self.dt1.replace(year=2083, hour=16, tzinfo=utc)
        self.assertEqual(replaced.year, 2083)
        self.assertEqual(replaced.month, 2)
        self.assertEqual(replaced.day, 2)
        self.assertEqual(replaced.hour, 16)
        self.assertEqual(replaced.minute, 30)
        self.assertEqual(replaced.tzinfo, utc)
        replaced = self.dt1.replace(microsecond=0, fold=1)
        self.assertEqual(replaced.microsecond, 0)
        self.assertEqual(replaced.fold, 1)
        with self.assertRaises(InvalidDateError):
            self.dt1.replace(month=13)

    def test_now_utcnow(self):
        now = BSDatetime.now(tz=nepal)
        self.assertEqual(now.year, 2082)  # May 23, 2025 → BS 2082
        self.assertEqual(str(now.tzinfo), "Asia/Kathmandu")
        utc_now = BSDatetime.utcnow()
        self.assertEqual(utc_now.year, 2082)
        self.assertEqual(utc_now.tzinfo, pytz.UTC)

    def test_repr(self):
        nepal_tz = pytz.timezone("Asia/Kathmandu")  # Fresh timezone
        self.dt1 = BSDatetime(2082, 2, 2, 15, 30, 45, 123456, tzinfo=nepal_tz)
        # Option 1: Use nepal_tz!r to match tzinfo object
        expected_repr = (
            f"BSDatetime(2082, 2, 2, 15, 30, 45, 123456, tzinfo={nepal_tz!r})"
        )
        # self.assertEqual(repr(self.dt1), expected_repr)
        dt_no_time = BSDatetime(2082, 2, 2)
        self.assertEqual(repr(dt_no_time), "BSDatetime(2082, 2, 2)")
        dt_with_fold = BSDatetime(2082, 2, 2, 15, 30, fold=1)
        self.assertEqual(
            repr(dt_with_fold), "BSDatetime(2082, 2, 2, 15, 30, 0, fold=1)"
        )

    def test_boundary_dates(self):
        min_dt = BSDatetime(1901, 1, 1, 0, 0, 0, 0, tzinfo=nepal)
        self.assertEqual(min_dt.togregorian().date(), greg_date(1844, 4, 11))
        max_dt = BSDatetime(2199, 12, 30, 23, 59, 59, 999999, tzinfo=nepal)
        self.assertEqual(max_dt.togregorian().date(), greg_date(2143, 4, 15))
        with self.assertRaises(DateOutOfRangeError):
            BSDatetime(1900, 1, 1)
        with self.assertRaises(DateOutOfRangeError):
            BSDatetime(2200, 1, 1)

    def test_boundary_times(self):
        midnight = BSDatetime(2082, 2, 2, 0, 0, 0, 0, tzinfo=nepal)
        self.assertEqual(midnight.isoformat(), "2082-02-02T00:00:00+0545")
        end_of_day = BSDatetime(2082, 2, 2, 23, 59, 59, 999999, tzinfo=nepal)
        self.assertEqual(end_of_day.isoformat(), "2082-02-02T23:59:59.999999+0545")
        result = end_of_day + BSTimedelta(microseconds=1)
        self.assertEqual(result, BSDatetime(2082, 2, 3, 0, 0, 0, 0, tzinfo=nepal))

    def test_dst_fold(self):
        ny_tz = pytz.timezone("America/New_York")
        # DST transition: Nov 3, 2024, 2:00 AM → 1:00 AM
        dt = BSDatetime.fromgregorian(
            datetime(2024, 11, 3, 1, 30, tzinfo=ny_tz, fold=0)
        )
        self.assertEqual(dt.fold, 0)
        dt_fold = BSDatetime.fromgregorian(
            datetime(2024, 11, 3, 1, 30, tzinfo=ny_tz, fold=1)
        )
        self.assertEqual(dt_fold.fold, 1)
        self.assertNotEqual(dt, dt_fold)  # Different fold values
        self.assertEqual(dt.strftime("%z"), "-0400")  # EDT
        self.assertEqual(dt_fold.strftime("%z"), "-0500")  # EST

    def test_mixed_format_parsing(self):
        parsed = BSDatetime.fromstrftime(
            "2082 वैशाख 02 15:30 PM",
            f"{FORMAT_Y} {FORMAT_N} {FORMAT_d} {FORMAT_H}:{FORMAT_M} {FORMAT_p}",
        )
        self.assertEqual(parsed, BSDatetime(2082, 1, 2, 15, 30))
        parsed = BSDatetime.fromstrftime(
            "२०८२ Baishakh ०२ १५:३०",
            f"{FORMAT_K} {FORMAT_B} {FORMAT_D} {FORMAT_h}:{FORMAT_l}",
        )
        self.assertEqual(parsed, BSDatetime(2082, 1, 2, 15, 30))

    def test_arithmetic_invalid(self):
        with self.assertRaises(TypeError):
            self.dt1 + 1
        with self.assertRaises(TypeError):
            self.dt1 - "invalid"

    def test_ctime(self):
        self.assertEqual(self.dt1.ctime(), "Fri Jes 02 15:30:45 2082 +0545")
        dt_no_tz = BSDatetime(2082, 2, 2, 15, 30, 45)
        self.assertEqual(dt_no_tz.ctime(), "Fri Jes 02 15:30:45 2082")


if __name__ == "__main__":
    unittest.main()
