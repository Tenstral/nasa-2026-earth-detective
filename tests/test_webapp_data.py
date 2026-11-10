"""
tests/test_webapp_data.py
=========================
Verifies data integrity, schema consistency, and zero drift between
source CSVs in outputs/v3/ and compiled JavaScript payloads in data/.
"""

import json
import re
import unittest
from pathlib import Path
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"


def load_js_object(js_path: Path, var_name: str) -> dict:
    with open(js_path, "r", encoding="utf-8") as f:
        content = f.read()
    prefix = f"window.ED.{var_name} = "
    idx = content.find(prefix)
    if idx == -1:
        raise ValueError(f"Could not find {prefix} in {js_path}")
    json_str = content[idx + len(prefix):].rstrip()
    if json_str.endswith(";"):
        json_str = json_str[:-1]
    return json.loads(json_str)


class TestWebappData(unittest.TestCase):

    def test_all_data_files_exist(self):
        expected_files = [
            "catalog.js",
            "map.js",
            "presets.js",
            "series_regions.js",
            "series_divisions.js",
            "series_extremes.js",
            "series_aod.js",
        ]
        for fname in expected_files:
            fpath = DATA_DIR / fname
            self.assertTrue(fpath.exists(), f"Missing compiled data file: {fname}")
            self.assertGreater(fpath.stat().st_size, 500, f"File {fname} is unexpectedly small")

    def test_catalog_structure(self):
        catalog = load_js_object(DATA_DIR / "catalog.js", "catalog")
        self.assertIn("variables", catalog)
        self.assertIn("regions", catalog)
        self.assertIn("divisions", catalog)
        self.assertIn("floodEvents", catalog)
        self.assertIn("gapPeriod", catalog)
        self.assertIn("canonicalWindows", catalog)

        var_ids = [v["id"] for v in catalog["variables"]]
        self.assertIn("grace_tws", var_ids)
        self.assertIn("imerg_precip", var_ids)
        self.assertIn("power_precip", var_ids)
        self.assertIn("noah_sms_anom", var_ids)
        self.assertIn("subsurface_residual", var_ids)
        self.assertIn("modis_aod", var_ids)
        self.assertIn("aeronet_aod", var_ids)

        reg_ids = [r["id"] for r in catalog["regions"]]
        self.assertEqual(set(reg_ids), {"NW", "NE", "Central", "SW", "SE", "National"})

        div_ids = [d["id"] for d in catalog["divisions"]]
        self.assertEqual(len(div_ids), 8)

    def test_series_regions_spot_check(self):
        reg_data = load_js_object(DATA_DIR / "series_regions.js", "seriesRegions")
        csv_df = pd.read_csv(REPO_ROOT / "outputs/v3/full_record/region_series_2002_2026.csv")

        # Spot check NW 2002-04
        nw_row = csv_df[(csv_df["region"] == "NW") & (csv_df["ym"] == "2002-04")].iloc[0]
        nw_js = reg_data["NW"]
        idx_2002_04 = nw_js["ym"].index("2002-04")

        self.assertAlmostEqual(nw_js["tws"][idx_2002_04], nw_row["grace_tws_cm"], places=3)
        self.assertAlmostEqual(nw_js["imerg"][idx_2002_04], nw_row["imerg_precip_mm"], places=2)
        self.assertAlmostEqual(nw_js["power"][idx_2002_04], nw_row["power_precip_mm"], places=2)

    def test_presets_match_master_results(self):
        presets = load_js_object(DATA_DIR / "presets.js", "presets")
        res_df = pd.read_csv(REPO_ROOT / "outputs/v3/full_record/results_all_windows.csv")

        # Check NW full_record tws
        row = res_df[
            (res_df["window"] == "full_record") &
            (res_df["entity"] == "NW") &
            (res_df["variable"] == "tws") &
            (res_df["season"] == "annual")
        ].iloc[0]

        preset_key = "full_record_NW_tws"
        self.assertIn(preset_key, presets)
        p_item = presets[preset_key]

        self.assertAlmostEqual(p_item["slope"], row["slope"], places=4)
        self.assertAlmostEqual(p_item["slope_ci_low"], row["slope_ci_low"], places=4)
        self.assertAlmostEqual(p_item["slope_ci_high"], row["slope_ci_high"], places=4)
        self.assertEqual(p_item["verdict"], row["verdict"])

    def test_extremes_series_spot_check(self):
        ext_data = load_js_object(DATA_DIR / "series_extremes.js", "seriesExtremes")
        self.assertIn("NW", ext_data)
        nw_ext = ext_data["NW"]
        self.assertGreater(len(nw_ext), 20)
        item_2003 = [x for x in nw_ext if x["year"] == 2003][0]
        self.assertEqual(item_2003["annual_total_mm"], 2296.2)
        self.assertEqual(item_2003["days_ge_50mm"], 3)


if __name__ == "__main__":
    unittest.main()
