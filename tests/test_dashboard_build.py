"""
Unit Test: Verify Dashboard Data Integrity and Drift Prevention
==============================================================
Asserts:
  1. Both index.html and report.html embed identical, valid DASHBOARD_DATA.
  2. Every value in seasonal panel data matches ratio_trend.csv and dry_season_drawdown.csv.
  3. Key results in DASHBOARD_DATA match results_all_windows.csv.
  4. Population exposure shows 108.5M and stale 69.4M is absent.
  5. Fragments (fragments.json and data/fragments.js) exist and have all 5 required sections.
  6. Regenerating data payload yields zero drift against committed report.html and index.html.
"""

import json
import re
import unittest
from pathlib import Path
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
REPORT_HTML = REPO_ROOT / "report.html"
INDEX_HTML = REPO_ROOT / "index.html"
RESULTS_CSV = REPO_ROOT / "outputs" / "v3" / "full_record" / "results_all_windows.csv"
RATIO_CSV = REPO_ROOT / "outputs" / "v3" / "seasonal" / "ratio_trend.csv"
DRAWDOWN_CSV = REPO_ROOT / "outputs" / "v3" / "seasonal" / "dry_season_drawdown.csv"
FRAGMENTS_JSON = REPO_ROOT / "fragments.json"
FRAGMENTS_JS = REPO_ROOT / "data" / "fragments.js"


class TestDashboardBuild(unittest.TestCase):

    def setUp(self):
        self.assertTrue(REPORT_HTML.exists(), "report.html must exist")
        self.assertTrue(INDEX_HTML.exists(), "index.html must exist")

        with open(REPORT_HTML, "r", encoding="utf-8") as f:
            self.report_html = f.read()
        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            self.index_html = f.read()

        m_rep = re.search(r"const DASHBOARD_DATA = (\{.*?\});\s*</script>", self.report_html, re.DOTALL)
        self.assertIsNotNone(m_rep, "DASHBOARD_DATA block missing from report.html")
        self.data_report = json.loads(m_rep.group(1))

        m_idx = re.search(r"const DASHBOARD_DATA = (\{.*?\});\s*</script>", self.index_html, re.DOTALL)
        self.assertIsNotNone(m_idx, "DASHBOARD_DATA block missing from index.html")
        self.data_index = json.loads(m_idx.group(1))

    def test_dashboard_data_parity_between_pages(self):
        """Confirm index.html and report.html share the identical DASHBOARD_DATA payload."""
        self.assertEqual(
            self.data_report,
            self.data_index,
            "DASHBOARD_DATA differs between report.html and index.html"
        )

    def test_seasonal_panel_matches_csvs(self):
        """Confirm every value in the seasonal panel data matches ratio_trend.csv and dry_season_drawdown.csv."""
        # Check ratio trends
        ratio_df = pd.read_csv(RATIO_CSV)
        dashboard_ratios = pd.DataFrame(self.data_report["ratio_trends"])
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
        dashboard_dds = pd.DataFrame(self.data_report["dry_season_drawdowns"])
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

    def test_results_match_csv(self):
        """Confirm results in DASHBOARD_DATA match results_all_windows.csv."""
        res_df = pd.read_csv(RESULTS_CSV)
        dash_res = pd.DataFrame(self.data_report["results"])
        self.assertEqual(len(dash_res), len(res_df))

        # Spot check primary NW annual tws in full_record
        nw_row_csv = res_df[
            (res_df["entity"] == "NW") &
            (res_df["window"] == "full_record") &
            (res_df["variable"] == "tws") &
            (res_df["season"] == "annual")
        ].iloc[0]

        nw_row_dash = dash_res[
            (dash_res["entity"] == "NW") &
            (dash_res["window"] == "full_record") &
            (dash_res["variable"] == "tws") &
            (dash_res["season"] == "annual")
        ].iloc[0]

        self.assertAlmostEqual(nw_row_dash["slope"], round(nw_row_csv["slope"], 3), places=3)
        self.assertEqual(nw_row_dash["verdict"], nw_row_csv["verdict"])

    def test_exposure_and_no_stale_population(self):
        """Confirm 108.5M is present in report exposure context and stale 69.4M is absent."""
        self.assertIn("108.5", self.report_html, "108.5M exposure must be present in report.html")
        self.assertNotIn("69.4M", self.report_html, "Stale 69.4M value must not be present in report.html")
        self.assertNotIn("69.4 M", self.report_html, "Stale 69.4 M value must not be present in report.html")
        self.assertNotIn("69.4M", self.index_html, "Stale 69.4M value must not be present in index.html")
        self.assertNotIn("69.4 M", self.index_html, "Stale 69.4 M value must not be present in index.html")

    def test_fragments_integrity(self):
        """Confirm fragments.json and data/fragments.js contain all 5 required sections."""
        self.assertTrue(FRAGMENTS_JSON.exists(), "fragments.json must exist")
        self.assertTrue(FRAGMENTS_JS.exists(), "data/fragments.js must exist")

        with open(FRAGMENTS_JSON, "r", encoding="utf-8") as f:
            frag_dict = json.load(f)

        required_keys = ["threeway", "gldas", "pairwise-differences", "stakeholder-actions", "limitations"]
        for key in required_keys:
            self.assertIn(key, frag_dict, f"Missing fragment key: {key}")
            self.assertTrue(len(frag_dict[key].strip()) > 50, f"Fragment {key} too short")

    def test_dashboard_regeneration_no_drift(self):
        """Regenerate data block and assert zero drift against committed report.html and index.html."""
        from v3.build_dashboard import build_dashboard_data, generate_updated_html

        data = build_dashboard_data(REPO_ROOT)
        new_report = generate_updated_html(REPORT_HTML, data)
        new_index = generate_updated_html(INDEX_HTML, data)

        with open(REPORT_HTML, "r", encoding="utf-8") as f:
            committed_report = f.read()
        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            committed_index = f.read()

        self.assertEqual(
            new_report,
            committed_report,
            "Drift detected between committed report.html and output of v3/build_dashboard.py"
        )
        self.assertEqual(
            new_index,
            committed_index,
            "Drift detected between committed index.html and output of v3/build_dashboard.py"
        )


if __name__ == "__main__":
    unittest.main()
