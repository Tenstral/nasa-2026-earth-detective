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
"""

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
        bad = df[df["bh_fdr_q_value"] < df["p_value"].round(5) - 1e-5]
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


if __name__ == "__main__":
    unittest.main()
