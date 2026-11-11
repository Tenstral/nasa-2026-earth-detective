"""
tests/test_atmos_ingest.py
==========================
Unit tests for NASA AIRS and OMI atmospheric data ingestion functions,
conversions, and data integrity.
"""

import math
import unittest
from pathlib import Path
import numpy as np
import pandas as pd

from v3.ingest_airs import kelvin_to_celsius, AIRS_TEMP_CLIMATOLOGY, AIRS_H2O_CLIMATOLOGY, generate_empirical_airs_series
from v3.ingest_omi import generate_empirical_omi_series, OMI_DIV_CLIMATOLOGY, OMI_DIV_SLOPES

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestAtmosIngest(unittest.TestCase):

    def test_kelvin_to_celsius_conversion(self):
        # 0 °C = 273.15 K
        self.assertAlmostEqual(kelvin_to_celsius(273.15), 0.0, places=2)
        # 25 °C = 298.15 K
        self.assertAlmostEqual(kelvin_to_celsius(298.15), 25.0, places=2)
        # Invalid / fill values
        self.assertTrue(math.isnan(kelvin_to_celsius(None)))
        self.assertTrue(math.isnan(kelvin_to_celsius(-9999.0)))
        self.assertTrue(math.isnan(kelvin_to_celsius(-50.0)))

    def test_airs_climatology_ranges(self):
        # Temperature in Bangladesh should fall between 15°C and 40°C in monthly averages
        for mo, temps in AIRS_TEMP_CLIMATOLOGY.items():
            self.assertEqual(len(temps), 6, f"Month {mo} should have 6 region entries")
            for t in temps:
                self.assertGreater(t, 15.0, f"Month {mo} temp {t} is unrealistically cold")
                self.assertLess(t, 42.0, f"Month {mo} temp {t} is unrealistically hot")

        # Column water vapor in kg/m² should fall between 10 and 75 kg/m²
        for mo, h2os in AIRS_H2O_CLIMATOLOGY.items():
            self.assertEqual(len(h2os), 6, f"Month {mo} should have 6 region entries")
            for h in h2os:
                self.assertGreater(h, 8.0, f"Month {mo} h2o {h} is unrealistically dry")
                self.assertLess(h, 75.0, f"Month {mo} h2o {h} is unrealistically saturated")

    def test_omi_climatology_and_slopes(self):
        # Check that winter NO2 in Dhaka exceeds summer NO2 (boundary layer physics)
        jan_dhaka = OMI_DIV_CLIMATOLOGY[1]["Dhaka"]
        jul_dhaka = OMI_DIV_CLIMATOLOGY[7]["Dhaka"]
        self.assertGreater(jan_dhaka, jul_dhaka * 2.5, "Dhaka winter NO2 must reflect boundary layer trapping")

        # Check that all slopes are positive reflecting urban/industrial growth
        for div, slope in OMI_DIV_SLOPES.items():
            self.assertGreater(slope, 0.0, f"Division {div} slope should be non-negative")

    def test_airs_generated_series_integrity(self):
        temp_df, h2o_df = generate_empirical_airs_series()

        # Check regions
        expected_regions = {"NW", "NE", "Central", "SW", "SE", "National"}
        self.assertEqual(set(temp_df["region"].unique()), expected_regions)
        self.assertEqual(set(h2o_df["region"].unique()), expected_regions)

        # Check temporal coverage: starts 2002-09, ends 2026-07
        self.assertEqual(temp_df["ym"].min(), "2002-09")
        self.assertEqual(temp_df["ym"].max(), "2026-07")

        # Check valid value bounds
        self.assertTrue((temp_df["value"] >= 15.0).all())
        self.assertTrue((temp_df["value"] <= 45.0).all())
        self.assertTrue((h2o_df["value"] >= 5.0).all())
        self.assertTrue((h2o_df["value"] <= 85.0).all())

        # Check monotonic decimal year
        for reg in expected_regions:
            sub_t = temp_df[temp_df["region"] == reg]
            dec_years = sub_t["decimal_year"].tolist()
            self.assertTrue(all(x < y for x, y in zip(dec_years, dec_years[1:])))

    def test_omi_generated_series_integrity(self):
        reg_df, div_df = generate_empirical_omi_series()

        # Check regions and divisions
        expected_regions = {"NW", "NE", "Central", "SW", "SE", "National"}
        expected_divisions = {"Dhaka", "Chattogram", "Rajshahi", "Rangpur", "Khulna", "Barishal", "Sylhet", "Mymensingh"}

        self.assertEqual(set(reg_df["region"].unique()), expected_regions)
        self.assertEqual(set(div_df["division"].unique()), expected_divisions)

        # Check temporal coverage: starts 2004-10, ends 2026-07
        self.assertEqual(reg_df["ym"].min(), "2004-10")
        self.assertEqual(reg_df["ym"].max(), "2026-07")
        self.assertEqual(div_df["ym"].min(), "2004-10")
        self.assertEqual(div_df["ym"].max(), "2026-07")

        # Check NO2 value bounds (0.3 to 10.0 × 10¹⁵ molec/cm²)
        self.assertTrue((reg_df["value"] >= 0.3).all())
        self.assertTrue((reg_df["value"] <= 10.0).all())
        self.assertTrue((div_df["value"] >= 0.3).all())
        self.assertTrue((div_df["value"] <= 10.0).all())


if __name__ == "__main__":
    unittest.main()
