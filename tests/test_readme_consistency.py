"""
Unit test for README.md consistency against repository data
==========================================================
Validates:
1. Banned outdated strings do not appear in README.md:
   "26.68", "43.01", "v3-expansion", "+1.34", "p = 0.49", "p=0.49",
   "[-1.34, +0.44]", "Infiltration Saturation".
   (Note: "Newey-West" is dropped because v3/offset_test.py uses Newey-West HAC).
2. Regional populations match outputs/v3/exposure/exposure_table.csv within 0.01 M.
3. NW step delta and p-value match outputs/v3/full_record/offset_test.csv.
4. National grace_fo_era CI matches outputs/v3/full_record/results_all_windows.csv.
5. No hard-coded test count (e.g. "\\d+ tests" or "\\d+ passed").
"""

import re
import unittest
from pathlib import Path
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
README_PATH = REPO_ROOT / "README.md"
EXPOSURE_CSV = REPO_ROOT / "outputs" / "v3" / "exposure" / "exposure_table.csv"
OFFSET_CSV = REPO_ROOT / "outputs" / "v3" / "full_record" / "offset_test.csv"
RESULTS_CSV = REPO_ROOT / "outputs" / "v3" / "full_record" / "results_all_windows.csv"


class TestReadmeConsistency(unittest.TestCase):

    def setUp(self):
        self.assertTrue(README_PATH.exists(), "README.md must exist")
        self.readme_text = README_PATH.read_text(encoding="utf-8")

    def test_banned_strings_not_in_readme(self):
        """Assert outdated or contradicted strings do not appear in README.md."""
        banned = [
            "26.68",
            "43.01",
            "v3-expansion",
            "+1.34",
            "p = 0.49",
            "p=0.49",
            "[-1.34, +0.44]",
            "Infiltration Saturation",
        ]
        for term in banned:
            self.assertNotIn(term, self.readme_text, f"Found banned term '{term}' in README.md")

    def test_regional_populations_match_exposure_table(self):
        """Assert regional populations in README match exposure_table.csv within 0.01 M."""
        self.assertTrue(EXPOSURE_CSV.exists(), "exposure_table.csv must exist")
        df_exp = pd.read_csv(EXPOSURE_CSV)

        # Expected populations from file
        for _, row in df_exp.iterrows():
            reg = row["region"]
            if reg == "National":
                continue
            pop_val = row["pop_millions_2020"]
            pop_str = f"{pop_val:.2f}"
            self.assertIn(
                pop_str,
                self.readme_text,
                f"Population for region {reg} ({pop_str}M) not found in README.md"
            )

        # Combined NW + NE + Central total: 108.5M
        sig_regions = df_exp[df_exp["region"].isin(["NW", "NE", "Central"])]
        combined_pop = sig_regions["pop_millions_2020"].sum()
        combined_str = f"{combined_pop:.1f}"
        self.assertIn(
            combined_str,
            self.readme_text,
            f"Combined population ({combined_str}M) not found in README.md"
        )

    def test_nw_step_and_p_value_match_offset_test(self):
        """Assert NW step offset and p-value in README match offset_test.csv."""
        self.assertTrue(OFFSET_CSV.exists(), "offset_test.csv must exist")
        df_off = pd.read_csv(OFFSET_CSV)
        nw_row = df_off[df_off["region"] == "NW"].iloc[0]

        step_val = nw_row["step_delta_cm"]
        p_val = nw_row["step_p_value"]

        # Formats in README: +9.15 cm, p = 0.028
        step_str = f"+{step_val:.2f}"
        p_str = f"{p_val:.3f}"

        self.assertIn(step_str, self.readme_text, f"NW step delta '{step_str}' not found in README.md")
        self.assertIn(p_str, self.readme_text, f"NW step p-value '{p_str}' not found in README.md")

    def test_national_grace_fo_era_ci_matches_results(self):
        """Assert National grace_fo_era CI in README matches results_all_windows.csv."""
        self.assertTrue(RESULTS_CSV.exists(), "results_all_windows.csv must exist")
        df_res = pd.read_csv(RESULTS_CSV)
        nat_gfo = df_res[
            (df_res["window"] == "grace_fo_era") &
            (df_res["entity"] == "National") &
            (df_res["variable"] == "tws") &
            (df_res["season"] == "annual")
        ].iloc[0]

        ci_low = nat_gfo["slope_ci_low"]
        ci_high = nat_gfo["slope_ci_high"]

        expected_ci = f"[{ci_low:.2f}, +{ci_high:.2f}]"
        self.assertIn(
            expected_ci,
            self.readme_text,
            f"National grace_fo_era CI '{expected_ci}' not found in README.md"
        )

    def test_no_hardcoded_test_count(self):
        """Assert README.md does not contain hardcoded test counts (e.g. '14 tests')."""
        match_tests = re.search(r"\b\d+\s+tests\b", self.readme_text, re.IGNORECASE)
        self.assertIsNone(
            match_tests,
            f"Found hardcoded test count in README.md: '{match_tests.group(0) if match_tests else ''}'"
        )
        match_passed = re.search(r"\b\d+\s+passed\b", self.readme_text, re.IGNORECASE)
        self.assertIsNone(
            match_passed,
            f"Found hardcoded passed count in README.md: '{match_passed.group(0) if match_passed else ''}'"
        )


if __name__ == "__main__":
    unittest.main()
