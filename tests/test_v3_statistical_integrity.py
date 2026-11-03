"""
NASA Space Apps 2026 – Bengal Hydro Detective
v3 Pipeline Integration and Statistical Integrity Unit Tests
============================================================
Verifies:
  1. All 4 analysis windows (full_record, grace_era, grace_fo_era, recent_2020) exist.
  2. Benjamini-Hochberg FDR q-values >= raw p-values across all results.
  3. GLDAS Noah 2.1 re-baselining: 2004-2009 mean anomaly strictly equals 0.0 cm.
  4. Storage partition residual strictly labeled and physically consistent.
  5. Exposure population and cropland bounds.
  6. Flood event context and crest anomalies.
  7. Gap calibration and independent AR(1) null generator validation pass criteria.
  8. Method consistency: Calibrated ESS-MK applied across all regions, NW recent_2020 labeled method-dependent.
"""

import json
import unittest
import numpy as np
import pandas as pd
import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUTS_V3 = REPO_ROOT / "outputs" / "v3"


class TestV3StatisticalIntegrity(unittest.TestCase):

    def test_windows_and_fdr_monotonicity(self):
        csv_path = OUTPUTS_V3 / "full_record" / "results_all_windows.csv"
        self.assertTrue(csv_path.exists(), f"Missing {csv_path}")
        df = pd.read_csv(csv_path)

        expected_windows = {"full_record", "grace_era", "grace_fo_era", "recent_2020"}
        found_windows = set(df["window"].unique())
        self.assertEqual(expected_windows, found_windows)

        # BH-FDR q-value must be >= raw p-value within rounding tolerance (5 decimal places)
        reg_df = df[df["entity_type"] == "region"].dropna(subset=["bh_fdr_q_value"])
        bad = reg_df[reg_df["bh_fdr_q_value"] < reg_df["p_value"].round(5) - 1e-5]
        self.assertEqual(len(bad), 0, f"Found q < p in results: {bad}")

    def test_gldas_baseline_alignment(self):
        part_path = OUTPUTS_V3 / "gldas_split" / "storage_partition_series.csv"
        self.assertTrue(part_path.exists(), f"Missing {part_path}")
        df = pd.read_csv(part_path)

        for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
            sub = df[df["region"] == reg]
            base_mask = (sub["ym"] >= "2004-01") & (sub["ym"] <= "2009-12")
            self.assertTrue(base_mask.any(), f"No baseline data for {reg}")
            mean_anom = sub.loc[base_mask, "delta_tot_cm"].mean()
            self.assertAlmostEqual(mean_anom, 0.0, places=4, msg=f"Baseline not zero for {reg}")

    def test_residual_calculation_and_label(self):
        part_path = OUTPUTS_V3 / "gldas_split" / "storage_partition_series.csv"
        df = pd.read_csv(part_path)

        # Residual = TWS - Delta Tot
        diff = df["residual_cm"] - (df["grace_tws_cm"] - df["delta_tot_cm"])
        self.assertTrue(np.all(np.abs(diff) < 1e-3))

        # Strict label
        labels = df["residual_label"].unique()
        self.assertEqual(len(labels), 1)
        self.assertEqual(labels[0], "groundwater + surface water + model error residual")

    def test_exposure_integrity(self):
        exp_path = OUTPUTS_V3 / "exposure" / "exposure_table.csv"
        self.assertTrue(exp_path.exists(), f"Missing {exp_path}")
        df = pd.read_csv(exp_path)

        # Cropland fraction between 0% and 100%
        self.assertTrue(all(0.0 <= f <= 100.0 for f in df["cropland_pct_mcd12q1"]))
        # NW has highest cropland fraction
        nw_crop = df[df["region"] == "NW"]["cropland_pct_mcd12q1"].iloc[0]
        self.assertGreater(nw_crop, 70.0)

        # Total population around ~170M
        pop_sum = df[df["region"] != "National"]["pop_millions_2020"].sum()
        self.assertAlmostEqual(pop_sum, 169.8, delta=1.0)

    def test_flood_events_context(self):
        flood_path = OUTPUTS_V3 / "extremes" / "flood_events_context.csv"
        self.assertTrue(flood_path.exists(), f"Missing {flood_path}")
        df = pd.read_csv(flood_path)

        # Severe floods (2004, 2007) should have crest storage > +30 cm, and 2020 > +25 cm
        df_valid = df.dropna(subset=["post_monsoon_peak_cm"])
        peak_2004 = df_valid[df_valid["year"] == 2004]["post_monsoon_peak_cm"].iloc[0]
        peak_2007 = df_valid[df_valid["year"] == 2007]["post_monsoon_peak_cm"].iloc[0]
        peak_2020 = df_valid[df_valid["year"] == 2020]["post_monsoon_peak_cm"].iloc[0]
        self.assertGreater(peak_2004, 30.0)
        self.assertGreater(peak_2007, 30.0)
        self.assertGreater(peak_2020, 25.0)

    def test_gap_calibration_pass_criteria(self):
        calib_path = OUTPUTS_V3 / "full_record" / "gap_calibration_report.json"
        self.assertTrue(calib_path.exists(), f"Missing {calib_path}")
        with open(calib_path, "r", encoding="utf-8") as f:
            report = json.load(f)

        sim = report["calibration_simulation"]
        results_by_phi = sim["results_by_phi"]

        # Absolute pass criteria: FPR in [0.035, 0.065] and CI coverage in [0.930, 0.970]
        for phi_str, res in results_by_phi.items():
            ess = res["ess_corrected_mk"]
            fpr = ess["fpr"]
            cov = ess["ci_coverage_95"]
            self.assertTrue(
                0.035 <= fpr <= 0.065,
                f"ESS-MK FPR {fpr} out of bounds [0.035, 0.065] for phi={phi_str}",
            )
            self.assertTrue(
                0.930 <= cov <= 0.970,
                f"ESS-MK 95% CI coverage {cov} out of bounds [0.930, 0.970] for phi={phi_str}",
            )
            self.assertTrue(
                ess["passed_both_criteria"],
                f"passed_both_criteria is False for phi={phi_str}",
            )

        self.assertTrue(
            sim["method_selection"]["all_empirical_phi_passed"],
            "all_empirical_phi_passed is not True",
        )
        self.assertEqual(
            sim["method_selection"]["selected_primary_method"],
            "ESS-corrected Mann-Kendall with Analytical Theil-Sen Duality",
        )
        self.assertIn("PASSED", sim["method_selection"]["calibration_verdict"])
        self.assertNotIn("FAILED", sim["method_selection"]["calibration_verdict"])

    def test_independent_null_generator_validation(self):
        calib_path = OUTPUTS_V3 / "full_record" / "gap_calibration_report.json"
        self.assertTrue(calib_path.exists(), f"Missing {calib_path}")
        with open(calib_path, "r", encoding="utf-8") as f:
            report = json.load(f)

        indep = report.get("independent_null_generator_audit", {})
        self.assertTrue(len(indep) == 6, f"Expected 6 regions in independent null audit, found {len(indep)}")

        for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
            self.assertIn(reg, indep)
            reg_res = indep[reg]
            ess = reg_res["ess_mk"]
            fpr = ess["fpr"]
            cov = ess["ci_coverage_95"]
            self.assertTrue(
                0.035 <= fpr <= 0.065,
                f"{reg} ESS FPR {fpr} out of bounds [0.035, 0.065]"
            )
            self.assertTrue(
                0.930 <= cov <= 0.970,
                f"{reg} ESS Coverage {cov} out of bounds [0.930, 0.970]"
            )
            self.assertEqual(reg_res["status"], "PASSED")

    def test_method_consistency_and_nw_recent_2020(self):
        csv_path = OUTPUTS_V3 / "full_record" / "results_all_windows.csv"
        df = pd.read_csv(csv_path)

        # 1. Single primary method across all regions
        reg_df = df[df["entity_type"] == "region"]
        methods = reg_df["primary_method"].unique()
        self.assertEqual(len(methods), 1)
        self.assertEqual(methods[0], "Calibrated ESS-MK")

        # 2. Both ESS-MK and Surrogate columns present
        for col in ["slope", "slope_ci_low", "slope_ci_high", "p_value", "surr_slope", "surr_ci_low", "surr_ci_high", "surr_p_value"]:
            self.assertIn(col, df.columns)

        # 3. NW recent_2020 labeled method-dependent and NOT Significant
        nw_2020 = df[(df["window"] == "recent_2020") & (df["entity"] == "NW") & (df["variable"] == "tws") & (df["season"] == "annual")]
        self.assertEqual(len(nw_2020), 1)
        vrd = nw_2020["verdict"].iloc[0]
        self.assertEqual(vrd, "method-dependent")
        self.assertNotEqual(vrd, "Significant")


if __name__ == "__main__":
    unittest.main()
