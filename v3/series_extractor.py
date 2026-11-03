"""
NASA Space Apps 2026 – Bengal Hydro Detective
v3 Series Extractor: Full-Record Monthly Aggregation (2002–2026)
================================================================
Extracts monthly TWS (cm) and NASA POWER precipitation (mm/month)
for all 8 divisions and 5 regions + National composite across the
complete GRACE/GRACE-FO era (2002-04 to 2026-07).

Outputs:
  outputs/v3/full_record/division_series_2002_2026.csv
  outputs/v3/full_record/region_series_2002_2026.csv
  outputs/v3/full_record/extraction_audit.json
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import numpy as np
import pandas as pd
import shapely
import shapely.geometry
from shapely.ops import unary_union
import xarray as xr

from v2.config_loader import get_grace_netcdf_path, load_config, require_grace_netcdf
from v3.windows import REGIONS, DIV_AREAS, OUTPUTS_V3_FULL

GEOJSON_PATH = REPO_ROOT / "bangladesh_divisions.geojson"
PRECIP_NC_PATH = REPO_ROOT / "nasa_precipitation_bangladesh.nc"


def load_division_geometries():
    with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
        gj = json.load(f)
    divs = {}
    for feat in gj["features"]:
        name = feat["properties"]["name"]
        geom = shapely.geometry.shape(feat["geometry"])
        divs[name] = {
            "geometry": geom,
            "area_km2": DIV_AREAS.get(name, 10000.0),
        }
    return divs


def extract_tws_series(grace_nc_path: Path, divs: dict) -> pd.DataFrame:
    """
    Extracts divisional GRACE TWS anomalies directly from CSR NetCDF (2002-04 to 2026-07).
    Handles calendar dates, asserts 'cm' units, and calculates area-weighted means.
    Averages duplicate intra-month solutions to single calendar months.
    """
    print(f"Reading GRACE/GRACE-FO NetCDF: {grace_nc_path.name}...")
    ds = xr.open_dataset(str(grace_nc_path), decode_times=False)

    lwe_units = ds["lwe_thickness"].attrs.get("units", ds["lwe_thickness"].attrs.get("Units", "?"))
    if not ("cm" in str(lwe_units).lower() or "centimeter" in str(lwe_units).lower()):
        raise ValueError(f"Unexpected units for lwe_thickness: '{lwe_units}'. Must be cm.")
    print(f"  [OK] lwe_thickness units verified: '{lwe_units}'")

    base = pd.Timestamp("2002-01-01")
    raw_days = ds["time"].values
    dates = [base + pd.Timedelta(days=float(d)) for d in raw_days]
    yms = [d.strftime("%Y-%m") for d in dates]

    lons = ds["lon"].values
    lats = ds["lat"].values
    lons_wgs = np.where(lons > 180, lons - 360, lons) if np.any(lons > 180) else lons

    # Bounding box for Bangladesh
    lon_idx = (lons_wgs >= 87.0) & (lons_wgs <= 93.5)
    lat_idx = (lats >= 20.0) & (lats <= 27.5)

    sub_lons = lons_wgs[lon_idx]
    sub_lats = lats[lat_idx]
    sub_lwe = ds["lwe_thickness"].values[:, lat_idx, :][:, :, lon_idx]

    lat2d, lon2d = np.meshgrid(sub_lats, sub_lons, indexing="ij")
    cos_lat = np.cos(np.radians(lat2d))

    # Precompute masks for each division
    div_masks = {}
    for div_name, info in divs.items():
        m = shapely.contains_xy(info["geometry"], lon2d, lat2d)
        if m.sum() == 0:
            c = info["geometry"].centroid
            dist = (lat2d - c.y) ** 2 + (lon2d - c.x) ** 2
            min_idx = np.unravel_index(np.argmin(dist), dist.shape)
            m[min_idx] = True
        div_masks[div_name] = m

    raw_records = []
    for t_idx, (dt, ym) in enumerate(zip(dates, yms)):
        if ym < "2002-04" or ym > "2026-07":
            continue
        grid_t = sub_lwe[t_idx, :, :]
        dec_year = dt.year + (dt.month - 0.5) / 12.0

        for div_name, mask in div_masks.items():
            wts = cos_lat[mask]
            vals = grid_t[mask]
            valid = ~np.isnan(vals)
            if valid.sum() > 0:
                wmean = float(np.sum(vals[valid] * wts[valid]) / np.sum(wts[valid]))
            else:
                wmean = float("nan")

            raw_records.append({
                "ym": ym,
                "date": pd.to_datetime(ym + "-01"),
                "decimal_year": dec_year,
                "Division": div_name,
                "grace_tws_cm": wmean,
            })

    raw_df = pd.DataFrame(raw_records)
    # Aggregate duplicate intra-month solutions by taking mean
    agg_df = raw_df.groupby(["ym", "Division"], as_index=False).agg({
        "date": "first",
        "decimal_year": "mean",
        "grace_tws_cm": "mean",
    })
    agg_df["grace_tws_cm"] = agg_df["grace_tws_cm"].round(4)
    print(f"  Extracted {len(agg_df)} divisional TWS records across {agg_df['ym'].nunique()} unique months.")
    return agg_df


def extract_precip_series(precip_nc_path: Path, divs: dict) -> pd.DataFrame:
    """
    Extracts divisional NASA POWER precipitation from NetCDF (2002-01 to 2026-09).
    """
    print(f"Reading Precipitation NetCDF: {precip_nc_path.name}...")
    ds = xr.open_dataset(str(precip_nc_path))

    lats = ds.lat.values
    lons = ds.lon.values
    if lats[0] > lats[-1]:
        ds = ds.isel(lat=slice(None, None, -1))
        lats = ds.lat.values

    lon2d, lat2d = np.meshgrid(lons, lats)
    area_wts = np.cos(np.radians(lat2d))
    times = pd.to_datetime(ds.time.values)

    div_masks = {}
    for div_name, info in divs.items():
        m = shapely.contains_xy(info["geometry"], lon2d, lat2d)
        if m.sum() == 0:
            m = np.array([
                info["geometry"].intersects(shapely.geometry.Point(lon2d[r, c], lat2d[r, c]))
                for r in range(lon2d.shape[0]) for c in range(lon2d.shape[1])
            ]).reshape(lon2d.shape)
        div_masks[div_name] = m

    rows = []
    for t_idx, dt in enumerate(times):
        ym = dt.strftime("%Y-%m")
        data = ds["precipitation"].isel(time=t_idx).values

        for div_name, mask in div_masks.items():
            if mask.sum() > 0:
                vals = data[mask]
                wts = area_wts[mask]
                valid = ~np.isnan(vals)
                wmean = float(np.sum(vals[valid] * wts[valid]) / np.sum(wts[valid])) if valid.sum() > 0 else float("nan")
            else:
                wmean = float("nan")

            rows.append({
                "ym": ym,
                "date": pd.to_datetime(ym + "-01"),
                "Division": div_name,
                "power_precip_mm": round(wmean, 3),
            })

    df = pd.DataFrame(rows)
    print(f"  Extracted {len(df)} divisional precipitation records across {df['ym'].nunique()} months.")
    return df


def build_regional_series(div_df: pd.DataFrame, divs: dict) -> pd.DataFrame:
    """
    Builds area-weighted regional and National composite series for TWS and Precipitation.
    """
    rows = []
    dates = sorted(div_df["date"].unique())

    for reg, info in REGIONS.items():
        members = info["divisions"]
        areas = np.array([divs[d]["area_km2"] for d in members])
        total_area = areas.sum()

        for dt in dates:
            m_sub = div_df[(div_df["date"] == dt) & (div_df["Division"].isin(members))]
            if m_sub.empty:
                continue

            ym = m_sub["ym"].iloc[0]
            dec_yr = m_sub["decimal_year"].iloc[0] if "decimal_year" in m_sub.columns else dt.year + (dt.month - 0.5) / 12.0

            # Area-weighted TWS
            tws_vals = m_sub["grace_tws_cm"].values
            tws_valid = ~np.isnan(tws_vals)
            if tws_valid.sum() == len(members):
                reg_tws = float(np.sum(tws_vals * areas) / total_area)
            elif tws_valid.sum() > 0:
                reg_tws = float(np.sum(tws_vals[tws_valid] * areas[tws_valid]) / np.sum(areas[tws_valid]))
            else:
                reg_tws = float("nan")

            # Area-weighted Precip
            pr_vals = m_sub["power_precip_mm"].values
            pr_valid = ~np.isnan(pr_vals)
            if pr_valid.sum() == len(members):
                reg_pr = float(np.sum(pr_vals * areas) / total_area)
            elif pr_valid.sum() > 0:
                reg_pr = float(np.sum(pr_vals[pr_valid] * areas[pr_valid]) / np.sum(areas[pr_valid]))
            else:
                reg_pr = float("nan")

            rows.append({
                "region": reg,
                "date": dt,
                "ym": ym,
                "decimal_year": round(dec_yr, 4),
                "grace_tws_cm": round(reg_tws, 4) if not np.isnan(reg_tws) else np.nan,
                "power_precip_mm": round(reg_pr, 3) if not np.isnan(reg_pr) else np.nan,
            })

    return pd.DataFrame(rows)


def run_extraction():
    grace_nc = require_grace_netcdf("v3 Full-Record Series Extraction")
    divs = load_division_geometries()

    # 1. Extract TWS
    tws_df = extract_tws_series(grace_nc, divs)

    # 2. Extract Precip
    precip_df = extract_precip_series(PRECIP_NC_PATH, divs)

    # 3. Merge at division level
    merged_div = pd.merge(
        tws_df,
        precip_df[["ym", "Division", "power_precip_mm"]],
        on=["ym", "Division"],
        how="outer"
    ).sort_values(["Division", "date"]).reset_index(drop=True)

    # Fill decimal_year for precipitation-only months if any
    for idx in merged_div[merged_div["decimal_year"].isna()].index:
        d = merged_div.loc[idx, "date"]
        merged_div.loc[idx, "decimal_year"] = d.year + (d.month - 0.5) / 12.0

    # 4. Regional aggregation
    reg_df = build_regional_series(merged_div, divs)

    # 5. Save deliverables
    div_out = OUTPUTS_V3_FULL / "division_series_2002_2026.csv"
    reg_out = OUTPUTS_V3_FULL / "region_series_2002_2026.csv"
    audit_out = OUTPUTS_V3_FULL / "extraction_audit.json"

    merged_div.to_csv(div_out, index=False)
    reg_df.to_csv(reg_out, index=False)

    # Audit summary
    tws_months = sorted(tws_df["ym"].unique())
    precip_months = sorted(precip_df["ym"].unique())

    audit = {
        "timestamp": datetime.now().isoformat(),
        "grace_netcdf": str(grace_nc.name),
        "tws_unique_months": len(tws_months),
        "tws_min_month": tws_months[0],
        "tws_max_month": tws_months[-1],
        "precip_unique_months": len(precip_months),
        "precip_min_month": precip_months[0],
        "precip_max_month": precip_months[-1],
        "division_rows": len(merged_div),
        "region_rows": len(reg_df),
        "regions_covered": list(REGIONS.keys()),
        "divisions_covered": list(DIV_AREAS.keys()),
    }
    with open(audit_out, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2)

    print(f"\n[OK] Series Extraction Complete!")
    print(f"  Saved: {div_out.name} ({len(merged_div)} rows)")
    print(f"  Saved: {reg_out.name} ({len(reg_df)} rows)")
    print(f"  Saved: {audit_out.name}")
    return merged_div, reg_df, audit


if __name__ == "__main__":
    run_extraction()
