"""
NASA Space Apps 2026 – Bengal Hydro Detective
Unit Tests for Task 5: GLDAS Multi-Model Soil-Moisture & Storage Partitioning
=============================================================================
Verifies:
  1. Full temporal coverage for all three models:
     - Noah 2.1: 292 months (2002-04 to 2026-07)
     - VIC 2.1: 292 months (2002-04 to 2026-07)
     - CLSM 2.2: 282 months (2003-02 to 2026-07)
  2. Baseline period (2004-01 to 2009-12) mean anomaly == 0.0 for all models.
  3. Proper scientific labeling:
     - CLSM: 'Non-independent / GRACE-assimilated'
     - Residual: 'groundwater + surface water + model error residual'
  4. Complete coverage across all 4 operational windows (full_record, grace_era, grace_fo_era, recent_2020).
  5. Multi-model spread statistics are properly computed and bounded.
"""

import unittest
import pandas as pd
import numpy as np
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "outputs" / "v3" / "gldas_split"


class TestGLDASMultiModel(unittest.TestCase):

    def setUp(self):
        self.summary_csv = OUTPUT_DIR / "gldas_multi_model_summary.csv"
        self.series_csv = OUTPUT_DIR / "storage_partition_series_multi_model.csv"
        self.assertTrue(self.summary_csv.exists(), f"Missing {self.summary_csv}")
        self.assertTrue(self.series_csv.exists(), f"Missing {self.series_csv}")
        self.df_summary = pd.read_csv(self.summary_csv)
        self.df_series = pd.read_csv(self.series_csv)

    def test_all_four_windows_present(self):
        expected_windows = {"full_record", "grace_era", "grace_fo_era", "recent_2020"}
        actual_windows = set(self.df_summary["window"].unique())
        self.assertEqual(expected_windows, actual_windows, "All 4 windows must be present in multi-model summary")

    def test_all_regions_present_per_window(self):
        expected_regions = {"NW", "NE", "Central", "SW", "SE", "National"}
        for win in ["full_record", "grace_era", "grace_fo_era", "recent_2020"]:
            sub = self.df_summary[self.df_summary["window"] == win]
            actual_regions = set(sub["region"].unique())
            self.assertEqual(expected_regions, actual_regions, f"Region mismatch in window {win}")

    def test_total_summary_row_count(self):
        # 4 windows * 6 regions = 24 rows
        self.assertEqual(len(self.df_summary), 24, "Expected exactly 24 rows (4 windows x 6 regions)")

    def test_clsm_and_residual_labels(self):
        # CLSM label must be Non-independent / GRACE-assimilated
        clsm_labels = set(self.df_summary["clsm_label"].dropna().unique())
        self.assertEqual(clsm_labels, {"Non-independent / GRACE-assimilated"})

        # Residual label must be strictly groundwater + surface water + model error residual
        res_labels = set(self.df_summary["residual_label"].unique())
        self.assertEqual(res_labels, {"groundwater + surface water + model error residual"})

    def test_multi_model_spread_validity(self):
        spread = self.df_summary["sms_slope_spread_cm_yr"]
        self.assertTrue((spread >= 0).all(), "Model spread must be non-negative")
        self.assertFalse(spread.isna().any(), "Model spread must not contain NaNs")

    def test_temporal_coverage_in_series(self):
        # Check National series
        nat = self.df_series[self.df_series["region"] == "National"].copy()
        
        # Noah and VIC must have 292 months (2002-04 to 2026-07)
        noah_valid = nat.dropna(subset=["noah_sms_anom_cm"])
        vic_valid = nat.dropna(subset=["vic_sms_anom_cm"])
        self.assertEqual(len(noah_valid), 292, f"Expected 292 Noah months, got {len(noah_valid)}")
        self.assertEqual(len(vic_valid), 292, f"Expected 292 VIC months, got {len(vic_valid)}")

        # CLSM starts 2003-02, so exactly 282 months (2003-02 to 2026-07)
        clsm_valid = nat.dropna(subset=["clsm_sms_anom_cm"])
        self.assertEqual(len(clsm_valid), 282, f"Expected 282 CLSM months, got {len(clsm_valid)}")

    def test_reference_period_zero_mean_anomaly(self):
        for reg in ["NW", "National"]:
            sub = self.df_series[self.df_series["region"] == reg].copy()
            base_mask = (sub["ym"] >= "2004-01") & (sub["ym"] <= "2009-12")

            # All model anomalies must have zero mean (+-1e-4) over baseline
            self.assertAlmostEqual(sub.loc[base_mask, "noah_sms_anom_cm"].mean(), 0.0, places=4)
            self.assertAlmostEqual(sub.loc[base_mask, "vic_sms_anom_cm"].mean(), 0.0, places=4)
            self.assertAlmostEqual(sub.loc[base_mask, "clsm_sms_anom_cm"].mean(), 0.0, places=4)


    def test_independent_models_separation_and_range(self):
        self.assertIn("independent_sms_slope_min", self.df_summary.columns)
        self.assertIn("independent_sms_slope_max", self.df_summary.columns)
        self.assertIn("independent_residual_slope_min", self.df_summary.columns)
        self.assertIn("independent_residual_slope_max", self.df_summary.columns)

        for _, row in self.df_summary.iterrows():
            self.assertLessEqual(row["independent_sms_slope_min"], row["independent_sms_slope_max"])
            self.assertLessEqual(row["independent_residual_slope_min"], row["independent_residual_slope_max"])
            self.assertIn("cannot serve as an independent partition", str(row["clsm_independence_note"]))

    def test_homogeneity_interpretation_note(self):
        md_path = OUTPUT_DIR / "gldas_multi_model_summary.md"
        self.assertTrue(md_path.exists())
        md_text = md_path.read_text(encoding="utf-8")
        self.assertIn("Interpretation of Homogeneity Tests Under a Secular Trend", md_text)
        self.assertIn("does not constitute evidence of meteorological data inhomogeneity", md_text.replace("**", ""))

        json_path = OUTPUT_DIR / "gldas_multi_model_summary.json"
        self.assertTrue(json_path.exists())
        import json
        data = json.loads(json_path.read_text(encoding="utf-8"))
        self.assertIn("homogeneity_interpretation_note", data)


if __name__ == "__main__":
    unittest.main()
