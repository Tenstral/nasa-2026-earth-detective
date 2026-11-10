"""
download_dhaka_modis_aod.py
===========================
NASA Space Apps 2026 – Trend Detective: Bengal Hydro Detective

Automated utility to obtain, process, and analyze NASA Aerosol Optical Depth (AOD)
at 550 nm for Dhaka, Bangladesh.

Supports 3 download & ingestion workflows:
  1. Direct Giovanni Web CSV Import (--csv <path>):
     Cleans and formats area-averaged monthly AOD exported from the NASA Giovanni portal.
  2. NASA Giovanni API Download (--token <token>):
     Direct programmatic fetch using a NASA Earthdata Bearer token.
  3. NASA AERONET Dhaka Station Fetch (--aeronet):
     Zero-auth, keyless automated download from the official NASA AERONET sun-photometer
     station at Dhaka University (23.728°N, 90.398°E).

Produces standardized monthly and annual/seasonal series matching the project schema
and performs the calibrated Effective-Sample-Size Mann-Kendall (ESS-MK) trend test.

Usage:
  python download_dhaka_modis_aod.py --guide
  python download_dhaka_modis_aod.py --aeronet
  python download_dhaka_modis_aod.py --csv path/to/giovanni_dhaka.csv
  python download_dhaka_modis_aod.py --token <YOUR_EARTHDATA_TOKEN>
"""

import sys
import os
import argparse
import json
import io
import urllib.request
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import scipy.stats

REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Coordinate bounds for Dhaka & surrounding capital region
DHAKA_LAT = 23.8103
DHAKA_LON = 90.4125
DHAKA_BBOX = {"min_lon": 89.8, "min_lat": 23.3, "max_lon": 91.0, "max_lat": 24.4}

GIOVANNI_VAR_ID = "MYD08_M3_6_1_AOD_550_Dark_Target_Deep_Blue_Combined_Mean_Mean"
GIOVANNI_API_URL = "https://api.giovanni.earthdata.nasa.gov/timeseries"


def print_giovanni_guide():
    """Prints clear, 5-step instructions to download Dhaka AOD from NASA Giovanni in 30 seconds."""
    guide = f"""
================================================================================
 NASA GIOVANNI MANUAL DOWNLOAD GUIDE: DHAKA MODIS AQUA AOD (550 nm)
================================================================================
If you do not have an Earthdata API token, download the CSV directly from the
official NASA Giovanni portal in 5 easy steps:

1. Open Giovanni in your browser:
   https://giovanni.gsfc.nasa.gov/giovanni/

2. Under 'Select Plot Type', choose:
   -> 'Time Series' -> 'Area-Averaged of Monthly'

3. Under 'Select Date Range':
   -> Start: 2002-07-01
   -> End:   2024-12-31 (or latest available)

4. Under 'Select Region (Bounding Box)':
   -> West:  {DHAKA_BBOX['min_lon']}
   -> South: {DHAKA_BBOX['min_lat']}
   -> East:  {DHAKA_BBOX['max_lon']}
   -> North: {DHAKA_BBOX['max_lat']}

5. In the Search / Variable filter:
   -> Search for: MYD08_M3 AOD
   -> Check the box for:
      'Aerosol Optical Depth 550 nm (Dark Target Deep Blue Combined) (MYD08_M3 v6.1)'
      Variable ID: {GIOVANNI_VAR_ID}

6. Click the green 'Plot Data' button (bottom right).
7. Once the plot appears, click 'Downloads' -> 'CSV'.
8. Run this script to ingest it into the project:
   python download_dhaka_modis_aod.py --csv <downloaded_file.csv>
================================================================================
"""
    print(guide)


def fetch_aeronet_dhaka(start_year: int = 2012, end_year: int = 2024) -> pd.DataFrame:
    """
    Fetches official NASA AERONET ground-truth sun photometer AOD (Level 1.5 cloud-cleared)
    from Dhaka University station (23.728°N, 90.398°E). Keyless, no login required.
    """
    print(f"[*] Fetching NASA AERONET data for Dhaka University ({start_year}–{end_year})...")
    url = (
        f"https://aeronet.gsfc.nasa.gov/cgi-bin/print_web_data_v3?"
        f"site=Dhaka_University&data_type=0&type=AOD15"
        f"&year={start_year}&month=1&day=1&year2={end_year}&month2=12&day2=31"
        f"&AOD15=1&AVG=20"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "NASA-SpaceApps-BengalHydro/1.0"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        content = resp.read().decode("utf-8", errors="ignore")

    lines = [
        line.strip()
        for line in content.splitlines()
        if line.strip()
        and not line.startswith("<")
        and not line.startswith("Version")
        and not line.startswith("The following")
        and not line.startswith("Contact:")
    ]

    header_idx = -1
    for idx, l in enumerate(lines):
        if "AERONET_Site" in l:
            header_idx = idx
            break

    if header_idx == -1:
        raise ValueError("Could not find AERONET table header in NASA response.")

    raw_df = pd.read_csv(io.StringIO("\n".join(lines[header_idx:])))
    date_col = [c for c in raw_df.columns if "Date" in c][0]
    aod_col = "AOD_500nm" if "AOD_500nm" in raw_df.columns else raw_df.columns[4]

    raw_df["date"] = pd.to_datetime(raw_df[date_col], format="%d:%m:%Y", errors="coerce")
    raw_df = raw_df.dropna(subset=["date"])
    raw_df["aod_val"] = pd.to_numeric(raw_df[aod_col], errors="coerce")
    raw_df = raw_df[(raw_df["aod_val"] > 0) & (raw_df["aod_val"] < 5.0)]

    raw_df["ym"] = raw_df["date"].dt.strftime("%Y-%m")
    raw_df["year"] = raw_df["date"].dt.year
    raw_df["month"] = raw_df["date"].dt.month

    # Aggregate to monthly mean
    monthly = (
        raw_df.groupby(["ym", "year", "month"])["aod_val"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "aod_550", "count": "n_days"})
    )
    # Require at least 3 daily observations in a month for statistical validity
    monthly = monthly[monthly["n_days"] >= 3].copy()
    monthly["aod_550"] = monthly["aod_550"].round(3)
    monthly["source"] = "NASA_AERONET_Dhaka_University_L1.5"
    return monthly


def fetch_giovanni_api(token: str, start_year: int = 2002, end_year: int = 2024) -> pd.DataFrame:
    """
    Queries NASA Giovanni Time Series API with an Earthdata Bearer token.
    """
    print(f"[*] Querying NASA Giovanni API for Dhaka MODIS Aqua AOD ({start_year}–{end_year})...")
    params = {
        "data": f"{GIOVANNI_VAR_ID},MYD08_M3_061",
        "location": f"[{DHAKA_LAT},{DHAKA_LON}]",
        "time": f"{start_year}-07-01T00:00:00Z/{end_year}-12-31T23:59:59Z",
    }
    query_str = urllib.parse.urlencode(params)
    full_url = f"{GIOVANNI_API_URL}?{query_str}"

    req = urllib.request.Request(
        full_url,
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "NASA-SpaceApps-BengalHydro/1.0",
        },
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        res_json = json.loads(resp.read().decode("utf-8"))

    # Parse Giovanni JSON format
    data_points = res_json.get("data", [])
    if not data_points:
        raise ValueError(f"No data returned by Giovanni API: {res_json}")

    rows = []
    for pt in data_points:
        # Date format YYYY-MM
        t_str = str(pt.get("time", ""))[:7]
        val = pt.get("value")
        if val is not None and val != -999.0:
            rows.append({"ym": t_str, "aod_550": float(val)})

    df = pd.DataFrame(rows)
    df["year"] = df["ym"].str.slice(0, 4).astype(int)
    df["month"] = df["ym"].str.slice(5, 7).astype(int)
    df["source"] = "NASA_MODIS_Aqua_MYD08_M3_Giovanni_API"
    return df


def parse_giovanni_csv(csv_path: Path) -> pd.DataFrame:
    """
    Parses a CSV file downloaded from the NASA Giovanni web interface.
    Robust against header comments, dynamic column names, and missing value indicators.
    """
    print(f"[*] Ingesting Giovanni CSV from: {csv_path}")
    with open(csv_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    header_line_idx = -1
    for idx, l in enumerate(lines):
        l_str = l.strip().lower()
        if "time" in l_str or "date" in l_str:
            header_line_idx = idx
            break

    if header_line_idx == -1:
        # Fall back to standard CSV read
        df_raw = pd.read_csv(csv_path, comment="#")
    else:
        df_raw = pd.read_csv(io.StringIO("".join(lines[header_line_idx:])))

    # Identify date column and value column
    cols = df_raw.columns.tolist()
    time_col = [c for c in cols if "time" in c.lower() or "date" in c.lower()][0]
    val_cols = [c for c in cols if c != time_col]
    val_col = val_cols[0]

    df = pd.DataFrame()
    df["raw_time"] = df_raw[time_col].astype(str).str.strip()
    df["ym"] = df["raw_time"].str.slice(0, 7)
    df["aod_550"] = pd.to_numeric(df_raw[val_col], errors="coerce")

    # Filter invalid / fill values (-999, etc.)
    df = df.dropna(subset=["aod_550"])
    df = df[(df["aod_550"] >= 0) & (df["aod_550"] < 10.0)]
    df["year"] = df["ym"].str.slice(0, 4).astype(int)
    df["month"] = df["ym"].str.slice(5, 7).astype(int)
    df["source"] = "NASA_MODIS_Aqua_MYD08_M3_Giovanni_CSV"
    return df[["ym", "year", "month", "aod_550", "source"]].sort_values("ym").reset_index(drop=True)


def compute_seasonal_aggregation(monthly_df: pd.DataFrame) -> pd.DataFrame:
    """
    Scientifically correct seasonal trend aggregation per REVIEW_OF_ULTIMATE_PLAN.md:
    Averages each season into ONE value per year to preserve independent annual spacing
    and satisfy Mann-Kendall serial independence assumptions.

    Seasons:
      - Winter / Dry (DJF): Dec (yr-1), Jan (yr), Feb (yr) -> peak smog season
      - Monsoon (JJAS): Jun, Jul, Aug, Sep -> rain washout season
      - Summer (JJA): Jun, Jul, Aug -> direct comparison with Dr. Acker's benchmark
      - Annual: Full calendar year mean
    """
    records = []
    years = sorted(monthly_df["year"].unique())

    for yr in years:
        yr_data = monthly_df[monthly_df["year"] == yr]
        
        # Annual mean (requires >= 6 months)
        if len(yr_data) >= 6:
            records.append({
                "year": yr,
                "season": "annual",
                "aod_mean": round(float(yr_data["aod_550"].mean()), 3),
                "n_obs": len(yr_data)
            })

        # Monsoon (JJAS: months 6, 7, 8, 9)
        jjas = yr_data[yr_data["month"].isin([6, 7, 8, 9])]
        if len(jjas) >= 2:
            records.append({
                "year": yr,
                "season": "monsoon_jjas",
                "aod_mean": round(float(jjas["aod_550"].mean()), 3),
                "n_obs": len(jjas)
            })

        # Winter Smog (DJF: Dec of yr-1, Jan & Feb of yr)
        prev_dec = monthly_df[(monthly_df["year"] == yr - 1) & (monthly_df["month"] == 12)]
        curr_jf = yr_data[yr_data["month"].isin([1, 2])]
        djf = pd.concat([prev_dec, curr_jf])
        if len(djf) >= 2:
            records.append({
                "year": yr,
                "season": "winter_djf",
                "aod_mean": round(float(djf["aod_550"].mean()), 3),
                "n_obs": len(djf)
            })

    return pd.DataFrame(records)


def run_trend_test(series_df: pd.DataFrame, season: str = "winter_djf") -> dict:
    """Runs Theil-Sen slope and Mann-Kendall test on annual/seasonal series."""
    sub = series_df[series_df["season"] == season].dropna().sort_values("year")
    n = len(sub)
    if n < 8:
        return {"season": season, "n": n, "status": "insufficient_data (minimum 8 years required)"}

    t = sub["year"].values.astype(float)
    y = sub["aod_mean"].values.astype(float)

    # Attempt to import calibrated v3 trend engine; fallback to scipy/theil-sen
    try:
        from v3.trend_engine import run_ess_mann_kendall
        res = run_ess_mann_kendall(t, y)
        slope = round(float(res.get("slope", res.get("theil_sen_slope", 0.0))), 4)
        p_val = round(float(res.get("p_value", res.get("ess_p_value", 1.0))), 4)
        ci_low = round(float(res.get("ci_low", res.get("ci_95_low", 0.0))), 4)
        ci_high = round(float(res.get("ci_high", res.get("ci_95_high", 0.0))), 4)
        method = "ESS-MK (Calibrated)"
    except Exception:
        # Scipy fallback
        i_idx, j_idx = np.triu_indices(n, k=1)
        pairwise_slopes = (y[j_idx] - y[i_idx]) / (t[j_idx] - t[i_idx])
        slope = round(float(np.median(pairwise_slopes)), 4)
        tau, p_val = scipy.stats.kendalltau(t, y)
        ci_low = round(float(np.percentile(pairwise_slopes, 2.5)), 4)
        ci_high = round(float(np.percentile(pairwise_slopes, 97.5)), 4)
        method = "Kendall Tau (scipy fallback)"

    verdict = "Significant increase" if (p_val < 0.05 and slope > 0) else (
        "Significant decrease" if (p_val < 0.05 and slope < 0) else "No detectable trend"
    )

    return {
        "season": season,
        "n_years": n,
        "start_year": int(sub["year"].min()),
        "end_year": int(sub["year"].max()),
        "theil_sen_slope_per_year": slope,
        "ci_95": [ci_low, ci_high],
        "p_value": p_val,
        "verdict": verdict,
        "method": method
    }


def main():
    parser = argparse.ArgumentParser(
        description="Download and process NASA Aerosol Optical Depth (AOD) at 550 nm for Dhaka, Bangladesh."
    )
    parser.add_argument("--guide", action="store_true", help="Show step-by-step NASA Giovanni download instructions.")
    parser.add_argument("--csv", type=str, default=None, help="Path to exported NASA Giovanni CSV file.")
    parser.add_argument("--token", type=str, default=None, help="NASA Earthdata Bearer token for Giovanni API.")
    parser.add_argument("--aeronet", action="store_true", help="Download official NASA AERONET ground-truth AOD for Dhaka (Keyless).")
    parser.add_argument("--outdir", type=str, default="outputs/v3/aerosols", help="Output directory path.")

    args = parser.parse_args()

    if args.guide or (not args.csv and not args.token and not args.aeronet):
        print_giovanni_guide()
        if not args.aeronet and not args.csv and not args.token:
            print("\nTip: To test immediately with real NASA ground-truth Dhaka data (no login required), run:")
            print("     python download_dhaka_modis_aod.py --aeronet\n")
            return

    out_dir = Path(args.outdir)
    out_dir.mkdir(parents=True, exist_ok=True)

    monthly_df = None
    if args.csv:
        csv_path = Path(args.csv)
        if not csv_path.exists():
            print(f"[!] Error: File not found: {csv_path}")
            sys.exit(1)
        monthly_df = parse_giovanni_csv(csv_path)

    elif args.token:
        monthly_df = fetch_giovanni_api(args.token)

    elif args.aeronet:
        monthly_df = fetch_aeronet_dhaka()

    if monthly_df is None or len(monthly_df) == 0:
        print("[!] No data could be processed.")
        sys.exit(1)

    # 1. Save monthly cleaned series
    monthly_path = out_dir / "dhaka_aod_monthly.csv"
    monthly_df.to_csv(monthly_path, index=False)
    print(f"[✓] Saved monthly series ({len(monthly_df)} months) -> {monthly_path}")

    # 2. Compute annual & seasonal aggregation (1 value per season per year)
    seasonal_df = compute_seasonal_aggregation(monthly_df)
    seasonal_path = out_dir / "dhaka_aod_seasonal.csv"
    seasonal_df.to_csv(seasonal_path, index=False)
    print(f"[✓] Saved annual & seasonal series ({len(seasonal_df)} points) -> {seasonal_path}")

    # 3. Run trend analysis
    trends = {}
    for season in ["annual", "winter_djf", "monsoon_jjas"]:
        res = run_trend_test(seasonal_df, season=season)
        trends[season] = res

    # 4. Save summary JSON
    summary_path = out_dir / "dhaka_aod_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({
            "region": "Dhaka, Bangladesh",
            "coordinates": {"lat": DHAKA_LAT, "lon": DHAKA_LON},
            "source": monthly_df["source"].iloc[0],
            "total_months": len(monthly_df),
            "trends": trends
        }, f, indent=2)
    print(f"[✓] Saved statistical summary -> {summary_path}")

    # 5. Print results table
    print("\n" + "=" * 70)
    print(" DHAKA AOD STATISTICAL TREND DETECTIVE REPORT")
    print("=" * 70)
    for s_name, res in trends.items():
        if "theil_sen_slope_per_year" in res:
            print(f"Season: {s_name.upper():<12} | N: {res['n_years']:<2} yrs | "
                  f"Slope: {res['theil_sen_slope_per_year']:+.4f}/yr | "
                  f"p-val: {res['p_value']:.4f} | Verdict: {res['verdict']}")
        else:
            print(f"Season: {s_name.upper():<12} | Status: {res.get('status')}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
