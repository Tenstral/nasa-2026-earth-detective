"""
Unit and Integration Tests for Exploratory Seasonal Extensions
==============================================================
Verifies:
  1. Existence and structure of ratio_trend.csv and dry_season_drawdown.csv.
  2. Every confidence interval contains the estimated Theil-Sen slope.
  3. Duality property: CI excludes zero if and only if p < 0.05.
  4. results_all_windows.csv integrity: exactly 336 rows, FDR family size 36, unaffected by new analyses.
  5. Sensitivity runs have fewer or equal observations than the main run.
  6. Required verbatim limits text is present in the markdown reports.
  7. Zero forbidden phrases appear in the new seasonal outputs.
"""

import re
import unittest
from pathlib import Path
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
SEASONAL_DIR = REPO_ROOT / "outputs" / "v3" / "seasonal"
RESULTS_CSV = REPO_ROOT / "outputs" / "v3" / "full_record" / "results_all_windows.csv"

FORBIDDEN_PATTERNS = [
    (r"\bflat\b", "flat"),
    (r"\bCorrected to Flat\b", "Corrected to Flat"),
    (r"\bHydrologically Steady\b", "Hydrologically Steady"),
    (r"\bprov(ing|en|es)\b", "proving/proven/proves"),
    (r"\bdespite normal rainfall\b", "despite normal rainfall"),
    (r"\bparadox\w*\b", "paradox"),
    (r"\bcannot be attributed\b", "cannot be attributed"),
    (r"\bcompletely decoupled\b", "completely decoupled"),
    (r"\bdisproving\b", "disproving"),
    (r"\bcorroborat\w*", "corroborat*"),
    (r"\bdemonstrat\w*", "demonstrat*"),
    (r"\bconfirmed\b", "confirmed"),
    (r"\bconcentrated in\b", "concentrated in"),
    (r"\brecharge efficiency\b", "recharge efficiency"),
    (r"\bcaused by\b", "caused by"),
    (r"\bdriven by\b", "driven by"),
    (r"\bbecause of pumping\b", "because of pumping"),
    (r"\baquifers?\b", "aquifer"),
]


class TestV3SeasonalExtensions(unittest.TestCase):

    def setUp(self):
        self.ratio_csv = SEASONAL_DIR / "ratio_trend.csv"
        self.ratio_md = SEASONAL_DIR / "ratio_trend.md"
        self.drawdown_csv = SEASONAL_DIR / "dry_season_drawdown.csv"
        self.drawdown_md = SEASONAL_DIR / "dry_season_drawdown.md"

    def test_files_exist(self):
        """1. Verify new seasonal output files exist."""
        self.assertTrue(self.ratio_csv.exists(), "Missing ratio_trend.csv")
        self.assertTrue(self.ratio_md.exists(), "Missing ratio_trend.md")
        self.assertTrue(self.drawdown_csv.exists(), "Missing dry_season_drawdown.csv")
        self.assertTrue(self.drawdown_md.exists(), "Missing dry_season_drawdown.md")

    def test_ci_contains_slope_and_duality_ratio(self):
        """2 & 3. In ratio_trend.csv: CI contains slope; CI excludes zero iff p < 0.05."""
        df = pd.read_csv(self.ratio_csv)
        self.assertGreaterEqual(len(df), 12, "Expected at least 12 rows (6 regions x 2 analysis types)")

        for _, row in df.iterrows():
            slope = row["slope_pct_yr"]
            ci_low = row["slope_ci_low_pct_yr"]
            ci_high = row["slope_ci_high_pct_yr"]
            p_val = row["p_value"]

            # CI contains slope
            self.assertLessEqual(ci_low, slope + 1e-6, f"Slope {slope} below CI low {ci_low} for {row['region']} ({row['analysis_type']})")
            self.assertGreaterEqual(ci_high, slope - 1e-6, f"Slope {slope} above CI high {ci_high} for {row['region']} ({row['analysis_type']})")

            # Duality property: CI excludes zero iff p < 0.05
            ci_excludes_zero = (ci_low > 0 or ci_high < 0)
            p_is_sig = (p_val < 0.05)
            self.assertEqual(ci_excludes_zero, p_is_sig,
                             f"Duality failure for {row['region']} ({row['analysis_type']}): p={p_val}, CI=[{ci_low}, {ci_high}]")

    def test_ci_contains_slope_and_duality_drawdown(self):
        """2 & 3. In dry_season_drawdown.csv: CI contains slope; CI excludes zero iff p < 0.05."""
        df = pd.read_csv(self.drawdown_csv)
        self.assertGreaterEqual(len(df), 12, "Expected at least 12 rows (6 regions x 2 analysis types)")

        for _, row in df.iterrows():
            slope = row["drawdown_slope_cm_yr"]
            ci_low = row["drawdown_ci_low_cm_yr"]
            ci_high = row["drawdown_ci_high_cm_yr"]
            p_val = row["p_value"]

            # CI contains slope
            self.assertLessEqual(ci_low, slope + 1e-6, f"Slope {slope} below CI low {ci_low} for {row['region']} ({row['analysis_type']})")
            self.assertGreaterEqual(ci_high, slope - 1e-6, f"Slope {slope} above CI high {ci_high} for {row['region']} ({row['analysis_type']})")

            # Duality property: CI excludes zero iff p < 0.05
            ci_excludes_zero = (ci_low > 0 or ci_high < 0)
            p_is_sig = (p_val < 0.05)
            self.assertEqual(ci_excludes_zero, p_is_sig,
                             f"Duality failure for {row['region']} ({row['analysis_type']}): p={p_val}, CI=[{ci_low}, {ci_high}]")

    def test_results_all_windows_unaffected(self):
        """4. Verify results_all_windows.csv row count is exactly 336 and FDR family size is 36."""
        self.assertTrue(RESULTS_CSV.exists(), "results_all_windows.csv must exist")
        df = pd.read_csv(RESULTS_CSV)
        self.assertEqual(len(df), 336, f"Expected exactly 336 rows in results_all_windows.csv, found {len(df)}")

        non_null_fdr = df["fdr_family_size_m"].dropna()
        self.assertTrue(all(non_null_fdr == 36.0), "All valid FDR family sizes in results_all_windows.csv must be 36")

    def test_sensitivity_run_sample_sizes(self):
        """5. Verify sensitivity run has fewer or equal observations than the main run."""
        ratio_df = pd.read_csv(self.ratio_csv)
        for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
            sub_main = ratio_df[(ratio_df["region"] == reg) & (ratio_df["analysis_type"] == "main_run")]
            sub_sens = ratio_df[(ratio_df["region"] == reg) & (ratio_df["analysis_type"] == "sensitivity_buffer_excluded")]
            self.assertEqual(len(sub_main), 1)
            self.assertEqual(len(sub_sens), 1)
            self.assertLessEqual(sub_sens.iloc[0]["n_seasons"], sub_main.iloc[0]["n_seasons"],
                                 f"Sensitivity n_seasons > main n_seasons for ratio {reg}")

        drawdown_df = pd.read_csv(self.drawdown_csv)
        for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
            sub_main = drawdown_df[(drawdown_df["region"] == reg) & (drawdown_df["analysis_type"] == "main_run")]
            sub_sens = drawdown_df[(drawdown_df["region"] == reg) & (drawdown_df["analysis_type"] == "sensitivity_buffer_excluded")]
            self.assertEqual(len(sub_main), 1)
            self.assertEqual(len(sub_sens), 1)
            self.assertLessEqual(sub_sens.iloc[0]["n_years"], sub_main.iloc[0]["n_years"],
                                 f"Sensitivity n_years > main n_years for drawdown {reg}")

    def test_required_limits_text_present(self):
        """6. Verify required verbatim limits text appears in dry_season_drawdown.md."""
        content = self.drawdown_md.read_text(encoding="utf-8")
        required_text = (
            "Gravimetry measures total water storage (groundwater, soil moisture and surface water together). "
            "This analysis shows regional patterns that are consistent with dry-season agricultural water use "
            "but does not attribute them to irrigation pumping. Testing that would require metered pumping or "
            "electricity records (BMDA), BWDB well hydrographs, or irrigated-area mapping."
        )
        self.assertIn(required_text, content, "Verbatim limits text missing from dry_season_drawdown.md")

    def test_zero_forbidden_phrases_in_seasonal_outputs(self):
        """7. Verify zero forbidden phrases appear in outputs/v3/seasonal/."""
        target_files = [self.ratio_csv, self.ratio_md, self.drawdown_csv, self.drawdown_md]
        for fpath in target_files:
            text = fpath.read_text(encoding="utf-8", errors="ignore")
            for pattern, label in FORBIDDEN_PATTERNS:
                matches = list(re.finditer(pattern, text, re.IGNORECASE))
                self.assertEqual(len(matches), 0, f"Found forbidden phrase '{label}' in {fpath.name}: {[m.group(0) for m in matches]}")


    def test_verdict_labels_follow_project_rule(self):
        """8. Verify every verdict follows: Significant if q < 0.05 and CI excludes 0; Suggestive if raw p < 0.05; else No detectable trend."""
        # Test ratio_trend.csv
        ratio_df = pd.read_csv(self.ratio_csv)
        for _, row in ratio_df.iterrows():
            p_val = row["p_value"]
            q_val = row["exploratory_fdr_q"]
            ci_low = row["slope_ci_low_pct_yr"]
            ci_high = row["slope_ci_high_pct_yr"]
            ci_excludes_zero = (ci_low > 0 or ci_high < 0)
            verdict = row["verdict"]

            if q_val < 0.05 and ci_excludes_zero:
                expected = "Exploratory: trend detected"
            elif p_val < 0.05:
                expected = "Suggestive"
            else:
                expected = "No detectable trend"

            self.assertEqual(verdict, expected,
                             f"Ratio verdict mismatch for {row['region']} ({row['analysis_type']}): got '{verdict}', expected '{expected}' (p={p_val}, q={q_val})")

        # Test dry_season_drawdown.csv
        drawdown_df = pd.read_csv(self.drawdown_csv)
        for _, row in drawdown_df.iterrows():
            p_val = row["p_value"]
            q_val = row["exploratory_fdr_q"]
            ci_low = row["drawdown_ci_low_cm_yr"]
            ci_high = row["drawdown_ci_high_cm_yr"]
            ci_excludes_zero = (ci_low > 0 or ci_high < 0)
            verdict = row["verdict"]

            if q_val < 0.05 and ci_excludes_zero:
                expected = "Exploratory: trend detected"
            elif p_val < 0.05:
                expected = "Suggestive"
            else:
                expected = "No detectable trend"

            self.assertEqual(verdict, expected,
                             f"Drawdown verdict mismatch for {row['region']} ({row['analysis_type']}): got '{verdict}', expected '{expected}' (p={p_val}, q={q_val})")

    def test_no_tab_characters_in_outputs_markdown(self):
        """9. Verify no markdown file under outputs/ contains literal tab characters."""
        outputs_dir = REPO_ROOT / "outputs"
        md_files = list(outputs_dir.rglob("*.md"))
        self.assertGreater(len(md_files), 10, "Expected at least 10 markdown files under outputs/")

        for md_path in md_files:
            content = md_path.read_text(encoding="utf-8", errors="ignore")
            tab_count = content.count("\t")
            self.assertEqual(tab_count, 0, f"Found {tab_count} tab character(s) in {md_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    unittest.main()
