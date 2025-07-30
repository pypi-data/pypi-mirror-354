import unittest
from datetime import date as gregorian_date, datetime as gregorian_datetime, timezone
from bikram_sambat import conversion
from bikram_sambat.data import calendar_data
from bikram_sambat.exceptions import (
    DateOutOfRangeError,
    InvalidTypeError,
    InvalidDateError,
)


class TestConversion(unittest.TestCase):
    def setUp(self):
        # Reference and test dates
        self.ref_date = gregorian_date(1918, 4, 13)  # BS 1975-01-01
        self.test_date_2025 = gregorian_date(2025, 5, 16)  # ~BS 2082-02-02
        self.test_date_2025_next = gregorian_date(2025, 5, 17)  # ~BS 2082-02-03
        self.test_date_2044 = gregorian_date(2044, 4, 12)  # ~BS 2100-12-30
        self.test_date_1919_early = gregorian_date(1919, 3, 13)  # ~BS 1975-11-30
        self.test_date_chaitra_1975 = gregorian_date(1919, 3, 14)  # ~BS 1975-12-01

        self.test_date_1919_later = gregorian_date(1919, 4, 12)  # ~BS 1975-12-30
        self.test_date_1976_baisakh_1 = gregorian_date(1919, 4, 13)  # ~BS 1976-01-01


    def test_ad_to_bs_valid(self):
        """Test valid Gregorian to BS conversions."""
        # Reference date
        self.assertEqual(
            conversion.ad_to_bs(self.ref_date),
            (1975, 1, 1),
            "Failed reference date conversion",
        )
        # Test date in 2025
        self.assertEqual(
            conversion.ad_to_bs(self.test_date_2025),
            (2082, 2, 2),
            "Failed 2025-05-16 conversion",
        )
        self.assertEqual(
            conversion.ad_to_bs(self.test_date_2025_next),
            (2082, 2, 3),
            "Failed 2025-05-17 conversion",
        )
        # Last valid date
        self.assertEqual(
            conversion.ad_to_bs(self.test_date_2044),
            (2100, 12, 30),
            "Failed 2044-04-12 conversion",
        )
        # Edge cases
        self.assertEqual(
            conversion.ad_to_bs(self.test_date_1919_early),
            (1975, 11, 30),  # Adjust based on calendar.json
            "Failed 1919-03-13 conversion",
        )
        self.assertEqual(
            conversion.ad_to_bs(self.test_date_1919_later),
            (1975, 12, 30),
            "Failed 1919-04-12 conversion",
        )

    def test_bs_to_ad_valid(self):
        """Test valid BS to Gregorian conversions."""
        # Reference date
        self.assertEqual(
            conversion.bs_to_ad(1975, 1, 1),
            self.ref_date,
            "Failed BS 1975-01-01 conversion",
        )
        # Test date in 2082
        self.assertEqual(
            conversion.bs_to_ad(2082, 2, 2),
            self.test_date_2025,
            "Failed BS 2082-02-02 conversion",
        )
        self.assertEqual(
            conversion.bs_to_ad(2082, 2, 3),
            self.test_date_2025_next,
            "Failed BS 2082-02-03 conversion",
        )
        # Last valid date
        self.assertEqual(
            conversion.bs_to_ad(2100, 12, 30),
            self.test_date_2044,
            "Failed BS 2100-12-30 conversion",
        )
        # Edge cases
        self.assertEqual(
            conversion.bs_to_ad(1975, 11, 30),
            self.test_date_1919_early,
            "Failed BS 1975-11-30 conversion",
        )
        self.assertEqual(
            conversion.bs_to_ad(1975, 12, 1),
            self.test_date_chaitra_1975,  
            "Failed BS 1975-12-01 conversion",
        )
        self.assertEqual(
            conversion.bs_to_ad(1976, 1, 1),
            self.test_date_1976_baisakh_1,
            "Failed BS 1976-01-01 conversion",
        )

    def test_round_trip(self):
        """Test Gregorian → BS → Gregorian and BS → Gregorian → BS consistency."""
        # Gregorian to BS to Gregorian
        test_dates = [
            self.ref_date,
            self.test_date_2025,
            self.test_date_2025_next,
            self.test_date_2044,
            self.test_date_1919_early,
            self.test_date_1919_later,
        ]
        for greg_date in test_dates:
            bs_year, bs_month, bs_day = conversion.ad_to_bs(greg_date)
            round_trip = conversion.bs_to_ad(bs_year, bs_month, bs_day)
            self.assertEqual(
                round_trip, greg_date, f"Round trip failed for Gregorian {greg_date}"
            )
        # BS to Gregorian to BS
        bs_dates = [
            (1975, 1, 1),
            (2082, 2, 2),
            (2082, 2, 3),
            (2100, 12, 30),
            (1975, 11, 30),
            (1975, 12, 1),
            (1976, 1, 1),
        ]
        for year, month, day in bs_dates:
            greg_date = conversion.bs_to_ad(year, month, day)
            round_trip_year, round_trip_month, round_trip_day = conversion.ad_to_bs(
                greg_date
            )
            self.assertEqual(
                (round_trip_year, round_trip_month, round_trip_day),
                (year, month, day),
                f"Round trip failed for BS {year}-{month:02d}-{day:02d}",
            )

    def test_invalid_inputs(self):
        """Test invalid input types and values."""
        # Invalid types for ad_to_bs
        with self.assertRaises(InvalidTypeError):
            conversion.ad_to_bs("2025-05-15")
        with self.assertRaises(InvalidTypeError):
            conversion.ad_to_bs(2025)
        # Invalid types for bs_to_ad
        with self.assertRaises(InvalidTypeError):
            conversion.bs_to_ad("2082", 2, 2)
        with self.assertRaises(InvalidTypeError):
            conversion.bs_to_ad(2082, 2.5, 2)
        # Invalid BS date components
        with self.assertRaises(InvalidDateError):
            conversion.bs_to_ad(2082, 13, 1)  # Invalid month
        with self.assertRaises(InvalidDateError):
            conversion.bs_to_ad(2082, 2, 32)  # Invalid day
        # Out-of-range years
        with self.assertRaises(DateOutOfRangeError):
            conversion.bs_to_ad(1900, 1, 1)  # Before 1901
        with self.assertRaises(DateOutOfRangeError):
            conversion.bs_to_ad(2200, 1, 1)  # After 2100
        with self.assertRaises(DateOutOfRangeError):
            conversion.ad_to_bs(gregorian_date(1800, 1, 1))  # Before BS 1975
        with self.assertRaises(DateOutOfRangeError):
            conversion.ad_to_bs(gregorian_date(2200, 1, 1))  # After BS 2100

    def test_edge_cases(self):
        """Test boundary and edge cases."""
        # First valid BS date
        self.assertEqual(
            conversion.ad_to_bs(gregorian_date(1918, 4, 13)),
            (1975, 1, 1),
            "Failed first BS date",
        )
        self.assertEqual(
            conversion.bs_to_ad(1975, 1, 1),
            gregorian_date(1918, 4, 13),
            "Failed first BS date reverse",
        )
        # Last valid BS date 
        max_days = calendar_data.YEAR_MONTH_DAYS_BS[2100][11]
        self.assertEqual(
            conversion.bs_to_ad(2100, 12, max_days),
            gregorian_date(2044, 4, 13),
            "Failed last BS date",
        )
        self.assertEqual(
            conversion.ad_to_bs(gregorian_date(2044, 4, 13)),
            (2100, 12, max_days),
            "Failed last BS date reverse",
        )
        # First day of a month
        self.assertEqual(
            conversion.bs_to_ad(2082, 1, 1),
            gregorian_date(2025, 4, 14),  
            "Failed first day of month",
        )
        # Last day of a month
        max_days_2082_2 = calendar_data.YEAR_MONTH_DAYS_BS[2082][1]
        self.assertEqual(
            conversion.bs_to_ad(2082, 2, max_days_2082_2),
            gregorian_date(2025, 6, 14), 
            "Failed last day of month",
        )
        # Edge case: Your specified dates
        self.assertEqual(
            conversion.bs_to_ad(1975, 11, 30),
            gregorian_date(1919, 3, 13),
            "Failed BS 1975-11-30",
        )
        self.assertEqual(
            conversion.bs_to_ad(1975, 12, 1),
            gregorian_date(1919, 3, 14),
            "Failed BS 1975-12-01",
        )
        self.assertEqual(
            conversion.bs_to_ad(1976, 1, 1),
            gregorian_date(1919, 4, 13),
            "Failed BS 1976-01-01",
        )

    def test_ad_datetime_to_bs(self):
        """Test Gregorian datetime to BS datetime tuple conversion."""
        dt = gregorian_datetime(2025, 5, 16, 12, 30, 45, 500, tzinfo=timezone.utc)
        expected = (2082, 2, 2, 12, 30, 45, 500, timezone.utc)
        result = conversion.ad_datetime_to_bs(dt)
        self.assertEqual(result, expected, "Failed datetime conversion")
        # Without timezone
        dt_no_tz = gregorian_datetime(2025, 5, 16, 12, 30, 45, 500)
        expected_no_tz = (2082, 2, 2, 12, 30, 45, 500, None)
        self.assertEqual(
            conversion.ad_datetime_to_bs(dt_no_tz),
            expected_no_tz,
            "Failed datetime conversion without timezone",
        )
        # Invalid input
        with self.assertRaises(InvalidTypeError):
            conversion.ad_datetime_to_bs("2025-05-16")

    def test_bs_datetime_to_ad(self):
        """Test BS datetime to Gregorian datetime conversion."""
        expected = gregorian_datetime(2025, 5, 16, 12, 30, 45, 500, tzinfo=timezone.utc)
        result = conversion.bs_datetime_to_ad(2082, 2, 2, 12, 30, 45, 500, timezone.utc)
        self.assertEqual(result, expected, "Failed BS datetime conversion")
        # Without timezone
        expected_no_tz = gregorian_datetime(2025, 5, 16, 12, 30, 45, 500)
        result_no_tz = conversion.bs_datetime_to_ad(2082, 2, 2, 12, 30, 45, 500)
        self.assertEqual(
            result_no_tz,
            expected_no_tz,
            "Failed BS datetime conversion without timezone",
        )
        # Invalid inputs
        with self.assertRaises(InvalidTypeError):
            conversion.bs_datetime_to_ad(2082, 2, 2, "12", 30, 45, 500)
        with self.assertRaises(InvalidDateError):
            conversion.bs_datetime_to_ad(2082, 2, 2, 24, 30, 45, 500)  # Invalid hour
        with self.assertRaises(DateOutOfRangeError):
            conversion.bs_datetime_to_ad(1900, 1, 1, 12, 30, 45, 500)


if __name__ == "__main__":
    unittest.main()
