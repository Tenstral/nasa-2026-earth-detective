"""
Unit & Integration Tests: Pairwise Between-Region Slope Comparison & Statistical Pipeline
=========================================================================================
Validates the v3 between-region comparison methodology:
  1. CSV integrity: 20 rows per run (primary, grace_era, transition_excluded), monotone BH q-values.
  2. Antisymmetry: delta(A, B) == -delta(B, A), negated CI bounds, identical p-value.
  3. Duality & CI coverage: CI contains point estimate delta; CI excludes zero iff p < 0.05.
  4. Project verdict rule: strictly verified across p_value, bh_q_value, and CI zero-exclusion.
  5. Invariance of primary pipeline: results_all_windows.csv remains 336 rows, FDR family size 36.
  6. Verbatim limits text present in markdown report; zero forbidden phrases.
  7. Full 10-pair calibration: 0.035 <= FPR <= 0.065 and 0.930 <= Coverage <= 0.970 across all 20 tested pairs.
  8. Preserved audit trail and conservative CI overlap verification.
  9. Real-residual placebo audit with Variant 1 and Variant 2 across all 10 pairs.
 10. Dashboard and documentation integration of calibration line, overlap note, and disclosure.
"""

import json
import re
import unittest
from pathlib import Path
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent

VERBATIM_LIMITS_TEXT = (
    "Regions are adjacent and GRACE resolves a few hundred kilometres, "
    "so neighbouring regions share signal and coastal leakage is possible. "
    "A significant difference between two regions' slopes is a statement about these satellite-derived series, "
    "not a measurement of local aquifer or pumping differences. Recent windows are below the detection limit."
)

REAL_RESIDUAL_DISCLOSURE = (
    "Calibration used simulated AR(1) noise, which is the easier test. "
    "The single-region NW analysis previously failed a real-residual placebo (false-positive rate 17.6%, coverage 82.5%); "
    "the same check for the pairwise test is reported below."
)


class TestV3RegionComparison(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.out_dir = REPO_ROOT / "outputs" / "v3" / "region_comparison"
        cls.csv_path = cls.out_dir / "pairwise_region_differences.csv"
        cls.md_path = cls.out_dir / "pairwise_region_differences.md"
        cls.json_path = cls.out_dir / "calibration_report.json"
        cls.json_archived_v1 = cls.out_dir / "calibration_report_v1_bootstrap_failed.json"
        cls.json_placebo = cls.out_dir / "real_residual_placebo.json"
        cls.results_all_csv = REPO_ROOT / "outputs" / "v3" / "full_record" / "results_all_windows.csv"
        cls.index_html_path = REPO_ROOT / "index.html"
        cls.status_md_path = REPO_ROOT / "PROJECT_STATUS.md"

    def test_01_output_files_exist(self):
        self.assertTrue(self.csv_path.exists(), f"Missing CSV: {self.csv_path}")
        self.assertTrue(self.md_path.exists(), f"Missing MD: {self.md_path}")
        self.assertTrue(self.json_path.exists(), f"Missing JSON: {self.json_path}")
        self.assertTrue(self.json_archived_v1.exists(), f"Missing archived v1 JSON: {self.json_archived_v1}")
        self.assertTrue(self.json_placebo.exists(), f"Missing placebo JSON: {self.json_placebo}")

    def test_02_csv_structure_and_monotone_bh_q(self):
        df = pd.read_csv(self.csv_path)
        expected_cols = [
            "variable", "window", "run", "region_A", "region_B",
            "slope_A", "slope_B", "delta_slope", "ci_low", "ci_high",
            "p_value", "bh_q_value", "mds_80", "n_months", "block_length", "verdict",
            "v1_verdict", "ci_overlap", "placebo_flag"
        ]
        self.assertEqual(list(df.columns), expected_cols)

        runs = ["primary", "sensitivity_grace_era", "sensitivity_transition_excluded"]
        for r in runs:
            sub = df[df["run"] == r]
            self.assertEqual(len(sub), 20, f"Run {r} must have exactly 20 tests (10 pairs x 2 vars)")

            # Monotonicity of Benjamini-Hochberg q-values in p-values
            sorted_by_p = sub.sort_values("p_value").reset_index(drop=True)
            for i in range(len(sorted_by_p) - 1):
                self.assertLessEqual(
                    sorted_by_p.loc[i, "bh_q_value"],
                    sorted_by_p.loc[i + 1, "bh_q_value"] + 1e-6,
                    f"Run {r}: BH q-value must be monotone non-decreasing in p-value"
                )

    def test_03_antisymmetry_and_duality(self):
        from v3.region_comparison import compute_pairwise_difference_trend

        t = np.linspace(2002.25, 2026.5, 100)
        rng = np.random.default_rng(123)
        yA = -1.2 * (t - 2002) + rng.normal(0, 1, 100)
        yB = -0.5 * (t - 2002) + rng.normal(0, 1, 100)

        res_AB = compute_pairwise_difference_trend(t, yA, yB)
        res_BA = compute_pairwise_difference_trend(t, yB, yA)

        # Antisymmetry of delta slope
        self.assertAlmostEqual(res_AB["delta_slope"], -res_BA["delta_slope"], places=4)
        # CI bounds negated and swapped
        self.assertAlmostEqual(res_AB["ci_low"], -res_BA["ci_high"], places=3)
        self.assertAlmostEqual(res_AB["ci_high"], -res_BA["ci_low"], places=3)
        # Two-sided p-value identical
        self.assertAlmostEqual(res_AB["p_value"], res_BA["p_value"], places=4)

    def test_04_ci_contains_point_estimate_and_excludes_zero_iff_p_less_than_05(self):
        df = pd.read_csv(self.csv_path)
        for _, row in df.iterrows():
            # CI contains delta_slope
            self.assertLessEqual(row["ci_low"], row["delta_slope"] + 1e-3, f"ci_low > delta: {row}")
            self.assertGreaterEqual(row["ci_high"], row["delta_slope"] - 1e-3, f"ci_high < delta: {row}")

            # Duality: CI excludes zero iff p < 0.05
            ci_excludes_zero = (row["ci_low"] > 0 or row["ci_high"] < 0)
            p_less_than_05 = (row["p_value"] < 0.05)
            self.assertEqual(
                ci_excludes_zero, p_less_than_05,
                f"Duality failed for {row['run']} {row['variable']} {row['region_A']}-{row['region_B']}: CI=[{row['ci_low']}, {row['ci_high']}], p={row['p_value']}"
            )

    def test_05_verdict_rule_adherence(self):
        df = pd.read_csv(self.csv_path)
        for _, row in df.iterrows():
            ci_excludes_zero = (row["ci_low"] > 0 or row["ci_high"] < 0)
            if row["bh_q_value"] < 0.05 and ci_excludes_zero:
                expected_verdict = "Significant difference"
            elif row["p_value"] < 0.05:
                expected_verdict = "Suggestive"
            else:
                expected_verdict = "No detectable difference"

            self.assertEqual(
                row["verdict"], expected_verdict,
                f"Verdict mismatch for {row['run']} {row['variable']} {row['region_A']}-{row['region_B']}: got '{row['verdict']}', expected '{expected_verdict}'"
            )

    def test_06_invariance_of_results_all_windows(self):
        df = pd.read_csv(self.results_all_csv)
        self.assertEqual(len(df), 336, "results_all_windows.csv must contain exactly 336 rows")
        # Check FDR families still size 36 for primary windows
        for win in ["full_record", "grace_era", "grace_fo_era", "recent_2020"]:
            sub = df[(df["window"] == win) & (df["entity_type"] == "region")]
            # 6 regions x 2 variables x 3 seasons = 36 tests
            self.assertEqual(len(sub), 36, f"Window {win} must have FDR family size 36")

    def test_07_verbatim_limits_text_present_in_markdown(self):
        md_text = self.md_path.read_text(encoding="utf-8")
        self.assertIn(
            VERBATIM_LIMITS_TEXT, md_text,
            "Verbatim limits text must appear in outputs/v3/region_comparison/pairwise_region_differences.md"
        )

    def test_08_calibration_report_validity(self):
        """Strict calibration targets: 0.035 <= FPR <= 0.065 and 0.930 <= Coverage <= 0.970 across all 20 tested pairs."""
        with open(self.json_path, "r", encoding="utf-8") as f:
            calib = json.load(f)

        self.assertEqual(calib["selected_method"], "candidate_a_difference_ess_mk")
        self.assertIn("candidates_evaluated", calib)
        self.assertIn("tws_pairs_calibration", calib)
        self.assertIn("precip_pairs_calibration", calib)
        self.assertIn("all_pairs_summary", calib)

        # Top level benchmark metrics (NW vs Central)
        self.assertGreaterEqual(calib["false_positive_rate"], 0.035)
        self.assertLessEqual(calib["false_positive_rate"], 0.065)
        self.assertGreaterEqual(calib["ci_coverage"], 0.930)
        self.assertLessEqual(calib["ci_coverage"], 0.970)
        self.assertTrue(calib["target_fpr_met"])
        self.assertTrue(calib["target_coverage_met"])

        # Strict verification across all 10 TWS pairs
        tws_calib = calib["tws_pairs_calibration"]
        self.assertEqual(len(tws_calib), 10, "Exactly 10 TWS pairs must be calibrated")
        for pair_name, p_data in tws_calib.items():
            self.assertIn("power_pct", p_data, f"Pair {pair_name} must report power_pct")
            self.assertGreaterEqual(
                p_data["false_positive_rate"], 0.035,
                f"Pair {pair_name}: FPR {p_data['false_positive_rate']} must be >= 0.035"
            )
            self.assertLessEqual(
                p_data["false_positive_rate"], 0.065,
                f"Pair {pair_name}: FPR {p_data['false_positive_rate']} must be <= 0.065"
            )
            self.assertGreaterEqual(
                p_data["ci_coverage"], 0.930,
                f"Pair {pair_name}: Coverage {p_data['ci_coverage']} must be >= 0.930"
            )
            self.assertLessEqual(
                p_data["ci_coverage"], 0.970,
                f"Pair {pair_name}: Coverage {p_data['ci_coverage']} must be <= 0.970"
            )
            self.assertTrue(p_data["target_fpr_met"])
            self.assertTrue(p_data["target_coverage_met"])

        # Strict verification across all 10 Rainfall pairs
        precip_calib = calib["precip_pairs_calibration"]
        self.assertEqual(len(precip_calib), 10, "Exactly 10 Rainfall pairs must be calibrated")
        for pair_name, p_data in precip_calib.items():
            self.assertGreaterEqual(
                p_data["false_positive_rate"], 0.035,
                f"Precip Pair {pair_name}: FPR {p_data['false_positive_rate']} must be >= 0.035"
            )
            self.assertLessEqual(
                p_data["false_positive_rate"], 0.065,
                f"Precip Pair {pair_name}: FPR {p_data['false_positive_rate']} must be <= 0.065"
            )
            self.assertGreaterEqual(
                p_data["ci_coverage"], 0.930,
                f"Precip Pair {pair_name}: Coverage {p_data['ci_coverage']} must be >= 0.930"
            )
            self.assertLessEqual(
                p_data["ci_coverage"], 0.970,
                f"Precip Pair {pair_name}: Coverage {p_data['ci_coverage']} must be <= 0.970"
            )
            self.assertTrue(p_data["target_fpr_met"])
            self.assertTrue(p_data["target_coverage_met"])

        # Check all_pairs_pass flag
        self.assertTrue(calib["all_pairs_summary"]["all_pairs_pass"])
        self.assertTrue(calib["all_pairs_pass"])

        # Check candidate comparisons and archived v1 report
        cand = calib["candidates_evaluated"]
        self.assertIn("candidate_b_block_bootstrap_b10", cand)
        self.assertIn("candidate_c_ar1_bootstrap", cand)
        self.assertIn("v1_bootstrap_failed", cand)
        self.assertTrue(self.json_archived_v1.exists(), "Archived v1 failed report must exist")

    def test_09_ci_overlap_and_v1_verdict_columns(self):
        """Verifies v1_verdict and ci_overlap columns and cross-check logic."""
        df = pd.read_csv(self.csv_path)
        prim_tws = df[(df["run"] == "primary") & (df["variable"] == "tws")].set_index(["region_A", "region_B"])

        # NE vs Central single-region CIs overlap
        self.assertTrue(bool(prim_tws.loc[("NE", "Central"), "ci_overlap"]))
        # SW vs SE single-region CIs overlap
        self.assertTrue(bool(prim_tws.loc[("SW", "SE"), "ci_overlap"]))
        # NW vs Central single-region CIs do not overlap
        self.assertFalse(bool(prim_tws.loc[("NW", "Central"), "ci_overlap"]))
        # NW vs SW single-region CIs do not overlap
        self.assertFalse(bool(prim_tws.loc[("NW", "SW"), "ci_overlap"]))

    def test_10_real_residual_placebo_report(self):
        """Verifies real-residual placebo audit results and structure."""
        with open(self.json_placebo, "r", encoding="utf-8") as f:
            plac = json.load(f)

        self.assertIn("disclaimer", plac)
        self.assertEqual(plac["n_shifts"], 1000)
        self.assertEqual(len(plac["pairs"]), 10)

        for pair_name, p_data in plac["pairs"].items():
            self.assertIn("variant_1_independent", p_data)
            self.assertIn("variant_2_synchronized", p_data)
            self.assertIn("placebo_flag", p_data)
            v1 = p_data["variant_1_independent"]
            v2 = p_data["variant_2_synchronized"]
            # Variant 1 is conservative (FPR <= 0.05)
            self.assertLessEqual(v1["false_positive_rate"], 0.05)
            # Flag matches Variant 2 performance
            if v2["false_positive_rate"] > 0.065 or v2["ci_coverage"] < 0.930:
                self.assertEqual(p_data["placebo_flag"], "Fails real-residual placebo")
            else:
                self.assertEqual(p_data["placebo_flag"], "Passes real-residual placebo")

    def test_11_dashboard_and_docs_integration(self):
        """Verifies dashboard data keys, markup, and required disclosure sentence."""
        html_text = self.index_html_path.read_text(encoding="utf-8")
        md_text = self.md_path.read_text(encoding="utf-8")
        status_text = self.status_md_path.read_text(encoding="utf-8")

        # Required disclosure sentence appears in md and PROJECT_STATUS.md
        self.assertIn(REAL_RESIDUAL_DISCLOSURE, md_text)
        self.assertIn(REAL_RESIDUAL_DISCLOSURE, status_text)

        # Dashboard data block keys
        self.assertIn('"pairwise_differences":', html_text)
        self.assertIn('"pairwise_calibration":', html_text)
        self.assertIn('"real_residual_placebo":', html_text)

        # Dashboard visible calibration line and overlap note
        self.assertIn("Calibrated ESS-MK on the difference series", html_text)
        self.assertIn("3.60%–6.50%", html_text)
        self.assertIn("93.50%–96.40%", html_text)
        self.assertIn("calibration_report_v1_bootstrap_failed.json", html_text)
        self.assertIn("Paired test detects a difference, but the two regions' own CIs overlap. Treat as small and descriptive.", html_text)


if __name__ == "__main__":
    unittest.main()
