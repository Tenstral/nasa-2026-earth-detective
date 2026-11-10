"""
Unit Test: Verify Dashboard Data Integrity and Drift Prevention
==============================================================
Asserts:
  1. Every value in the dashboard's seasonal panel matches the CSV outputs.
  2. Regenerating the data payload via v3/build_dashboard.py yields byte-identical
     content to committed index.html (drift test).
"""

import json
import re
import unittest
from pathlib import Path
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_HTML = REPO_ROOT / "report.html"
RATIO_CSV = REPO_ROOT / "outputs" / "v3" / "seasonal" / "ratio_trend.csv"
DRAWDOWN_CSV = REPO_ROOT / "outputs" / "v3" / "seasonal" / "dry_season_drawdown.csv"


class TestDashboardBuild(unittest.TestCase):

    def setUp(self):
        self.assertTrue(INDEX_HTML.exists(), "index.html must exist")
        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            html = f.read()

        m = re.search(r"const DASHBOARD_DATA = (\{.*?\});\s*</script>", html, re.DOTALL)
        self.assertIsNotNone(m, "DASHBOARD_DATA block missing from index.html")
        self.data = json.loads(m.group(1))

    def test_seasonal_panel_matches_csvs(self):
        """1. Confirm every value in the seasonal panel data matches ratio_trend.csv and dry_season_drawdown.csv."""
        # Check ratio trends
        ratio_df = pd.read_csv(RATIO_CSV)
        dashboard_ratios = pd.DataFrame(self.data["ratio_trends"])
        self.assertEqual(len(dashboard_ratios), len(ratio_df))

        for _, row in ratio_df.iterrows():
            sub = dashboard_ratios[
                (dashboard_ratios["region"] == row["region"]) &
                (dashboard_ratios["analysis_type"] == row["analysis_type"])
            ]
            self.assertEqual(len(sub), 1, f"Missing ratio entry for {row['region']} {row['analysis_type']}")
            d_row = sub.iloc[0]

            self.assertAlmostEqual(d_row["slope_pct_yr"], row["slope_pct_yr"], places=4)
            self.assertAlmostEqual(d_row["p_value"], row["p_value"], places=4)
            self.assertAlmostEqual(d_row["exploratory_fdr_q"], row["exploratory_fdr_q"], places=4)
            self.assertEqual(d_row["verdict"], row["verdict"])

        # Check dry-season drawdowns
        dd_df = pd.read_csv(DRAWDOWN_CSV)
        dashboard_dds = pd.DataFrame(self.data["dry_season_drawdowns"])
        self.assertEqual(len(dashboard_dds), len(dd_df))

        for _, row in dd_df.iterrows():
            sub = dashboard_dds[
                (dashboard_dds["region"] == row["region"]) &
                (dashboard_dds["analysis_type"] == row["analysis_type"])
            ]
            self.assertEqual(len(sub), 1, f"Missing drawdown entry for {row['region']} {row['analysis_type']}")
            d_row = sub.iloc[0]

            self.assertAlmostEqual(d_row["drawdown_slope_cm_yr"], row["drawdown_slope_cm_yr"], places=4)
            self.assertAlmostEqual(d_row["p_value"], row["p_value"], places=4)
            self.assertAlmostEqual(d_row["exploratory_fdr_q"], row["exploratory_fdr_q"], places=4)
            self.assertEqual(d_row["verdict"], row["verdict"])

    def test_dashboard_regeneration_no_drift(self):
        """2. Regenerate data block and assert zero drift against committed index.html."""
        from v3.build_dashboard import build_dashboard_data, generate_updated_html

        data = build_dashboard_data(REPO_ROOT)
        new_html = generate_updated_html(INDEX_HTML, data)

        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            committed_html = f.read()

        self.assertEqual(
            new_html,
            committed_html,
            "Drift detected between committed index.html and output of v3/build_dashboard.py"
        )


if __name__ == "__main__":
    unittest.main()
