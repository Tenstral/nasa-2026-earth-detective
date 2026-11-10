"""
Unit test for literature alignment evaluation report integrity
=============================================================
Validates:
1. National rainfall slope and CI quoted in literature_alignment_evaluation.md
   match outputs/v3/full_record/results_all_windows.csv to two decimal places (+2.04 mm/yr, CI [-7.70, +12.45]).
2. The string 'n = 76' does not appear anywhere in the document.
"""

import unittest
from pathlib import Path
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestLiteratureAlignmentReport(unittest.TestCase):

    def setUp(self):
        self.report_path = REPO_ROOT / "outputs" / "v3" / "benchmark" / "literature_alignment_evaluation.md"
        self.csv_path = REPO_ROOT / "outputs" / "v3" / "full_record" / "results_all_windows.csv"
        self.assertTrue(self.report_path.exists(), "literature_alignment_evaluation.md must exist")
        self.assertTrue(self.csv_path.exists(), "results_all_windows.csv must exist")
        self.report_text = self.report_path.read_text(encoding="utf-8")
        self.df = pd.read_csv(self.csv_path)

    def test_no_n_76_string(self):
        """Assert the outdated string 'n = 76' does not appear in the report."""
        self.assertNotIn("n = 76", self.report_text, "Found forbidden outdated string 'n = 76'")

    def test_national_rainfall_matches_csv_to_two_decimals(self):
        """Assert national rainfall slope and CI match results_all_windows.csv to 2 decimals."""
        nat_precip = self.df[
            (self.df["window"] == "full_record") &
            (self.df["entity"] == "National") &
            (self.df["variable"] == "precip")
        ].iloc[0]

        slope_str = f"+{nat_precip['slope']:.2f}" if nat_precip['slope'] >= 0 else f"{nat_precip['slope']:.2f}"
        ci_low_str = f"{nat_precip['slope_ci_low']:.2f}"
        ci_high_str = f"+{nat_precip['slope_ci_high']:.2f}" if nat_precip['slope_ci_high'] >= 0 else f"{nat_precip['slope_ci_high']:.2f}"

        expected_pattern = f"{slope_str} mm/yr; CI: [{ci_low_str}, {ci_high_str}]"
        self.assertIn(
            expected_pattern,
            self.report_text,
            f"Expected national rainfall pattern '{expected_pattern}' not found in report"
        )


if __name__ == "__main__":
    unittest.main()
