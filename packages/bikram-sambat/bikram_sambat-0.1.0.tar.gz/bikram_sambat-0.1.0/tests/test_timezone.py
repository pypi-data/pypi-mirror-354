import unittest
from datetime import datetime
import pytz
from bikram_sambat.bs_timezone import nepal, utc, get_timezone, all_timezones_list
from bikram_sambat.bs_datetime import BSDatetime


class TestTimezone(unittest.TestCase):
    def setUp(self):
        self.dt_nepal = BSDatetime(2082, 2, 2, 15, 30, tzinfo=nepal)
        self.dt_utc = BSDatetime(2082, 2, 2, 15, 30, tzinfo=utc)

    def test_nepal_timezone(self):
        self.assertEqual(str(nepal), "Asia/Kathmandu")
        self.assertEqual(self.dt_nepal.strftime("%z"), "+0545")
        offset = nepal.utcoffset(datetime(2025, 5, 16))
        self.assertEqual(offset.total_seconds() / 3600, 5.75)

    def test_utc_timezone(self):
        self.assertEqual(str(utc), "UTC")
        self.assertEqual(self.dt_utc.strftime("%z"), "+0000")
        offset = utc.utcoffset(datetime(2025, 5, 16))
        self.assertEqual(offset.total_seconds(), 0)

    def test_get_timezone(self):
        ny_tz = get_timezone("America/New_York")
        self.assertEqual(str(ny_tz), "America/New_York")
        dt_ny = self.dt_nepal.astimezone(ny_tz)
        self.assertEqual(dt_ny.strftime("%z"), "-0400")  # EDT

    def test_all_timezones(self):
        self.assertIn("Asia/Kathmandu", all_timezones_list)
        self.assertIn("America/New_York", all_timezones_list)
        self.assertGreater(len(all_timezones_list), 100)

    def test_invalid_timezone(self):
        with self.assertRaises(pytz.exceptions.UnknownTimeZoneError):
            get_timezone("Invalid/Timezone")


if __name__ == "__main__":
    unittest.main()
