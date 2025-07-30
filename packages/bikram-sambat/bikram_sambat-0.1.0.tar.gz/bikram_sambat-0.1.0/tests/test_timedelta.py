import unittest
import pickle
from bikram_sambat.bs_timedelta import BSTimedelta
from bikram_sambat.exceptions import InvalidTypeError
from bikram_sambat.constants import STANDARD_DIGITS


class TestBSTimeDelta(unittest.TestCase):
    def setUp(self):
        self.td1 = BSTimedelta(days=1, seconds=3600)  # 1 day, 1 hour
        self.td2 = BSTimedelta(seconds=7200)  # 2 hours
        self.td3 = BSTimedelta(days=-1, seconds=-1800)  # -1 day, -30 min

    def test_init(self):
        self.assertEqual(self.td1.days, 1)
        self.assertEqual(self.td1.seconds, 3600)
        self.assertEqual(self.td1.microseconds, 0)
        # self.assertEqual(self.td3.days, -1)
        self.assertEqual(self.td3.total_seconds(), -88200) # -1 day and -1800s

        self.assertEqual(self.td3.seconds, 84600)
        self.assertEqual(self.td3, BSTimedelta(days=-2, seconds=84600))

    def test_invalid_init(self):
        with self.assertRaises(InvalidTypeError):
            BSTimedelta(days="1")
        with self.assertRaises(InvalidTypeError):
            BSTimedelta(seconds=[7200])

    def test_arithmetic(self):
        # Addition
        result = self.td1 + self.td2
        self.assertEqual(result, BSTimedelta(days=1, seconds=10800))
        # Subtraction
        result = self.td1 - self.td2
        self.assertEqual(result, BSTimedelta(days=0, hours=23, seconds=0))
        # Multiplication
        result = self.td1 * 2
        self.assertEqual(result, BSTimedelta(days=2, seconds=7200))
        # Division
        result = self.td1 / 2
        self.assertEqual(result, BSTimedelta(seconds=45000))  # 12 hours

    def test_comparison(self):
        self.assertEqual(self.td1, BSTimedelta(days=1, seconds=3600))
        self.assertLess(self.td2, self.td1)
        self.assertGreater(self.td1, self.td3)
        self.assertLessEqual(self.td1, self.td1)
        self.assertGreaterEqual(self.td1, self.td1)

    def test_str_english(self):
        self.assertEqual(str(self.td1), "1 day, 1:00:00")
        self.assertEqual(str(self.td2), "2:00:00")
        self.assertEqual(str(self.td3), "-1 day, 0:30:00")

    def test_str_nepali(self):
        expected = "१ दिन, १:००:००"
        result = self.td1.__str__(use_nepali_digits=True)
        self.assertEqual(result, expected)
        expected = "२:००:००"
        result = self.td2.__str__(use_nepali_digits=True)
        self.assertEqual(result, expected)

    def test_edge_cases(self):
        # Large timedelta
        large_td = BSTimedelta(days=999999)
        self.assertEqual(str(large_td).split()[0], "999999")
        # Zero timedelta
        zero_td = BSTimedelta()
        self.assertEqual(str(zero_td), "0:00:00")
        # Microsecond precision
        micro_td = BSTimedelta(microseconds=123456)
        self.assertEqual(str(micro_td), "0:00:00.123456")
        micro_nepali = micro_td.__str__(use_nepali_digits=True)
        self.assertEqual(micro_nepali, "०:००:००.१२३४५६")

    def test_pickle(self):
        pickled = pickle.dumps(self.td1)
        unpickled = pickle.loads(pickled)
        self.assertEqual(unpickled, self.td1)
        self.assertIsInstance(unpickled, BSTimedelta)


if __name__ == "__main__":
    unittest.main()
