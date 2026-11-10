"""
v3/build_webapp_data.py
=======================
Compiles and serializes all primary datasets into structured JavaScript files
under data/ for zero-dependency client-side execution in the browser.

Outputs:
  - data/catalog.js          (Variable definitions, regions, divisions, flood events, presets)
  - data/map.js              (Cleaned SVG paths and division centroids)
  - data/series_regions.js   (Monthly time series for 5 macro-regions + National)
  - data/series_divisions.js (Monthly time series for 8 administrative divisions)
  - data/series_extremes.js  (Annual ETCCDI extreme precipitation indices)
  - data/series_aod.js       (AERONET ground truth and MODIS satellite AOD)
  - data/presets.js          (FDR q-values and benchmark verdicts for canonical annual windows)
"""

import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from v3.build_dashboard import build_map_paths

DATA_DIR = REPO_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def sanitize(val, decimals=4):
    """Sanitizes floats, NaNs, and rounds decimals."""
    if val is None or pd.isna(val) or np.isneginf(val) or np.isposinf(val):
        return None
    try:
        return round(float(val), decimals)
    except Exception:
        return None


def export_map_js():
    geojson_path = REPO_ROOT / "bangladesh_divisions.geojson"
    svg_paths, div_centers = build_map_paths(geojson_path)

    region_divisions = {
        "NW": ["Rajshahi", "Rangpur"],
        "NE": ["Sylhet", "Mymensingh"],
        "Central": ["Dhaka"],
        "SW": ["Khulna", "Barishal"],
        "SE": ["Chattogram"],
    }

    division_to_region = {}
    for r, divs in region_divisions.items():
        for d in divs:
            division_to_region[d] = r

    payload = {
        "svgPaths": svg_paths,
        "divCenters": div_centers,
        "regionDivisions": region_divisions,
        "divisionToRegion": division_to_region,
    }

    out_file = DATA_DIR / "map.js"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"window.ED = window.ED || {{}};\nwindow.ED.map = {json.dumps(payload, indent=2)};\n")
    print(f"[OK] Exported {out_file} ({out_file.stat().st_size:,} bytes)")


def export_catalog_js():
    # Load flood events context
    floods_df = pd.read_csv(REPO_ROOT / "outputs/v3/extremes/flood_events_context.csv")
    flood_events = []
    for _, r in floods_df.iterrows():
        flood_events.append({
            "year": int(r["year"]),
            "flood_period": str(r["flood_period"]),
            "classification": str(r["ffwc_classification"]),
            "inundation_area_pct": str(r["inundation_area_pct"]),
            "districts_affected": str(r["districts_affected"]) if not pd.isna(r["districts_affected"]) else "",
            "national_monsoon_precip_mm": sanitize(r["national_monsoon_precip_mm"], 1),
            "national_monsoon_anom_pct": sanitize(r["national_monsoon_anom_pct"], 1),
            "post_monsoon_peak_cm": sanitize(r["post_monsoon_peak_cm"], 2),
            "source": str(r["source_document"]) if "source_document" in r and not pd.isna(r["source_document"]) else "",
            "url": str(r["source_url"]) if "source_url" in r and not pd.isna(r["source_url"]) else "",
            "notes": str(r["meteorological_driver"]) if "meteorological_driver" in r and not pd.isna(r["meteorological_driver"]) else ""
        })

    # Regions metadata from exposure table
    exp_df = pd.read_csv(REPO_ROOT / "outputs/v3/exposure/exposure_table.csv")
    regions = []
    for _, r in exp_df.iterrows():
        regions.append({
            "id": str(r["region"]),
            "name": {
                "NW": "Northwest (Rajshahi + Rangpur)",
                "NE": "Northeast (Sylhet + Mymensingh)",
                "Central": "Central (Dhaka)",
                "SW": "Southwest (Khulna + Barishal)",
                "SE": "Southeast (Chattogram)",
                "National": "National Composite (Bangladesh)"
            }.get(str(r["region"]), str(r["region"])),
            "population_2020_m": sanitize(r["pop_millions_2020"], 2),
            "population_share_pct": sanitize(r["pop_share_pct"], 1),
            "cropland_pct": sanitize(r["cropland_pct_mcd12q1"], 1),
            "total_agricultural_pct": sanitize(r["total_agricultural_pct"], 1),
            "tws_slope_cm_yr": sanitize(r["tws_slope_cm_yr"], 3),
            "tws_ci_95": str(r["tws_ci_95"]),
            "tws_verdict": str(r["tws_verdict"]),
            "context": str(r["regional_context"])
        })

    divisions = [
        {"id": "Barishal", "name": "Barishal Division", "region": "SW"},
        {"id": "Chattogram", "name": "Chattogram Division", "region": "SE"},
        {"id": "Dhaka", "name": "Dhaka Division", "region": "Central"},
        {"id": "Khulna", "name": "Khulna Division", "region": "SW"},
        {"id": "Mymensingh", "name": "Mymensingh Division", "region": "NE"},
        {"id": "Rajshahi", "name": "Rajshahi Division", "region": "NW"},
        {"id": "Rangpur", "name": "Rangpur Division", "region": "NW"},
        {"id": "Sylhet", "name": "Sylhet Division", "region": "NE"},
    ]

    variables = [
        {
            "id": "grace_tws",
            "name": "Total Water Storage Anomaly (TWS)",
            "domain": "Water & Gravity",
            "sensor": "CSR GRACE / GRACE-FO RL06.3 Mascons",
            "unit": "cm",
            "unit_description": "Centimeters of equivalent water height (anomaly vs. 2004–2009 baseline)",
            "spatial_footprint": "~300 km mascon resolution (regional aggregate)",
            "temporal_range": "2002-04 to 2026-07 (monthly)",
            "definition": "Measures total changes in all terrestrial water storage—deep and shallow groundwater, soil moisture, surface water bodies, and wetlands—by detecting minute changes in Earth's gravitational pull.",
            "caveats": "Coarse spatial resolution (~300 km). Administrative division estimates share neighboring mascons and are descriptive only. Shaded 11-month observation gap (July 2017 to May 2018) separates the two satellite missions.",
            "supports_divisions": True,
            "has_gap": True,
            "can_deseasonalize": True,
            "kind": "mean"
        },
        {
            "id": "imerg_precip",
            "name": "Satellite Precipitation (GPM IMERG)",
            "domain": "Rainfall & Storms",
            "sensor": "GPM IMERG V07B Final Run",
            "unit": "mm/month",
            "unit_description": "Millimeters of rainfall per month",
            "spatial_footprint": "0.1° (~10 km) satellite radar & passive microwave",
            "temporal_range": "2002-01 to 2025-09 (monthly)",
            "definition": "NASA's premier multi-satellite precipitation estimate combining spaceborne dual-frequency precipitation radar, passive microwave constellations, and ground rain-gauge calibration.",
            "caveats": "Satellite microwave algorithms can underestimate light drizzle or saturate in intense mountain-front convective storms.",
            "supports_divisions": True,
            "has_gap": False,
            "can_deseasonalize": True,
            "kind": "sum"
        },
        {
            "id": "power_precip",
            "name": "Reanalysis Precipitation (NASA POWER)",
            "domain": "Rainfall & Storms (Atmospheric Model)",
            "sensor": "NASA POWER MERRA-2 PRECTOTCORR",
            "unit": "mm/month",
            "unit_description": "Millimeters of rainfall per month (reanalysis model)",
            "spatial_footprint": "0.5° × 0.625° global atmospheric model grid",
            "temporal_range": "2002-01 to 2026-07 (monthly)",
            "definition": "Global reanalysis rainfall produced by NASA's Goddard Earth Observing System (GEOS) atmospheric model with data assimilation.",
            "caveats": "⚠️ Critical Sensor Break Trap: Contains a known artificial step shift around 2015 caused by observing system transitions in the underlying MERRA-2 model. Used in Case File #3 to teach data verification.",
            "supports_divisions": True,
            "has_gap": False,
            "can_deseasonalize": True,
            "kind": "sum"
        },
        {
            "id": "noah_sms_anom",
            "name": "Root-Zone Soil Moisture Anomaly (Noah 2.1)",
            "domain": "Land Surface & Agriculture",
            "sensor": "GLDAS Noah 2.1 Land Surface Model",
            "unit": "cm",
            "unit_description": "Centimeters of equivalent water in the top 0–2.0 m soil column",
            "spatial_footprint": "0.25° (~25 km) land surface simulation",
            "temporal_range": "2002-04 to 2026-07 (monthly)",
            "definition": "Simulates water stored in the upper 2 meters of soil (the root zone) where vegetation and crops absorb water.",
            "caveats": "Does not simulate deep unconfined or confined aquifers below 2 meters depth. Computed for macro-regions only.",
            "supports_divisions": False,
            "has_gap": False,
            "can_deseasonalize": True,
            "kind": "mean"
        },
        {
            "id": "vic_sms_anom",
            "name": "Root-Zone Soil Moisture Anomaly (VIC 2.1)",
            "domain": "Land Surface & Agriculture",
            "sensor": "GLDAS VIC 2.1 Hydrological Model",
            "unit": "cm",
            "unit_description": "Centimeters of equivalent water in the top 0–2.0 m soil column",
            "spatial_footprint": "0.25° (~25 km) land surface simulation",
            "temporal_range": "2002-04 to 2026-07 (monthly)",
            "definition": "Independent land surface model utilizing variable infiltration capacity to simulate moisture storage in the plant root zone.",
            "caveats": "Independent physics from Noah; provides an ensemble model envelope for soil moisture uncertainty.",
            "supports_divisions": False,
            "has_gap": False,
            "can_deseasonalize": True,
            "kind": "mean"
        },
        {
            "id": "subsurface_residual",
            "name": "Partitioned Subsurface Residual",
            "domain": "Partitioned Subsurface Storage",
            "sensor": "CSR GRACE TWS − GLDAS ΔSMS (Noah/VIC Midpoint)",
            "unit": "cm",
            "unit_description": "Centimeters of equivalent water thickness (subsurface residual)",
            "spatial_footprint": "Macro-regional aggregate (NW, NE, Central, SW, SE, National)",
            "temporal_range": "2002-04 to 2026-07 (monthly)",
            "definition": "The storage anomaly remaining after subtracting simulated root-zone soil moisture from total satellite water storage. Strictly labeled: 'groundwater + surface water + model error residual'.",
            "caveats": "Because satellite gravimetry measures the total water column, subtracting soil moisture isolates deep storage changes plus any unmodeled surface water bodies and land surface model errors.",
            "supports_divisions": False,
            "has_gap": True,
            "can_deseasonalize": True,
            "kind": "mean"
        },
        {
            "id": "extreme_rx1day",
            "name": "Extreme 1-Day Downpour (Rx1day)",
            "domain": "Climate Extremes",
            "sensor": "GPM IMERG Daily Precipitation Derivative",
            "unit": "mm/day",
            "unit_description": "Maximum 1-day rainfall recorded in the calendar year",
            "spatial_footprint": "Macro-regional aggregate",
            "temporal_range": "2003 to 2024 (annual)",
            "definition": "World Meteorological Organization standard index for the single heaviest daily deluge of the year.",
            "caveats": "Annual series (one observation per calendar year). Tests whether peak storm intensity is shifting.",
            "supports_divisions": False,
            "has_gap": False,
            "can_deseasonalize": False,
            "kind": "mean"
        },
        {
            "id": "extreme_days_ge_50",
            "name": "Heavy Torrent Days (Rainfall ≥ 50 mm)",
            "domain": "Climate Extremes",
            "sensor": "GPM IMERG Daily Precipitation Derivative",
            "unit": "days/year",
            "unit_description": "Number of days with regional rainfall ≥ 50 mm/day",
            "spatial_footprint": "Macro-regional aggregate",
            "temporal_range": "2003 to 2024 (annual)",
            "definition": "Counts the frequency of severe torrential rainfall events capable of triggering flash floods and waterlogging.",
            "caveats": "Annual series (one observation per year).",
            "supports_divisions": False,
            "has_gap": False,
            "can_deseasonalize": False,
            "kind": "mean"
        },
        {
            "id": "aod_550",
            "name": "Aerosol Optical Depth 550 nm (AOD)",
            "domain": "Atmosphere & Air Quality",
            "sensor": "NASA AERONET Ground Station + MODIS Aqua Satellite",
            "unit": "dimensionless AOD",
            "unit_description": "Optical thickness at 550 nm (higher values indicate hazier, more polluted air)",
            "spatial_footprint": "Ground station point (AERONET Dhaka University) & 1.0° satellite grid (MODIS)",
            "temporal_range": "2012 to 2024 (AERONET); 2002 to present (MODIS)",
            "definition": "Measures how much sunlight is prevented from reaching the ground by airborne particles such as seasonal winter smog, brick kiln emissions, and biomass burning.",
            "caveats": "Ground station measures directly above Dhaka University. Satellite MODIS observations are averaged over the 1° capital bounding box.",
            "supports_divisions": False,
            "has_gap": False,
            "can_deseasonalize": True,
            "kind": "mean"
        }
    ]

    payload = {
        "variables": variables,
        "regions": regions,
        "divisions": divisions,
        "floodEvents": flood_events,
        "gapPeriod": {"start": "2017-07", "end": "2018-05", "label": "Inter-Satellite Mission Gap (11 months)"},
        "canonicalWindows": [
            {"id": "full_record", "label": "Full 24-Year Record", "start": "2002-04", "end": "2026-07"},
            {"id": "grace_era", "label": "GRACE-1 Baseline Era", "start": "2002-04", "end": "2017-06"},
            {"id": "grace_fo_era", "label": "GRACE-FO Single Era", "start": "2018-06", "end": "2026-07"},
            {"id": "recent_2020", "label": "Recent Overlap Era", "start": "2020-01", "end": "2026-07"},
        ],
        "seasons": [
            {"id": "annual", "label": "All Months (Deseasonalized)", "months": "1–12"},
            {"id": "monsoon", "label": "Monsoon Season (JJAS)", "months": "Jun–Sep"},
            {"id": "winter", "label": "Winter / Dry Season (DJF)", "months": "Dec–Feb"},
            {"id": "pre_monsoon", "label": "Pre-Monsoon Season (MAM)", "months": "Mar–May"},
            {"id": "post_monsoon", "label": "Post-Monsoon Season (ON)", "months": "Oct–Nov"},
        ]
    }

    out_file = DATA_DIR / "catalog.js"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"window.ED = window.ED || {{}};\nwindow.ED.catalog = {json.dumps(payload, indent=2)};\n")
    print(f"[OK] Exported {out_file} ({out_file.stat().st_size:,} bytes)")


def export_presets_js():
    res_df = pd.read_csv(REPO_ROOT / "outputs/v3/full_record/results_all_windows.csv")
    # Filter to annual series only (canonical presets)
    ann_df = res_df[res_df["season"] == "annual"].copy()

    presets = {}
    for _, r in ann_df.iterrows():
        key = f"{r['window']}_{r['entity']}_{r['variable']}"
        presets[key] = {
            "window": str(r["window"]),
            "entity": str(r["entity"]),
            "variable": str(r["variable"]),
            "n_obs": int(r["n_obs"]),
            "slope": sanitize(r["slope"], 4),
            "slope_ci_low": sanitize(r["slope_ci_low"], 4),
            "slope_ci_high": sanitize(r["slope_ci_high"], 4),
            "p_value": sanitize(r["p_value"], 6),
            "bh_fdr_q_value": sanitize(r["bh_fdr_q_value"], 6),
            "verdict": str(r["verdict"]),
            "gamma": sanitize(r["gamma"], 3),
            "r1_detrended": sanitize(r["r1_detrended"], 4),
            "n_star": sanitize(r["n_star"], 1),
            "unit": str(r["unit_primary"])
        }

    out_file = DATA_DIR / "presets.js"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"window.ED = window.ED || {{}};\nwindow.ED.presets = {json.dumps(presets, indent=2)};\n")
    print(f"[OK] Exported {out_file} ({len(presets)} canonical preset tests)")


def export_series_regions_js():
    reg_df = pd.read_csv(REPO_ROOT / "outputs/v3/full_record/region_series_2002_2026.csv")
    part_df = pd.read_csv(REPO_ROOT / "outputs/v3/gldas_split/storage_partition_series_multi_model.csv")

    regions_data = {}
    regions = ["NW", "NE", "Central", "SW", "SE", "National"]

    for reg in regions:
        r_sub = reg_df[reg_df["region"] == reg].sort_values("ym").copy()
        p_sub = part_df[part_df["region"] == reg].set_index("ym")

        ym_list = r_sub["ym"].tolist()
        t_list = [sanitize(x, 4) for x in r_sub["decimal_year"]]
        tws_list = [sanitize(x, 3) for x in r_sub["grace_tws_cm"]]
        imerg_list = [sanitize(x, 2) for x in r_sub["imerg_precip_mm"]]
        power_list = [sanitize(x, 2) for x in r_sub["power_precip_mm"]]

        noah_sms = []
        vic_sms = []
        resid_mid = []
        resid_min = []
        resid_max = []

        for ym in ym_list:
            if ym in p_sub.index:
                row = p_sub.loc[ym]
                noah_sms.append(sanitize(row["noah_sms_anom_cm"], 3))
                vic_sms.append(sanitize(row["vic_sms_anom_cm"], 3))
                rmin = sanitize(row["independent_residual_min_cm"], 3)
                rmax = sanitize(row["independent_residual_max_cm"], 3)
                resid_min.append(rmin)
                resid_max.append(rmax)
                if rmin is not None and rmax is not None:
                    resid_mid.append(round((rmin + rmax) / 2.0, 3))
                else:
                    resid_mid.append(None)
            else:
                noah_sms.append(None)
                vic_sms.append(None)
                resid_mid.append(None)
                resid_min.append(None)
                resid_max.append(None)

        regions_data[reg] = {
            "ym": ym_list,
            "t": t_list,
            "tws": tws_list,
            "imerg": imerg_list,
            "power": power_list,
            "noah_sms": noah_sms,
            "vic_sms": vic_sms,
            "residual_mid": resid_mid,
            "residual_min": resid_min,
            "residual_max": resid_max,
        }

    out_file = DATA_DIR / "series_regions.js"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"window.ED = window.ED || {{}};\nwindow.ED.seriesRegions = {json.dumps(regions_data, separators=(',', ':'))};\n")
    print(f"[OK] Exported {out_file} ({out_file.stat().st_size:,} bytes)")


def export_series_divisions_js():
    div_df = pd.read_csv(REPO_ROOT / "outputs/v3/full_record/division_series_2002_2026.csv")
    div_df["Division"] = div_df["Division"].str.strip()

    divisions_data = {}
    for div, grp in div_df.groupby("Division"):
        grp = grp.sort_values("ym").copy()
        divisions_data[div] = {
            "ym": grp["ym"].tolist(),
            "t": [sanitize(x, 4) for x in grp["decimal_year"]],
            "tws": [sanitize(x, 3) for x in grp["grace_tws_cm"]],
            "imerg": [sanitize(x, 2) for x in grp["imerg_precip_mm"]],
            "power": [sanitize(x, 2) for x in grp["power_precip_mm"]],
        }

    out_file = DATA_DIR / "series_divisions.js"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"window.ED = window.ED || {{}};\nwindow.ED.seriesDivisions = {json.dumps(divisions_data, separators=(',', ':'))};\n")
    print(f"[OK] Exported {out_file} ({out_file.stat().st_size:,} bytes)")


def export_series_extremes_js():
    ext_df = pd.read_csv(REPO_ROOT / "outputs/v3/extremes/imerg_extreme_indices_annual.csv")
    extremes_data = {}
    for reg, grp in ext_df.groupby("region"):
        grp = grp.sort_values("year")
        items = []
        for _, r in grp.iterrows():
            items.append({
                "year": int(r["year"]),
                "decimal_year": int(r["year"]) + 0.5,
                "annual_total_mm": sanitize(r["annual_total_mm"], 1),
                "rx1day_mm": sanitize(r["rx1day_mm"], 1),
                "rx5day_mm": sanitize(r["rx5day_mm"], 1),
                "days_ge_50mm": int(r["days_ge_50mm"]) if not pd.isna(r["days_ge_50mm"]) else 0,
            })
        extremes_data[reg] = items

    out_file = DATA_DIR / "series_extremes.js"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"window.ED = window.ED || {{}};\nwindow.ED.seriesExtremes = {json.dumps(extremes_data, indent=2)};\n")
    print(f"[OK] Exported {out_file} ({out_file.stat().st_size:,} bytes)")


def export_series_aod_js():
    aod_data = {
        "dhaka_aeronet": [],
        "dhaka_modis": [],
        "bangladesh_modis": []
    }

    # 1. Dhaka AERONET
    aeronet_path = REPO_ROOT / "outputs/v3/aerosols/dhaka_aod_monthly.csv"
    if aeronet_path.exists():
        df = pd.read_csv(aeronet_path)
        for _, r in df.iterrows():
            yr = int(r["year"])
            mo = int(r["month"])
            dec_yr = round(yr + (mo - 0.5) / 12.0, 4)
            aod_data["dhaka_aeronet"].append({
                "ym": str(r["ym"]),
                "year": yr,
                "month": mo,
                "decimal_year": dec_yr,
                "aod_550": sanitize(r["aod_550"], 3),
                "n_days": int(r["n_days"]) if not pd.isna(r["n_days"]) else None,
                "source": "NASA_AERONET_Dhaka_University_L1.5"
            })

    # 2. Dhaka MODIS (if available)
    dhaka_modis_path = REPO_ROOT / "outputs/v3/aerosols/modis_aod_dhaka_monthly.csv"
    if dhaka_modis_path.exists():
        df = pd.read_csv(dhaka_modis_path)
        for _, r in df.iterrows():
            aod_data["dhaka_modis"].append({
                "ym": str(r["ym"]),
                "year": int(r["year"]),
                "month": int(r["month"]),
                "decimal_year": sanitize(r["decimal_year"], 4),
                "aod_550": sanitize(r["aod_550"], 3),
                "source": "NASA_MODIS_Aqua_MYD08_M3_Dhaka_Box"
            })

    # 3. Bangladesh MODIS (if available)
    bd_modis_path = REPO_ROOT / "outputs/v3/aerosols/modis_aod_bangladesh_monthly.csv"
    if bd_modis_path.exists():
        df = pd.read_csv(bd_modis_path)
        for _, r in df.iterrows():
            aod_data["bangladesh_modis"].append({
                "ym": str(r["ym"]),
                "year": int(r["year"]),
                "month": int(r["month"]),
                "decimal_year": sanitize(r["decimal_year"], 4),
                "aod_550": sanitize(r["aod_550"], 3),
                "source": "NASA_MODIS_Aqua_MYD08_M3_Bangladesh_National"
            })

    out_file = DATA_DIR / "series_aod.js"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"window.ED = window.ED || {{}};\nwindow.ED.seriesAOD = {json.dumps(aod_data, indent=2)};\n")
    print(f"[OK] Exported {out_file} (AERONET: {len(aod_data['dhaka_aeronet'])} mo, MODIS Dhaka: {len(aod_data['dhaka_modis'])} mo, MODIS BD: {len(aod_data['bangladesh_modis'])} mo)")


def main():
    print("Building web application data payloads...")
    export_map_js()
    export_catalog_js()
    export_presets_js()
    export_series_regions_js()
    export_series_divisions_js()
    export_series_extremes_js()
    export_series_aod_js()
    print("[SUCCESS] All web application data files generated successfully in data/.")


if __name__ == "__main__":
    main()
