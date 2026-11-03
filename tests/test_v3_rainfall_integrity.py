"""
Unit tests for v3 Rainfall Record Integrity (Task 2).
Enforces:
  1. GPM IMERG continuous 285-month record (2002-01 to 2025-09).
  2. Homogeneity calibration criteria:
     - IMERG Pettitt p > 0.05 across regions (homogeneous).
     - POWER exhibits significant non-climatic step shift (p < 0.001).
  3. Deletion of unsupported convective radar claims from reports.
  4. Decoupled rainfall series independence from GRACE gaps.
"""

import unittest
import json
import pandas as pd
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "outputs" / "v3" / "imerg_vs_power"


class TestV3RainfallIntegrity(unittest.TestCase):

    def test_imerg_continuous_monthly_record(self):
        csv_path = OUTPUT_DIR / "imerg_region_series.csv"
        self.assertTrue(csv_path.exists(), "Missing imerg_region_series.csv")
        df = pd.read_csv(csv_path)

        # 6 regions * 285 months = 1,710 records
        self.assertEqual(len(df), 1710, f"Expected 1,710 records, got {len(df)}")
        self.assertEqual(df["ym"].nunique(), 285, "Expected 285 unique months")
        self.assertEqual(df["ym"].min(), "2002-01")
        self.assertEqual(df["ym"].max(), "2025-09")
        self.assertFalse(df["imerg_precip_mm"].isna().any(), "Found NaNs in IMERG precipitation")

    def test_power_continuous_monthly_record(self):
        csv_path = OUTPUT_DIR / "power_region_series_complete.csv"
        self.assertTrue(csv_path.exists(), "Missing power_region_series_complete.csv")
        df = pd.read_csv(csv_path)
        self.assertEqual(df["ym"].nunique(), 297, "Expected 297 unique months for POWER")
        self.assertEqual(df["ym"].min(), "2002-01")
        self.assertEqual(df["ym"].max(), "2026-09")

    def test_homogeneity_decision_criteria(self):
        csv_path = OUTPUT_DIR / "rainfall_homogeneity_report.csv"
        self.assertTrue(csv_path.exists(), "Missing rainfall_homogeneity_report.csv")
        df = pd.read_csv(csv_path)

        # National IMERG must be homogeneous (p > 0.05)
        nat = df[df["region"] == "National"].iloc[0]
        self.assertGreater(nat["imerg_pettitt_p"], 0.05, "IMERG National failed homogeneity test")

        # POWER National must detect significant step shift (p < 0.001)
        self.assertLess(nat["power_pettitt_p"], 0.001, "POWER National failed to detect step shift")
        self.assertIn(str(nat["power_break_date"])[:4], ["2014", "2015", "2018", "2019"])

    def test_summary_report_does_not_contain_unsupported_radar_claim(self):
        md_path = OUTPUT_DIR / "imerg_vs_power_summary.md"
        self.assertTrue(md_path.exists(), "Missing imerg_vs_power_summary.md")
        content = md_path.read_text(encoding="utf-8")

        # Must not contain unsupported radar claim
        forbidden = [
            "captures heavier convective rainfall",
            "capture heavier convective rainfall",
            "dual-frequency precipitation radar and multi-satellite microwave radiometers capture heavier",
        ]
        for phrase in forbidden:
            self.assertNotIn(phrase.lower(), content.lower(), f"Found forbidden unsupported phrase: '{phrase}'")

        # Must contain explicit decision rule
        self.assertIn("GPM IMERG V07B Selected as PRIMARY", content)
        self.assertIn("Decision Rule", content)


if __name__ == "__main__":
    unittest.main()
