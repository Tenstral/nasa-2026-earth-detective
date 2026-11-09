"""
Compile all project datasets into structured JSON objects for index.html.
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
import shapely.geometry

REPO_ROOT = Path(__file__).resolve().parent.parent

# 1. Load GeoJSON and generate SVG path data
with open(REPO_ROOT / "bangladesh_divisions.geojson", encoding="utf-8") as f:
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
    
    # centroid for label placement
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
reg_df = pd.read_csv(REPO_ROOT / "outputs/v3/full_record/region_series_2002_2026.csv")
div_df = pd.read_csv(REPO_ROOT / "outputs/v3/full_record/division_series_2002_2026.csv")

# Clean division names
div_df["Division"] = div_df["Division"].str.strip()
div_df["year"] = div_df["ym"].str.slice(0, 4).astype(int)
div_df["month"] = div_df["ym"].str.slice(5, 7).astype(int)

# Divisional Annual Summary (2002 to 2026)
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
            "n_months": int(ygrp["grace_tws_cm"].notna().sum())
        }

# Divisional Monthly Series
div_monthly = {}
for div, grp in div_df.groupby("Division"):
    div_monthly[div] = {
        "ym": grp["ym"].tolist(),
        "tws": [round(float(v), 2) if not np.isnan(v) else None for v in grp["grace_tws_cm"]],
        "precip": [round(float(v), 1) if not np.isnan(v) else None for v in grp["imerg_precip_mm"]]
    }

# Regional Monthly Series
reg_monthly = {}
for reg, grp in reg_df.groupby("region"):
    reg_monthly[reg] = {
        "ym": grp["ym"].tolist(),
        "tws": [round(float(v), 2) if not np.isnan(v) else None for v in grp["grace_tws_cm"]],
        "imerg": [round(float(v), 1) if not np.isnan(v) else None for v in grp["imerg_precip_mm"]],
        "power": [round(float(v), 1) if not np.isnan(v) else None for v in grp["power_precip_mm"]]
    }

# 3. GLDAS Multi-Model Partition Series
part_df = pd.read_csv(REPO_ROOT / "outputs/v3/gldas_split/storage_partition_series_multi_model.csv")
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
res_df = pd.read_csv(REPO_ROOT / "outputs/v3/full_record/results_all_windows.csv")
res_clean = res_df[[
    "window", "entity", "entity_type", "variable", "season", "slope",
    "slope_ci_low", "slope_ci_high", "p_value", "bh_fdr_q_value", "verdict", "primary_method"
]].copy()
res_clean["p_value"] = res_clean["p_value"].apply(lambda p: "< 0.0001" if p < 0.0001 else f"{p:.4f}")
res_clean["bh_fdr_q_value"] = res_clean["bh_fdr_q_value"].apply(lambda q: "< 0.0001" if (pd.notna(q) and q < 0.0001) else (f"{q:.4f}" if pd.notna(q) else "—"))
res_clean["slope"] = res_clean["slope"].round(3)
res_clean["slope_ci_low"] = res_clean["slope_ci_low"].round(3)
res_clean["slope_ci_high"] = res_clean["slope_ci_high"].round(3)

# 5. Three-Way Slopes Table
three_way_df = pd.read_csv(REPO_ROOT / "outputs/v3/full_record/three_way_slopes_and_transition.csv")

# 6. GLDAS Summary Table
gldas_sum_df = pd.read_csv(REPO_ROOT / "outputs/v3/gldas_split/gldas_multi_model_summary.csv")
gldas_clean = gldas_sum_df[[
    "window", "region", "tws_slope_cm_yr", "noah_sms_slope", "vic_sms_slope",
    "independent_sms_range", "independent_residual_range", "clsm_sms_slope", "clsm_residual_slope"
]].copy()

# 7. Exposure Table
exp_df = pd.read_csv(REPO_ROOT / "outputs/v3/exposure/exposure_table.csv")
exp_clean = exp_df[[
    "region", "pop_millions_2020", "pop_share_pct", "cropland_pct_mcd12q1",
    "total_agricultural_pct", "tws_slope_cm_yr", "tws_ci_95", "tws_verdict", "exposure_narrative"
]].copy()

# 8. Flood Table
flood_df = pd.read_csv(REPO_ROOT / "outputs/v3/extremes/flood_events_context.csv")

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
    "floods": flood_df.to_dict(orient="records")
}

out_file = REPO_ROOT / "scratch/dashboard_data.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(compiled, f, indent=2)

print("Saved compiled dashboard data to:", out_file)
print("File size:", out_file.stat().st_size, "bytes")
