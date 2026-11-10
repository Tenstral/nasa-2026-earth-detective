"""
v3/build_dashboard.py
=====================
Programmatically extracts and compiles all project datasets from CSV, JSON, and GeoJSON
sources and injects the compiled DASHBOARD_DATA payload into index.html.

Sources:
  1. bangladesh_divisions.geojson (SVG paths & division centroids)
  2. outputs/v3/full_record/region_series_2002_2026.csv
  3. outputs/v3/full_record/division_series_2002_2026.csv
  4. outputs/v3/gldas_split/storage_partition_series_multi_model.csv
  5. outputs/v3/full_record/results_all_windows.csv (336 tests)
  6. outputs/v3/full_record/three_way_slopes_and_transition.csv
  7. outputs/v3/gldas_split/gldas_multi_model_summary.csv
  8. outputs/v3/exposure/exposure_table.csv
  9. outputs/v3/extremes/flood_events_context.csv
 10. outputs/v3/full_record/gap_calibration_report.json
 11. outputs/v3/seasonal/ratio_trend.csv
 12. outputs/v3/seasonal/dry_season_drawdown.csv
"""

import json
import re
from pathlib import Path
import numpy as np
import pandas as pd
import shapely.geometry

REPO_ROOT = Path(__file__).resolve().parent.parent


def build_dashboard_data(repo_root: Path = REPO_ROOT) -> dict:
    """Reads all primary data files and compiles structured dictionary for DASHBOARD_DATA."""
    # 1. GeoJSON and SVG paths
    geojson_path = repo_root / "bangladesh_divisions.geojson"
    with open(geojson_path, "r", encoding="utf-8") as f:
        gj = json.load(f)

    min_lon, max_lon = 88.0, 92.7
    min_lat, max_lat = 20.5, 26.7
    width, height = 600, 750

    def project(lon, lat):
        x = (lon - min_lon) / (max_lon - min_lon) * width
        y = (max_lat - lat) / (max_lat - min_lat) * height
        return round(x, 1), round(y, 1)

    svg_paths = {}
    div_centers = {}

    for feat in gj["features"]:
        name = feat["properties"]["name"]
        raw_geom = shapely.geometry.shape(feat["geometry"])
        geom = raw_geom.simplify(0.012, preserve_topology=True)

        c = raw_geom.centroid
        cx, cy = project(c.x, c.y)
        div_centers[name] = {"x": cx, "y": cy}

        if geom.geom_type == "Polygon":
            polys = [geom]
        elif geom.geom_type == "MultiPolygon":
            polys = list(geom.geoms)
        else:
            polys = []

        path_d = []
        for poly in polys:
            coords = list(poly.exterior.coords)
            if len(coords) < 3:
                continue
            p0 = project(coords[0][0], coords[0][1])
            d = [f"M {p0[0]},{p0[1]}"]
            for pt in coords[1:]:
                p = project(pt[0], pt[1])
                d.append(f"L {p[0]},{p[1]}")
            d.append("Z")
            path_d.append(" ".join(d))
        svg_paths[name] = " ".join(path_d)

    # 2. Regional and Divisional Series
    reg_df = pd.read_csv(repo_root / "outputs/v3/full_record/region_series_2002_2026.csv")
    div_df = pd.read_csv(repo_root / "outputs/v3/full_record/division_series_2002_2026.csv")

    div_df["Division"] = div_df["Division"].str.strip()
    div_df["year"] = div_df["ym"].str.slice(0, 4).astype(int)
    div_df["month"] = div_df["ym"].str.slice(5, 7).astype(int)

    div_annual = {}
    for div, grp in div_df.groupby("Division"):
        div_annual[div] = {}
        for yr, ygrp in grp.groupby("year"):
            tws_mean = ygrp["grace_tws_cm"].mean()
            tws_val = round(float(tws_mean), 2) if not np.isnan(tws_mean) else None
            pr_sum = ygrp["imerg_precip_mm"].sum()
            pr_val = round(float(pr_sum), 1) if not np.isnan(pr_sum) else None
            div_annual[div][str(yr)] = {
                "tws": tws_val,
                "precip": pr_val,
                "n_months": int(ygrp["grace_tws_cm"].notna().sum()),
            }

    div_monthly = {}
    for div, grp in div_df.groupby("Division"):
        div_monthly[div] = {
            "ym": grp["ym"].tolist(),
            "tws": [round(float(v), 2) if not np.isnan(v) else None for v in grp["grace_tws_cm"]],
            "precip": [round(float(v), 1) if not np.isnan(v) else None for v in grp["imerg_precip_mm"]],
        }

    reg_monthly = {}
    for reg, grp in reg_df.groupby("region"):
        reg_monthly[reg] = {
            "ym": grp["ym"].tolist(),
            "tws": [round(float(v), 2) if not np.isnan(v) else None for v in grp["grace_tws_cm"]],
            "imerg": [round(float(v), 1) if not np.isnan(v) else None for v in grp["imerg_precip_mm"]],
            "power": [round(float(v), 1) if not np.isnan(v) else None for v in grp["power_precip_mm"]],
        }

    # 3. GLDAS Multi-Model Partition Series
    part_df = pd.read_csv(repo_root / "outputs/v3/gldas_split/storage_partition_series_multi_model.csv")
    part_series = {}
    for reg, grp in part_df.groupby("region"):
        part_series[reg] = {
            "ym": grp["ym"].tolist(),
            "tws": [round(float(v), 2) if not np.isnan(v) else None for v in grp["grace_tws_cm"]],
            "noah_sms": [round(float(v), 2) if not np.isnan(v) else None for v in grp["noah_sms_anom_cm"]],
            "vic_sms": [round(float(v), 2) if not np.isnan(v) else None for v in grp["vic_sms_anom_cm"]],
            "clsm_sms": [round(float(v), 2) if not np.isnan(v) else None for v in grp["clsm_sms_anom_cm"]],
            "noah_res": [round(float(v), 2) if not np.isnan(v) else None for v in grp["noah_residual_cm"]],
            "vic_res": [round(float(v), 2) if not np.isnan(v) else None for v in grp["vic_residual_cm"]],
            "clsm_res": [round(float(v), 2) if not np.isnan(v) else None for v in grp["clsm_residual_cm"]],
        }

    # 4. Results Table (all 336 tests)
    res_df = pd.read_csv(repo_root / "outputs/v3/full_record/results_all_windows.csv")
    res_clean = res_df[[
        "window", "entity", "entity_type", "variable", "season", "slope",
        "slope_ci_low", "slope_ci_high", "p_value", "bh_fdr_q_value", "verdict", "primary_method"
    ]].copy()
    res_clean["p_value"] = res_clean["p_value"].apply(lambda p: "< 0.0001" if p < 0.0001 else f"{p:.4f}")
    res_clean["bh_fdr_q_value"] = res_clean["bh_fdr_q_value"].apply(
        lambda q: "< 0.0001" if (pd.notna(q) and q < 0.0001) else (f"{q:.4f}" if pd.notna(q) else "—")
    )
    res_clean["slope"] = res_clean["slope"].round(3)
    res_clean["slope_ci_low"] = res_clean["slope_ci_low"].round(3)
    res_clean["slope_ci_high"] = res_clean["slope_ci_high"].round(3)

    # 5. Three-Way Slopes Table
    three_way_df = pd.read_csv(repo_root / "outputs/v3/full_record/three_way_slopes_and_transition.csv")

    # 6. GLDAS Summary Table
    gldas_sum_df = pd.read_csv(repo_root / "outputs/v3/gldas_split/gldas_multi_model_summary.csv")
    gldas_clean = gldas_sum_df[[
        "window", "region", "tws_slope_cm_yr", "noah_sms_slope", "vic_sms_slope",
        "independent_sms_range", "independent_residual_range", "clsm_sms_slope", "clsm_residual_slope"
    ]].copy()

    # 7. Exposure Table
    exp_df = pd.read_csv(repo_root / "outputs/v3/exposure/exposure_table.csv")
    exp_clean = exp_df[[
        "region", "pop_millions_2020", "pop_share_pct", "cropland_pct_mcd12q1",
        "total_agricultural_pct", "tws_slope_cm_yr", "tws_ci_95", "tws_verdict", "exposure_narrative"
    ]].copy()

    # 8. Flood Table
    flood_df = pd.read_csv(repo_root / "outputs/v3/extremes/flood_events_context.csv")

    # 9. Calibration & Detection Limits (MDS)
    with open(repo_root / "outputs/v3/full_record/gap_calibration_report.json", "r", encoding="utf-8") as f:
        gap_calib = json.load(f)
    mds_by_window = gap_calib.get("regional_power_and_mds_by_window", {})

    # 10. Exploratory Seasonal Extensions (Ratio Trends & Dry-Season Drawdown)
    ratio_trend_df = pd.read_csv(repo_root / "outputs/v3/seasonal/ratio_trend.csv")
    drawdown_df = pd.read_csv(repo_root / "outputs/v3/seasonal/dry_season_drawdown.csv")

    # 11. Pairwise Between-Region Differences
    pairwise_csv = repo_root / "outputs/v3/region_comparison/pairwise_region_differences.csv"
    pairwise_data = []
    if pairwise_csv.exists():
        pairwise_df = pd.read_csv(pairwise_csv)
        pairwise_data = pairwise_df.to_dict(orient="records")

    compiled = {
        "svg_paths": svg_paths,
        "div_centers": div_centers,
        "years": list(range(2002, 2027)),
        "div_annual": div_annual,
        "div_monthly": div_monthly,
        "reg_monthly": reg_monthly,
        "part_series": part_series,
        "results": res_clean.to_dict(orient="records"),
        "three_way": three_way_df.to_dict(orient="records"),
        "gldas_summary": gldas_clean.to_dict(orient="records"),
        "exposure": exp_clean.to_dict(orient="records"),
        "floods": flood_df.to_dict(orient="records"),
        "mds_by_window": mds_by_window,
        "ratio_trends": ratio_trend_df.to_dict(orient="records"),
        "dry_season_drawdowns": drawdown_df.to_dict(orient="records"),
        "pairwise_differences": pairwise_data,
    }
    return compiled


def sanitize_nans(obj):
    """Recursively replaces NaN float values with None for compliant JSON serialization."""
    if isinstance(obj, float) and (np.isnan(obj) or np.isneginf(obj) or np.isposinf(obj)):
        return None
    elif isinstance(obj, dict):
        return {k: sanitize_nans(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_nans(v) for v in obj]
    return obj


def generate_updated_html(index_html_path: Path, data: dict) -> str:
    """Replaces DASHBOARD_DATA in index.html with new JSON data block."""
    with open(index_html_path, "r", encoding="utf-8") as f:
        content = f.read()

    m = re.search(r"const DASHBOARD_DATA = \{.*?\};\s*</script>", content, re.DOTALL)
    if not m:
        raise ValueError("Could not find 'const DASHBOARD_DATA = { ... }; </script>' in index.html")

    sanitized_data = sanitize_nans(data)
    data_json_str = json.dumps(sanitized_data, indent=2)
    new_block = f"const DASHBOARD_DATA = {data_json_str};\n  </script>"
    new_content = content[:m.start()] + new_block + content[m.end():]

    # Update badge class in populateSeasonalExploratoryTables if needed
    new_content = new_content.replace(
        "const vrdBadge = r.verdict.includes('trend detected') ? 'badge-sig' : 'badge-null';",
        "const vrdBadge = r.verdict.includes('trend detected') ? 'badge-sig' : (r.verdict === 'Suggestive' ? 'badge-suggestive' : 'badge-null');"
    )

    return new_content


def main():
    data = build_dashboard_data(REPO_ROOT)
    index_path = REPO_ROOT / "index.html"
    new_html = generate_updated_html(index_path, data)

    # Check for forbidden patterns
    banned = [
        r"\bparadox\b",
        r"\brecharge efficiency\b",
        r"\bcaused by\b",
        r"\bdriven by\b",
        r"\bproves\b",
    ]
    for b in banned:
        matches = list(re.finditer(b, new_html, re.IGNORECASE))
        if matches:
            raise ValueError(f"Forbidden phrase '{b}' found in updated HTML: {[m.group(0) for m in matches]}")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(new_html)

    print(f"[OK] Successfully built dashboard data and updated: {index_path} ({len(new_html)} bytes)")


if __name__ == "__main__":
    main()
