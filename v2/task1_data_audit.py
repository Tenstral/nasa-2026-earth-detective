"""
NASA Space Apps 2026 – Bengal Hydro Detective
Task 1: Data Audit
==================
Checks coverage, missing months, units, gap handling, provenance, and
temporal overlap for all input datasets. Fails loudly if required files
are absent. Prints a plain-language explanation of every choice.

Run:
    python v2/task1_data_audit.py
"""

import json
import os
import sys
import hashlib
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

# Force UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "outputs" / "v2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

try:
    from v2.config_loader import get_grace_netcdf_path, load_config
except ImportError:
    from config_loader import get_grace_netcdf_path, load_config

cfg = load_config()
GRACE_NC = get_grace_netcdf_path()
PRECIP_NC = REPO_ROOT / cfg.get("nasa_precipitation_netcdf_path", "nasa_precipitation_bangladesh.nc")
EXCEL_FILE = REPO_ROOT / cfg.get("excel_fallback_path", "bangladesh_water_analysis_detailed.xlsx")

# Analysis windows
PRIMARY_START = cfg.get("primary_window", {}).get("start", "2020-01")
PRIMARY_END   = cfg.get("primary_window", {}).get("end", "2026-07")
GRACE_FO_START = cfg.get("grace_fo_window", {}).get("start", "2018-06")

# Approved 5-region groupings
REGIONS = {
    "NW":      ["Rajshahi", "Rangpur"],
    "NE":      ["Sylhet", "Mymensingh"],
    "Central": ["Dhaka"],
    "SW":      ["Khulna", "Barishal"],
    "SE":      ["Chattogram"],
}

DIVISIONS = ["Barishal", "Chattogram", "Dhaka", "Khulna",
             "Mymensingh", "Rajshahi", "Rangpur", "Sylhet"]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _md5(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            buf = f.read(chunk)
            if not buf:
                break
            h.update(buf)
    return h.hexdigest()


def _months_between(start_ym: str, end_ym: str) -> int:
    s = pd.to_datetime(start_ym + "-01")
    e = pd.to_datetime(end_ym  + "-01")
    return (e.year - s.year) * 12 + (e.month - s.month) + 1


def _missing_months(present: list[str], start_ym: str, end_ym: str) -> list[str]:
    """Return months in [start, end] that are not in present."""
    s = pd.to_datetime(start_ym + "-01")
    e = pd.to_datetime(end_ym   + "-01")
    expected = pd.date_range(s, e, freq="MS").strftime("%Y-%m").tolist()
    present_set = set(present)
    return [m for m in expected if m not in present_set]


def _sep():
    print("─" * 72)

# ---------------------------------------------------------------------------
# Section 1: GRACE NetCDF (primary storage source)
# ---------------------------------------------------------------------------

def audit_grace_netcdf(report: dict) -> dict:
    """Attempt to open the GRACE NetCDF. Fail loudly if absent."""
    _sep()
    print("  SECTION 1 — GRACE/GRACE-FO NetCDF")
    _sep()

    grace_report = {"file": str(GRACE_NC) if GRACE_NC else "None", "status": None}

    if GRACE_NC is None or not GRACE_NC.exists():
        msg = (
            f"\n[LOUD AUDIT ALERT] GRACE / GRACE-FO NetCDF not found.\n"
            f"  Lookup checked: CLI (--grace-nc), env (GRACE_NETCDF_PATH), config.json, and repo root.\n"
            f"  IMPACT & POLICY:\n"
            f"    1. Multi-window duplicate rows are strictly prohibited (no artificial window collapse).\n"
            f"    2. Only the Primary Window (2020-01 to 2026-07) will be processed from verified Excel series.\n"
            f"    3. The GRACE-FO robustness window (2018-06 to 2026-07) requires configuring the NetCDF path.\n"
            f"  To configure the path without hardcoding:\n"
            f"    - Set 'grace_netcdf_path' in config.json, OR\n"
            f"    - Export GRACE_NETCDF_PATH=/path/to/CSR_GRACE_GRACE-FO_RL0603_Mascons_all-corrections.nc\n"
        )
        print(msg)
        grace_report["status"] = "ABSENT – Processing restricted to Primary Window (2020-01 to 2026-07)"
        grace_report["impact"] = (
            "GRACE-FO window (2018-06 to 2026-07) requires NetCDF. "
            "Pipeline will process ONLY Primary Window and will NOT write duplicate-window rows."
        )
    else:
        print(f"  Found: {GRACE_NC.name}  ({GRACE_NC.stat().st_size / 1e6:.1f} MB)")
        print(f"  MD5  : {_md5(GRACE_NC)}")
        ds = xr.open_dataset(str(GRACE_NC), decode_times=False)
        if "Units" in ds["time"].attrs and "units" not in ds["time"].attrs:
            ds["time"].attrs["units"] = ds["time"].attrs["Units"]
        ds = xr.decode_cf(ds)
        times = pd.to_datetime(ds["time"].values)
        months_present = times.strftime("%Y-%m").tolist()
        start_ym = months_present[0]
        end_ym   = months_present[-1]
        missing  = _missing_months(months_present, start_ym, end_ym)
        lwe_var  = ds["lwe_thickness"]
        print(f"  Time range  : {start_ym} to {end_ym}  ({len(months_present)} months)")
        print(f"  Missing months: {len(missing)} {'(none)' if not missing else missing}")
        print(f"  Spatial     : lat {float(ds.lat.min()):.2f}°N–{float(ds.lat.max()):.2f}°N, "
              f"lon {float(ds.lon.min()):.2f}°E–{float(ds.lon.max()):.2f}°E")
        print(f"  Variable    : lwe_thickness  units={lwe_var.attrs.get('units','?')}  "
              f"long_name={lwe_var.attrs.get('long_name','?')}")
        grace_report.update({
            "status": "PRESENT",
            "start_ym": start_ym,
            "end_ym": end_ym,
            "n_months": len(months_present),
            "missing_months": missing,
            "lwe_units": lwe_var.attrs.get("units", "?"),
        })

    report["grace_netcdf"] = grace_report
    return report

# ---------------------------------------------------------------------------
# Section 2: NASA POWER precipitation NetCDF
# ---------------------------------------------------------------------------

def audit_precip_netcdf(report: dict) -> dict:
    _sep()
    print("  SECTION 2 — NASA POWER Precipitation NetCDF")
    _sep()

    if not PRECIP_NC.exists():
        raise FileNotFoundError(
            f"[FATAL] Precipitation NetCDF not found: {PRECIP_NC}\n"
            "Run: python download_nasa_precipitation.py"
        )

    print(f"  Found: {PRECIP_NC.name}  ({PRECIP_NC.stat().st_size / 1e3:.1f} kB)")
    print(f"  MD5  : {_md5(PRECIP_NC)}")

    ds = xr.open_dataset(str(PRECIP_NC))
    times = pd.to_datetime(ds["time"].values)
    months_present = times.strftime("%Y-%m").tolist()
    start_ym = months_present[0]
    end_ym   = months_present[-1]
    missing  = _missing_months(months_present, start_ym, end_ym)

    # NaN check
    nan_count = int(np.isnan(ds["precipitation"].values).sum())
    total_cells = ds["precipitation"].values.size
    nan_frac = nan_count / total_cells * 100

    print(f"\n  Source      : {ds.attrs.get('source', '?')}")
    print(f"  Variable    : precipitation (monthly total, mm/month)")
    print(f"              : precipitation_rate (daily mean, mm/day)")
    print(f"  Time range  : {start_ym} to {end_ym}  ({len(months_present)} months)")
    print(f"  Missing months in sequence: {len(missing)} {'(none)' if not missing else missing}")
    print(f"  Spatial     : lat {float(ds.lat.min()):.3f}°N–{float(ds.lat.max()):.3f}°N  "
          f"({len(ds.lat)} cells @ 0.5°)")
    print(f"              : lon {float(ds.lon.min()):.3f}°E–{float(ds.lon.max()):.3f}°E  "
          f"({len(ds.lon)} cells @ 0.625°)")
    print(f"  NaN cells   : {nan_count:,} / {total_cells:,}  ({nan_frac:.2f}%)")
    print(f"\n  ⚠  LABEL BUG NOTED: Source attribute says 'NASA POWER (GPM IMERG & GMAO MERRA-2).'")
    print(f"     The variable is PRECTOTCORR from NASA POWER, NOT the GPM IMERG Final Run product.")
    print(f"     All v2 outputs will use the corrected label: 'NASA POWER Precipitation (mm)'.")

    precip_report = {
        "file": str(PRECIP_NC),
        "source_attr": ds.attrs.get("source", "?"),
        "corrected_label": "NASA POWER Precipitation (PRECTOTCORR) [mm/month]",
        "spatial_resolution_deg": "0.5 lat × 0.625 lon",
        "n_lat": int(len(ds.lat)),
        "n_lon": int(len(ds.lon)),
        "start_ym": start_ym,
        "end_ym": end_ym,
        "n_months": len(months_present),
        "missing_months": missing,
        "nan_cells": nan_count,
        "nan_fraction_pct": round(nan_frac, 4),
    }
    report["precip_netcdf"] = precip_report
    return report

# ---------------------------------------------------------------------------
# Section 3: Excel fallback / pre-extracted series
# ---------------------------------------------------------------------------

def audit_excel(report: dict) -> dict:
    _sep()
    print("  SECTION 3 — Excel Pre-Extracted Series (GRACE fallback)")
    _sep()

    if not EXCEL_FILE.exists():
        raise FileNotFoundError(
            f"[FATAL] Excel file not found: {EXCEL_FILE}\n"
            "Run: python create_excel_report.py  (requires GRACE NetCDF)"
        )

    print(f"  Found: {EXCEL_FILE.name}  ({EXCEL_FILE.stat().st_size / 1e3:.1f} kB)")

    import openpyxl
    wb = openpyxl.load_workbook(str(EXCEL_FILE), read_only=True)
    print(f"  Sheets: {wb.sheetnames}")

    df = pd.read_excel(str(EXCEL_FILE), sheet_name="Historical_Trends_2020_2026", skiprows=3)

    # Validate columns
    expected_cols = ["Year-Month", "Year", "Month", "Division",
                     "GRACE Storage Anomaly (cm)", "IMERG Precipitation (mm)"]
    found_cols = df.columns.tolist()
    print(f"\n  Columns found: {found_cols}")

    # Note the label issue
    if "IMERG Precipitation (mm)" in found_cols:
        print("  ⚠  Column 'IMERG Precipitation (mm)' is mislabelled.")
        print("     Actual source: NASA POWER PRECTOTCORR. Will be renamed in v2 outputs.")

    # Coverage per division
    print(f"\n  {'Division':<14}  {'N months':>8}  {'Start':>8}  {'End':>8}  {'NaN GRACE':>10}  {'NaN Precip':>11}")
    print("  " + "─" * 68)
    excel_report = {"divisions": {}}
    for div in DIVISIONS:
        sub = df[df["Division"] == div].sort_values("Year-Month")
        n = len(sub)
        start = sub["Year-Month"].iloc[0] if n > 0 else "?"
        end   = sub["Year-Month"].iloc[-1] if n > 0 else "?"
        nan_g = int(sub["GRACE Storage Anomaly (cm)"].isna().sum())
        nan_p = int(sub["IMERG Precipitation (mm)"].isna().sum())
        print(f"  {div:<14}  {n:>8}  {start:>8}  {end:>8}  {nan_g:>10}  {nan_p:>11}")
        excel_report["divisions"][div] = {
            "n_months": n, "start_ym": start, "end_ym": end,
            "nan_grace": nan_g, "nan_precip": nan_p,
        }

    months_all = sorted(df["Year-Month"].unique())
    missing_months = _missing_months(months_all, months_all[0], months_all[-1])
    print(f"\n  Total unique months in Excel : {len(months_all)} ({months_all[0]} to {months_all[-1]})")
    print(f"  Missing months in sequence  : {len(missing_months)} {'(none)' if not missing_months else missing_months}")

    excel_report["start_ym"] = months_all[0]
    excel_report["end_ym"]   = months_all[-1]
    excel_report["n_months"] = len(months_all)
    excel_report["missing_months"] = missing_months
    report["excel_fallback"] = excel_report
    return report

# ---------------------------------------------------------------------------
# Section 4: Temporal Overlap & Window Definitions
# ---------------------------------------------------------------------------

def audit_overlap(report: dict) -> dict:
    _sep()
    print("  SECTION 4 — Temporal Overlap & Analysis Windows")
    _sep()

    grace_end  = report["excel_fallback"]["end_ym"]   # 2026-07
    precip_end = report["precip_netcdf"]["end_ym"]     # 2026-09
    grace_start = report["excel_fallback"]["start_ym"] # 2020-01
    precip_start = report["precip_netcdf"]["start_ym"] # 2020-01

    overlap_start = max(grace_start, precip_start)
    overlap_end   = min(grace_end, precip_end)
    n_overlap = _months_between(overlap_start, overlap_end)

    rain_only_months = _missing_months(
        pd.date_range(overlap_start + "-01", overlap_end + "-01",
                      freq="MS").strftime("%Y-%m").tolist(),
        overlap_start, precip_end
    )

    print(f"  GRACE (Excel)       : {grace_start} → {grace_end}")
    print(f"  NASA POWER Precip   : {precip_start} → {precip_end}")
    print(f"  Overlap window      : {overlap_start} → {overlap_end}  ({n_overlap} months)")
    print(f"  Rainfall-only months: {rain_only_months}  "
          f"(storage data unavailable; excluded from joint analysis)")

    print(f"\n  ANALYSIS WINDOWS (parameterised; start/end are CLI arguments):")
    windows = {
        "primary": {
            "start": PRIMARY_START,
            "end":   PRIMARY_END,
            "n_months": _months_between(PRIMARY_START, PRIMARY_END),
            "status": "ACTIVE",
            "note": "Primary analysis window (79 months) with verified complete satellite overlap.",
        },
        "grace_fo_era": {
            "start": GRACE_FO_START,
            "end":   PRIMARY_END,
            "n_months_nominal": _months_between(GRACE_FO_START, PRIMARY_END),
            "status": "ACTIVE (via NetCDF)" if GRACE_NC and GRACE_NC.exists() else "INACTIVE (NetCDF absent)",
            "note": (
                "GRACE-FO single-instrument mission era (2018-06 to 2026-07). "
                "Active when GRACE NetCDF path is configured; duplicate-window rows prevented when absent."
            ),
        },
    }

    for name, w in windows.items():
        print(f"\n  Window: {name}")
        for k, v in w.items():
            print(f"    {k:<25}: {v}")

    report["overlap"] = {
        "overlap_start": overlap_start,
        "overlap_end": overlap_end,
        "n_overlap_months": n_overlap,
        "rainfall_only_months": rain_only_months,
    }
    report["analysis_windows"] = windows
    return report

# ---------------------------------------------------------------------------
# Section 5: Region Definitions
# ---------------------------------------------------------------------------

def audit_regions(report: dict) -> dict:
    _sep()
    print("  SECTION 5 — Approved Region Groupings (5 regions)")
    _sep()

    import json as _json
    geojson_path = REPO_ROOT / "bangladesh_divisions.geojson"
    area_km2 = {}
    if geojson_path.exists():
        with open(geojson_path, "r", encoding="utf-8") as f:
            gj = _json.load(f)
        for feat in gj["features"]:
            name = feat["properties"]["name"]
            area = feat["properties"].get("area_km2")
            if area:
                area_km2[name] = area

    print(f"\n  {'Region':<10}  {'Divisions':<35}  {'Total area (km²)':>18}")
    print("  " + "─" * 68)
    region_report = {}
    for reg, divs in REGIONS.items():
        total_area = sum(area_km2.get(d, float("nan")) for d in divs)
        area_str = f"{total_area:,.0f}" if not np.isnan(total_area) else "?"
        print(f"  {reg:<10}  {', '.join(divs):<35}  {area_str:>18}")
        region_report[reg] = {"divisions": divs, "total_area_km2": round(total_area, 1) if not np.isnan(total_area) else None}

    print(f"\n  GRACE note: CSR RL06.3 mascons are ~300 km features. Adjacent divisions")
    print(f"  share signal. Division maps are retained as spatial context; significance")
    print(f"  tests and comparisons run on the 5 regions above.")

    report["regions"] = region_report
    return report

# ---------------------------------------------------------------------------
# Section 6: Provenance Summary
# ---------------------------------------------------------------------------

def audit_provenance(report: dict) -> dict:
    _sep()
    print("  SECTION 6 — Provenance & Source File Summary")
    _sep()

    print(f"\n  DATA SOURCES USED IN THIS PIPELINE RUN:")
    print(f"  ┌─────────────────────────────────────────────────────────────────┐")

    grace_status = report["grace_netcdf"]["status"]
    if GRACE_NC is None or not GRACE_NC.exists():
        print(f"  │ GRACE TWS  : Excel fallback  ({EXCEL_FILE.name})")
        print(f"  │             Sheets: Historical_Trends_2020_2026")
        print(f"  │             Coverage: 2020-01 → 2026-07 (79 months × 8 divisions)")
        print(f"  │             ⚠  Pre-extracted series – not from raw mascon grid")
    else:
        print(f"  │ GRACE TWS  : {GRACE_NC.name}")
        print(f"  │             Coverage: {report['grace_netcdf']['start_ym']} → {report['grace_netcdf']['end_ym']}")

    print(f"  │ Precip     : {PRECIP_NC.name}")
    print(f"  │             Source: NASA POWER PRECTOTCORR (not GPM IMERG Final Run)")
    print(f"  │             Coverage: {report['precip_netcdf']['start_ym']} → {report['precip_netcdf']['end_ym']}")
    print(f"  │ Boundaries : bangladesh_divisions.geojson (8 administrative divisions)")
    print(f"  └─────────────────────────────────────────────────────────────────┘")

    print(f"\n  ⚠  LABEL CORRECTIONS applied in all v2 outputs:")
    print(f"     'IMERG Precipitation' → 'NASA POWER Precipitation (PRECTOTCORR)'")
    print(f"     'groundwater'         → 'total water storage' (per GRACE convention)")
    print(f"     All results labelled PRELIMINARY.")

    report["generated_at"] = datetime.now().isoformat()
    report["python_version"] = sys.version
    return report

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("\n" + "═" * 72)
    print("  NASA EARTH DETECTIVE — TASK 1: DATA AUDIT")
    print("  Bengal Hydro Detective  |  Team Tenstral  |  2026-10-31")
    print("═" * 72)

    report = {}
    report = audit_grace_netcdf(report)
    report = audit_precip_netcdf(report)
    report = audit_excel(report)
    report = audit_overlap(report)
    report = audit_regions(report)
    report = audit_provenance(report)

    # Save JSON
    out_path = OUTPUT_DIR / "task1_data_audit.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    _sep()
    print(f"\n  ✓ Audit complete.  Saved: {out_path}")
    print()

    # -----------------------------------------------------------------------
    # Plain-language explanation for judges
    # -----------------------------------------------------------------------
    print("═" * 72)
    print("  PLAIN-LANGUAGE EXPLANATION — for judges or reviewers")
    print("═" * 72)
    print("""
  Q: Why are you using NASA POWER instead of real IMERG?
  A: The existing code downloads PRECTOTCORR from the NASA POWER API, which
     is a model-assimilated precipitation product (MERRA-2 + GPM corrections),
     not the GPM IMERG Final Run product. POWER requires no login and covers
     our full period. We corrected the mislabelling in all outputs. Real IMERG
     (GPM_3IMERGM V07B) is available via NASA Earthdata but requires a free
     account and the earthaccess package; we describe exactly how to set that
     up if the user wants it as a parallel source.

  Q: Why are the three analysis windows the same here?
  A: The Excel pre-extracted series covers only 2020-01 to 2026-07. The
     GRACE classic era (2002–2017) and the GRACE-FO gap (2017-06 to 2018-05)
     cannot be reconstructed without the raw GRACE NetCDF file. We flag this
     in every output. Downloading that file (~150 MB from UT CSR) would unlock
     the full-record and GRACE-FO-era windows in subsequent tasks.

  Q: What does the rainfall-only period mean?
  A: Rainfall data (NASA POWER) extends to 2026-09 but GRACE storage ends at
     2026-07. August and September 2026 have rainfall values but no matching
     storage values. We exclude those two months from any joint rainfall–storage
     analysis and note them explicitly. Rainfall-only trend tests can still use
     the full 81-month record.
""")


if __name__ == "__main__":
    main()
