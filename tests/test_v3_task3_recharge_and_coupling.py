"""
Unit and Integration Tests for Task 3: Rainfall Dependencies & Coupling
========================================================================
Verifies:
  1. 2x2 Hydrological Quadrant Matrix integrity
  2. Seasonal Recharge Dynamics: Storage rebound alone & IMERG efficiency
  3. Historical Flood Events: Decoupled IMERG totals & 2017 gap resolution
  4. Socioeconomic Exposure Table: Inclusion of primary rainfall verdict
"""

import json
from pathlib import Path
import unittest
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_V3 = REPO_ROOT / "outputs" / "v3"
FULL_RECORD_DIR = OUTPUTS_V3 / "full_record"
EXTREMES_DIR = OUTPUTS_V3 / "extremes"
EXPOSURE_DIR = OUTPUTS_V3 / "exposure"


class TestTask3RainfallDependencies(unittest.TestCase):
    def setUp(self):
        self.coupling_csv = FULL_RECORD_DIR / "rain_vs_storage_2x2_classification.csv"
        self.recharge_csv = FULL_RECORD_DIR / "seasonal_recharge_24yr.csv"
        self.recharge_json = FULL_RECORD_DIR / "seasonal_recharge_summary.json"
        self.flood_csv = EXTREMES_DIR / "flood_events_context.csv"
        self.exposure_csv = EXPOSURE_DIR / "exposure_table.csv"
        self.diff_csv = FULL_RECORD_DIR / "task3_old_vs_new_diff.csv"

    def test_files_exist(self):
        self.assertTrue(self.coupling_csv.exists(), "Missing rain_vs_storage_2x2_classification.csv")
        self.assertTrue(self.recharge_csv.exists(), "Missing seasonal_recharge_24yr.csv")
        self.assertTrue(self.recharge_json.exists(), "Missing seasonal_recharge_summary.json")
        self.assertTrue(self.flood_csv.exists(), "Missing flood_events_context.csv")
        self.assertTrue(self.exposure_csv.exists(), "Missing exposure_table.csv")
        self.assertTrue(self.diff_csv.exists(), "Missing task3_old_vs_new_diff.csv")

    def test_coupling_quadrants(self):
        df = pd.read_csv(self.coupling_csv)
        self.assertEqual(len(df), 42, "Expected 42 rows (14 entities x 3 seasons)")

        ann_df = df[df["season"] == "annual"].set_index("entity")

        # Northwest, Northeast, Central, National should be Q1
        for reg in ["NW", "NE", "Central", "National"]:
            self.assertEqual(ann_df.loc[reg, "quadrant_id"], "Q1", f"{reg} should be Q1")
            self.assertEqual(ann_df.loc[reg, "tws_verdict"], "Significant", f"{reg} TWS should be Significant")
            self.assertEqual(ann_df.loc[reg, "precip_verdict"], "No detectable trend", f"{reg} Rain should be flat")

        # Southwest and Southeast should be Q3
        for reg in ["SW", "SE"]:
            self.assertEqual(ann_df.loc[reg, "quadrant_id"], "Q3", f"{reg} should be Q3")
            self.assertEqual(ann_df.loc[reg, "tws_verdict"], "No detectable trend", f"{reg} TWS should be flat")
            self.assertEqual(ann_df.loc[reg, "precip_verdict"], "No detectable trend", f"{reg} Rain should be flat")

    def test_seasonal_recharge_dynamics(self):
        df = pd.read_csv(self.recharge_csv)
        self.assertEqual(len(df), 144, "Expected 144 rows (24 years x 6 regions)")

        # 2017 must have valid=False and gap note
        sub_2017 = df[df["year"] == 2017]
        self.assertTrue(all(~sub_2017["valid"]), "2017 must have valid=False")
        self.assertTrue(all(sub_2017["note"].str.contains("gap", case=False)), "2017 note must mention gap")

        # 2018 must have valid=False
        sub_2018 = df[df["year"] == 2018]
        self.assertTrue(all(~sub_2018["valid"]), "2018 must have valid=False")

        # Verify 22 valid seasons
        for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
            sub_reg = df[(df["region"] == reg) & (df["valid"] == True)]
            self.assertEqual(len(sub_reg), 22, f"Expected 22 valid seasons for {reg}")

        # Verify summary JSON reports storage rebound alone
        with open(self.recharge_json, "r", encoding="utf-8") as f:
            summary = json.load(f)

        for res in summary["results"]:
            self.assertIn("rebound_alone_mean_cm", res)
            self.assertIn("rebound_alone_slope_cm_yr", res)
            self.assertIn("rebound_alone_verdict", res)
            self.assertIn("efficiency_imerg_mean", res)
            self.assertGreater(res["rebound_alone_mean_cm"], 40.0)
            self.assertLess(res["rebound_alone_mean_cm"], 70.0)

    def test_flood_events_context(self):
        df = pd.read_csv(self.flood_csv).set_index("year")

        # 2017 rainfall must be > 1800 mm (not 690 mm) and positive anomaly
        self.assertGreater(df.loc[2017, "national_monsoon_precip_mm"], 1800.0)
        self.assertGreater(df.loc[2017, "precip_anomaly_vs_mean_pct"], 0.0)
        self.assertTrue(np.isnan(df.loc[2017, "post_monsoon_peak_cm"]))

        # 2020 rainfall must be ~1809 mm (not 2214 mm)
        self.assertAlmostEqual(df.loc[2020, "national_monsoon_precip_mm"], 1809.2, delta=5.0)

        # 2004 rainfall must be ~2021 mm (not 1416 mm)
        self.assertAlmostEqual(df.loc[2004, "national_monsoon_precip_mm"], 2020.9, delta=5.0)

    def test_exposure_table_coupling(self):
        df = pd.read_csv(self.exposure_csv).set_index("region")

        # Check primary precipitation columns exist
        self.assertIn("primary_precip_source", df.columns)
        self.assertIn("primary_precip_slope_mm_yr", df.columns)
        self.assertIn("primary_precip_verdict", df.columns)
        self.assertIn("hydrological_quadrant", df.columns)

        for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
            self.assertEqual(df.loc[reg, "primary_precip_source"], "GPM_IMERG_V07B")
            self.assertEqual(df.loc[reg, "primary_precip_verdict"], "No detectable trend")
            self.assertNotEqual(df.loc[reg, "tws_fdr_q"], "0.0")
            self.assertNotEqual(df.loc[reg, "tws_fdr_q"], "0.0000")


if __name__ == "__main__":
    unittest.main()
