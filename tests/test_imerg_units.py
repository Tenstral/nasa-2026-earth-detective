"""
Unit tests for GPM IMERG monthly precipitation unit conversion.
Verifies rate (mm/hr) to accumulation (mm/month) conversion logic:
  accumulation = rate_mm_hr * 24 * days_in_month
Includes leap-year handling (Feb 2020: 29 days vs Feb 2021: 28 days).
"""

import calendar
import unittest
import numpy as np


def convert_imerg_rate_to_monthly_accumulation(
    rate_mm_hr: float, year: int, month: int, input_units: str = "mm/hr"
) -> float:
    """
    Converts IMERG precipitation rate to monthly accumulation.
    Asserts input_units is 'mm/hr' or equivalent.
    """
    valid_units = ["mm/hr", "mm/hour", "mm hr-1", "mm/h"]
    if not any(v in input_units.lower() for v in valid_units):
        raise ValueError(f"Unexpected input units '{input_units}'; expected mm/hr")

    days_in_month = calendar.monthrange(year, month)[1]
    hours_in_month = days_in_month * 24.0
    return float(rate_mm_hr * hours_in_month)


class TestIMERGUnitConversion(unittest.TestCase):

    def test_standard_31_day_month(self):
        # January: 31 days * 24 = 744 hours
        rate = 0.5  # mm/hr
        accum = convert_imerg_rate_to_monthly_accumulation(rate, 2024, 1, "mm/hr")
        expected = 0.5 * 31 * 24
        self.assertAlmostEqual(accum, expected, places=5)
        self.assertEqual(accum, 372.0)

    def test_standard_30_day_month(self):
        # April: 30 days * 24 = 720 hours
        rate = 1.0  # mm/hr
        accum = convert_imerg_rate_to_monthly_accumulation(rate, 2024, 4, "mm/hr")
        expected = 1.0 * 30 * 24
        self.assertAlmostEqual(accum, expected, places=5)
        self.assertEqual(accum, 720.0)

    def test_leap_year_february(self):
        # Feb 2020: leap year = 29 days * 24 = 696 hours
        rate = 0.1  # mm/hr
        accum = convert_imerg_rate_to_monthly_accumulation(rate, 2020, 2, "mm/hr")
        expected = 0.1 * 29 * 24
        self.assertAlmostEqual(accum, expected, places=5)
        self.assertAlmostEqual(accum, 69.6, places=5)

    def test_non_leap_year_february(self):
        # Feb 2021: non-leap = 28 days * 24 = 672 hours
        rate = 0.1  # mm/hr
        accum = convert_imerg_rate_to_monthly_accumulation(rate, 2021, 2, "mm/hr")
        expected = 0.1 * 28 * 24
        self.assertAlmostEqual(accum, expected, places=5)
        self.assertAlmostEqual(accum, 67.2, places=5)

    def test_invalid_units_raises(self):
        with self.assertRaises(ValueError):
            convert_imerg_rate_to_monthly_accumulation(0.5, 2024, 1, "m/s")


if __name__ == "__main__":
    unittest.main()
