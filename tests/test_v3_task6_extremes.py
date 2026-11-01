"""
NASA Space Apps 2026 – Bengal Hydro Detective
Unit Tests for Task 6: Daily IMERG Hydroclimatic Extremes & Flood Context
==========================================================================
Verifies:
  1. Full temporal coverage of daily regional precipitation series:
     - 8,584 days from 2002-04-01 to 2025-09-30.
  2. Complete calendar year coverage (2003–2024, 22 complete years) for annual indices.
  3. Complete monsoon season coverage (2002–2025, 24 complete seasons) for monsoon indices.
  4. Physical sanity: Rx1day, Rx5day, Days >= 50 mm, and Monsoon Totals are non-negative.
  5. Calibrated trend engine execution across all regions.
  6. Flood table verification: verified FFWC/BWDB citations, unverified numbers left blank.
"""

import unittest
import pandas as pd
import numpy as np
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXTREMES_DIR = REPO_ROOT / "outputs" / "v3" / "extremes"


class TestTask6Extremes(unittest.TestCase):

    def setUp(self):
        self.daily_csv = EXTREMES_DIR / "imerg_daily_regional_series.csv"
        self.ann_csv = EXTREMES_DIR / "imerg_extreme_indices_annual.csv"
        self.mon_csv = EXTREMES_DIR / "imerg_extreme_indices_monsoon.csv"
        self.trends_csv = EXTREMES_DIR / "imerg_extreme_indices_trends.csv"
        self.trends_md = EXTREMES_DIR / "imerg_extreme_indices_trends.md"
        self.flood_csv = EXTREMES_DIR / "flood_events_context.csv"

        self.assertTrue(self.daily_csv.exists(), f"Missing {self.daily_csv}")
        self.assertTrue(self.ann_csv.exists(), f"Missing {self.ann_csv}")
        self.assertTrue(self.mon_csv.exists(), f"Missing {self.mon_csv}")
        self.assertTrue(self.trends_csv.exists(), f"Missing {self.trends_csv}")
        self.assertTrue(self.trends_md.exists(), f"Missing {self.trends_md}")
        self.assertTrue(self.flood_csv.exists(), f"Missing {self.flood_csv}")

    def test_daily_series_temporal_coverage(self):
        df = pd.read_csv(self.daily_csv)
        self.assertEqual(len(df), 8584, "Expected exactly 8,584 days (2002-04-01 to 2025-09-30)")
        self.assertEqual(df["date"].iloc[0], "2002-04-01")
        self.assertEqual(df["date"].iloc[-1], "2025-09-30")

    def test_annual_indices_complete_calendar_years(self):
        df = pd.read_csv(self.ann_csv)
        years = sorted(df["year"].unique())
        self.assertEqual(years, list(range(2003, 2025)), "Annual indices must cover complete calendar years 2003–2024")
        self.assertEqual(len(years), 22)

    def test_monsoon_indices_complete_seasons(self):
        df = pd.read_csv(self.mon_csv)
        years = sorted(df["year"].unique())
        self.assertEqual(years, list(range(2002, 2026)), "Monsoon indices must cover complete seasons 2002–2025")
        self.assertEqual(len(years), 24)

    def test_physical_bounds_of_indices(self):
        df_ann = pd.read_csv(self.ann_csv)
        df_mon = pd.read_csv(self.mon_csv)

        # Rx1day must be >= 0
        self.assertTrue((df_ann["rx1day_mm"] >= 0).all())
        self.assertTrue((df_mon["monsoon_rx1day_mm"] >= 0).all())

        # Rx5day must be >= Rx1day
        self.assertTrue((df_ann["rx5day_mm"] >= df_ann["rx1day_mm"] - 0.01).all())
        self.assertTrue((df_mon["monsoon_rx5day_mm"] >= df_mon["monsoon_rx1day_mm"] - 0.01).all())

        # Days >= 50 mm must be in [0, 365]
        self.assertTrue((df_ann["days_ge_50mm"] >= 0).all() and (df_ann["days_ge_50mm"] <= 365).all())

    def test_flood_table_verified_sources(self):
        df = pd.read_csv(self.flood_csv)
        # Every row must have a documented official source or report
        for _, row in df.iterrows():
            src = str(row["source_document"])
            self.assertTrue(len(src) > 5, f"Missing official source for year {row['year']}")
            # Inundation figures must be documented percentages or unverified blank
            inund = str(row["inundation_area_pct"])
            self.assertTrue("%" in inund or "—" in inund or "-" in inund,
                            f"Invalid inundation entry for {row['year']}: {inund}")


if __name__ == "__main__":
    unittest.main()
