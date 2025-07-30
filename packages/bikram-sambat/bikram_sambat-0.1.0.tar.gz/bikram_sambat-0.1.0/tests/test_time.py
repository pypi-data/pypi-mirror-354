import unittest
import pickle
import pytz
from datetime import timedelta
from bikram_sambat.bs_time import BSTime
from bikram_sambat.bs_timezone import nepal, utc, india
from bikram_sambat.exceptions import InvalidTypeError
from bikram_sambat.constants import (
    FORMAT_H,
    FORMAT_h,
    FORMAT_M,
    FORMAT_l,
    FORMAT_S,
    FORMAT_s,
    FORMAT_p,
    FORMAT_P,
    FORMAT_I,
    FORMAT_i,
    FORMAT_f,
    FORMAT_t,
    FORMAT_z,
    FORMAT_X,
)


class TestBSTime(unittest.TestCase):
    def setUp(self):
        self.t1 = BSTime(14, 30)  # 14:30:00
        self.t2 = BSTime(14, 30, 45, 123456, tzinfo=nepal)  # 14:30:45.123456
        self.t3 = BSTime(23, 59, 59, 999999, tzinfo=india, fold=1)  # 23:59:59.999999
        self.t4 = BSTime(0, 0, 0, 0, tzinfo=nepal)  # 00:00:00
        self.t5 = BSTime(23, 59, 59, 999999, tzinfo=nepal, fold=1)  # 23:59:59.999999

    def test_init(self):
        self.assertEqual(self.t1.hour, 14)
        self.assertEqual(self.t1.minute, 30)
        self.assertEqual(self.t1.second, 0)
        self.assertEqual(self.t1.microsecond, 0)
        self.assertIsNone(self.t1.tzinfo)
        self.assertEqual(self.t1.fold, 0)
        self.assertEqual(self.t2.second, 45)
        self.assertEqual(self.t2.microsecond, 123456)
        self.assertEqual(self.t2.tzinfo, nepal)
        self.assertEqual(self.t3.fold, 1)
        # self.assertEqual(self.t3.tzinfo, repr(self.t3.tzinfo))

    def test_invalid_init(self):
        with self.assertRaises(TypeError):
            BSTime("14", 30)
        with self.assertRaises(InvalidTypeError):
            BSTime(14, 30, tzinfo="invalid")
        with self.assertRaises(ValueError):
            BSTime(24, 0)
        with self.assertRaises(ValueError):
            BSTime(14, 60)
        with self.assertRaises(ValueError):
            BSTime(14, 30, 60)
        with self.assertRaises(ValueError):
            BSTime(14, 30, 0, 1000000)
        with self.assertRaises(ValueError):
            BSTime(14, 30, fold=2)

    def test_strftime_english(self):
        self.assertEqual(
            self.t2.strftime(f"{FORMAT_H}:{FORMAT_M}:{FORMAT_S} {FORMAT_p}"),
            "14:30:45 PM",
        )
        self.assertEqual(self.t2.strftime(f"{FORMAT_X}"), "14:30:45")
        self.assertEqual(self.t2.strftime(f"{FORMAT_z}"), "+0545")

    def test_strftime_nepali(self):
        self.assertEqual(
            self.t2.strftime(f"{FORMAT_h}:{FORMAT_l}:{FORMAT_s} {FORMAT_P}"),
            "१४:३०:४५ पछिल्लो",
        )

        self.assertEqual(self.t2.strftime(f"{FORMAT_t}"), "१२३४५६")

    def test_fromstrftime_english(self):
        parsed = BSTime.fromstrftime(
            "14:30:45 PM +0545",
            f"{FORMAT_H}:{FORMAT_M}:{FORMAT_S} {FORMAT_p} {FORMAT_z}",
        )
        self.assertEqual(parsed.hour, 14)
        self.assertEqual(parsed.minute, 30)
        self.assertEqual(parsed.second, 45)
        from datetime import timezone as dt_timezone

        self.assertIsInstance(parsed.tzinfo, dt_timezone)

    def test_fromstrftime_nepali(self):
        parsed = BSTime.fromstrftime(
            "१४:३०:४५ पछिल्लो +0545",
            f"{FORMAT_h}:{FORMAT_l}:{FORMAT_s} {FORMAT_P} {FORMAT_z}",
        )
        self.assertEqual(parsed.hour, 14)
        self.assertEqual(parsed.minute, 30)
        self.assertEqual(parsed.second, 45)
        self.assertEqual(parsed.utcoffset(), timedelta(hours=5, minutes=45))

        from datetime import timezone as dt_timezone  # python's native timezone

        self.assertIsInstance(parsed.tzinfo, dt_timezone)

    def test_timezone_transition(self):
        ny_tz = pytz.timezone("America/New_York")
        t_ny = BSTime(14, 30, tzinfo=ny_tz)
        self.assertEqual(t_ny.strftime(f"{FORMAT_z}"), "-0400")  # EDT
        t_nepal = t_ny.replace(tzinfo=nepal)
        self.assertEqual(t_nepal.strftime(f"{FORMAT_z}"), "+0545")

    def test_inherited_methods(self):
        self.assertEqual(self.t1.isoformat(), "14:30:00")
        self.assertEqual(self.t2.isoformat(timespec="milliseconds"), "14:30:45.123")
        self.assertEqual(self.t3.isoformat(), "23:59:59.999999")
        new_time = self.t1.replace(hour=15, minute=45)
        self.assertEqual(new_time, BSTime(15, 45))

    def test_comparison(self):
        self.assertEqual(self.t1, BSTime(14, 30))
        self.assertLess(self.t1, self.t2)
        self.assertLess(self.t2, self.t5)
        self.assertGreater(self.t3, self.t1)
        self.assertLessEqual(self.t1, self.t1)
        self.assertGreaterEqual(self.t3, self.t3)

    def test_repr(self):
        t0_default = BSTime()
        self.assertEqual(repr(t0_default), "bikram_sambat.bs_time.BSTime(0, 0)")
        self.assertEqual(repr(self.t1), "bikram_sambat.bs_time.BSTime(14, 30)")
        self.assertEqual(
            repr(self.t2),
            f"{BSTime.__module__}.BSTime(14, 30, 45, 123456, tzinfo={repr(self.t2.tzinfo)})",
        )
        self.assertEqual(
            repr(self.t3),
            f"{BSTime.__module__}.BSTime(23, 59, 59, 999999, tzinfo={repr(self.t3.tzinfo)}, fold=1)",
        )

    def test_str(self):
        self.assertEqual(str(self.t1), "14:30:00")
        self.assertEqual(str(self.t2), "14:30:45.123456")
        self.assertEqual(str(self.t3), "23:59:59.999999")

    def test_pickle(self):
        pickled = pickle.dumps(self.t2)
        unpickled = pickle.loads(pickled)
        self.assertEqual(unpickled, self.t2)
        self.assertIsInstance(unpickled, BSTime)
        self.assertEqual(str(unpickled.tzinfo), "Asia/Kathmandu")

    def test_class_attributes(self):
        self.assertEqual(BSTime.min, BSTime(0, 0))
        self.assertEqual(BSTime.max, BSTime(23, 59, 59, 999999))

    def test_edge_cases(self):
        # Midnight transition
        # midnight = BSTime(23, 59, 59, 999999) + timedelta(microseconds=1)
        # self.assertEqual(midnight, BSTime(0, 0))
        # Zero time
        zero = BSTime(0, 0, 0, 0)
        self.assertEqual(zero.isoformat(), "00:00:00")

    def test_midnight(self):
        from bikram_sambat import datetime, date

        temp_datetime = datetime.combine(date(2082, 1, 1), BSTime(23, 59, 59, 999999))
        result_datetime = temp_datetime + timedelta(microseconds=1)
        midnight_time = result_datetime.time()
        midnight_bstime = BSTime(
            midnight_time.hour,
            midnight_time.minute,
            midnight_time.second,
            midnight_time.microsecond,
            midnight_time.tzinfo,
            fold=midnight_time.fold,
        )
        self.assertEqual(midnight_bstime, BSTime(0, 0))


if __name__ == "__main__":
    unittest.main()
