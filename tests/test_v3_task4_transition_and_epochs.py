"""
Unit and Integration Tests for Task 4: GRACE to GRACE-FO Transition & Epoch Comparison
======================================================================================
Verifies:
  1. Calibrated epoch comparisons (GRACE era vs GRACE-FO era)
  2. Difference test 95% CIs include zero (no detectable acceleration or deceleration)
  3. Three-way slope reporting (single line, step-adjusted, transition-excluded, lead grace_era)
  4. Step offset significance and buffer exclusion sensitivity
"""

import json
from pathlib import Path
import unittest
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_V3 = REPO_ROOT / "outputs" / "v3"
FULL_RECORD_DIR = OUTPUTS_V3 / "full_record"


class TestTask4TransitionAndEpochs(unittest.TestCase):
    def setUp(self):
        self.epoch_csv = FULL_RECORD_DIR / "epoch_comparison.csv"
        self.epoch_md = FULL_RECORD_DIR / "epoch_comparison.md"
        self.epoch_json = FULL_RECORD_DIR / "epoch_comparison_summary.json"
        self.three_way_csv = FULL_RECORD_DIR / "three_way_slopes_and_transition.csv"
        self.offset_csv = FULL_RECORD_DIR / "offset_test.csv"

    def test_files_exist(self):
        self.assertTrue(self.epoch_csv.exists(), "Missing epoch_comparison.csv")
        self.assertTrue(self.epoch_md.exists(), "Missing epoch_comparison.md")
        self.assertTrue(self.epoch_json.exists(), "Missing epoch_comparison_summary.json")
        self.assertTrue(self.three_way_csv.exists(), "Missing three_way_slopes_and_transition.csv")
        self.assertTrue(self.offset_csv.exists(), "Missing offset_test.csv")

    def test_epoch_comparison_results(self):
        df = pd.read_csv(self.epoch_csv).set_index("region")
        self.assertEqual(len(df), 6, "Expected 6 regions in epoch comparison")

        # In all regions, the difference 95% CI must include zero
        for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
            ci_low = df.loc[reg, "diff_ci95_low"]
            ci_high = df.loc[reg, "diff_ci95_high"]
            self.assertLessEqual(ci_low, 0.0, f"{reg} diff CI low must be <= 0")
            self.assertGreaterEqual(ci_high, 0.0, f"{reg} diff CI high must be >= 0")
            self.assertGreaterEqual(df.loc[reg, "diff_p_value"], 0.05, f"{reg} p-value must be >= 0.05")

        # Core depletion hotspots must be classified as continuing at a similar rate
        for reg in ["NW", "NE", "Central", "National"]:
            self.assertIn("Continuing at a similar rate", df.loc[reg, "verdict"],
                          f"{reg} should be 'Continuing at a similar rate'")

    def test_three_way_slopes(self):
        df = pd.read_csv(self.three_way_csv).set_index("region")

        # Verify NW values
        nw = df.loc["NW"]
        self.assertAlmostEqual(nw["single_line_slope_cm_yr"], -1.25, delta=0.05)
        self.assertAlmostEqual(nw["step_adjusted_slope_cm_yr"], -1.81, delta=0.05)
        self.assertAlmostEqual(nw["transition_excluded_slope_cm_yr"], -1.29, delta=0.05)
        self.assertAlmostEqual(nw["lead_grace_era_slope_cm_yr"], -1.56, delta=0.05)
        self.assertAlmostEqual(nw["transition_step_delta_cm"], 9.15, delta=0.05)
        self.assertLess(nw["transition_step_p_value"], 0.05, "NW step term must be significant (p < 0.05)")
        self.assertGreater(nw["transition_excluded_step_p_value"], 0.05, "NW buffer excluded step must be non-significant (p >= 0.05)")

        # Verify that lead grace_era slope is steeper than single line slope in all depletion zones
        for reg in ["NW", "NE", "Central", "National"]:
            r = df.loc[reg]
            self.assertLess(r["lead_grace_era_slope_cm_yr"], r["single_line_slope_cm_yr"],
                            f"{reg} single-line fit should underestimate depletion compared to clean grace_era")


if __name__ == "__main__":
    unittest.main()
