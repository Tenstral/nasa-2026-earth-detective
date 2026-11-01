"""
NASA Space Apps 2026 – Bengal Hydro Detective
v3 GPM IMERG V07B Monthly Full Download and Extractor (2002–2025)
================================================================
Downloads and extracts all remaining GPM_3IMERGM granules to complete
the 2002-01 to 2025-09 continuous monthly record across all 8 divisions.
"""

import sys
import json
import time
import calendar
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import numpy as np
import pandas as pd
import xarray as xr
import shapely
import shapely.geometry
import earthaccess

from v3.windows import REGIONS, DIV_AREAS, OUTPUTS_V3

OUTPUT_DIR = OUTPUTS_V3 / "imerg_vs_power"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = REPO_ROOT / "data_imerg_temp"
TEMP_DIR.mkdir(parents=True, exist_ok=True)
CHECKPOINT_CSV = OUTPUT_DIR / "imerg_division_monthly_extracted.csv"
GEOJSON_FILE = REPO_ROOT / "bangladesh_divisions.geojson"


def precompute_grid_masks():
    geo = json.loads(GEOJSON_FILE.read_text(encoding="utf-8"))
    lons = np.round(np.arange(88.05, 92.8, 0.1), 2)  # 48 lons
    lats = np.round(np.arange(20.45, 26.8, 0.1), 2)  # 64 lats
    lon2d, lat2d = np.meshgrid(lons, lats)           # shape (64, 48)
    area_wts = np.cos(np.radians(lat2d))             # shape (64, 48)

    div_masks = {}
    for feat in geo["features"]:
        name = feat["properties"]["name"]
        poly = shapely.geometry.shape(feat["geometry"])
        div_masks[name] = shapely.contains_xy(poly, lon2d, lat2d)

    return lons, lats, lon2d, lat2d, area_wts, div_masks


def main():
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    print("=" * 80)
    print("  GPM IMERG V07B FULL DOWNLOAD AND EXTRACTION (2002-01 to 2025-09)")
    print("=" * 80)

    auth = earthaccess.login(strategy="netrc")
    if not auth.authenticated:
        raise RuntimeError("Earthdata login failed via netrc.")
    print("  [OK] Authenticated with NASA Earthdata via netrc.")

    lons, lats, lon2d, lat2d, area_wts, div_masks = precompute_grid_masks()

    extracted_rows = []
    processed_yms = set()
    if CHECKPOINT_CSV.exists():
        chk_df = pd.read_csv(CHECKPOINT_CSV)
        extracted_rows = chk_df.to_dict(orient="records")
        processed_yms = set(chk_df["ym"].unique())
        print(f"  [CHECKPOINT] Found {len(processed_yms)} months already extracted.")

    print("  Searching CMR for GPM_3IMERGM (2002-01-01 to 2026-07-31)...")
    results = earthaccess.search_data(
        short_name="GPM_3IMERGM",
        temporal=("2002-01-01", "2026-07-31"),
        bounding_box=(88.0, 20.4, 92.8, 26.8)
    )
    print(f"  Found {len(results)} total granules in CMR.")

    to_process = []
    for g in results:
        fname = g.data_links()[0].split("/")[-1]
        parts = fname.split(".")
        date_part = parts[4]  # YYYYMM01
        ym = f"{date_part[:4]}-{date_part[4:6]}"
        if ym not in processed_yms:
            to_process.append((ym, g))

    to_process.sort(key=lambda x: x[0])
    total_to_download = len(to_process)
    print(f"  Granules remaining to download & extract: {total_to_download}")
    if total_to_download == 0:
        print("  All available granules already extracted!")
        return

    batch_size = 8
    n_batches = (total_to_download + batch_size - 1) // batch_size
    t_start = time.time()

    for b_idx in range(n_batches):
        batch = to_process[b_idx * batch_size : (b_idx + 1) * batch_size]
        granules = [item[1] for item in batch]
        yms = [item[0] for item in batch]
        b_num = b_idx + 1

        print(f"\n  [BATCH {b_num}/{n_batches}] Downloading {len(granules)} granules ({yms[0]} to {yms[-1]})...")
        downloaded_files = []
        for attempt in range(3):
            try:
                downloaded_files = earthaccess.download(granules, str(TEMP_DIR), threads=6)
                break
            except Exception as e:
                print(f"    Download retry {attempt+1}/3 due to: {e}")
                time.sleep(2)

        if not downloaded_files:
            print(f"  [ERROR] Failed to download batch {b_num}. Aborting.")
            break

        # Process each downloaded granule
        for fpath_str in downloaded_files:
            fpath = Path(fpath_str)
            try:
                with xr.open_dataset(fpath, group="Grid") as ds:
                    units = ds["precipitation"].attrs.get("units") or ds["precipitation"].attrs.get("Units")
                    if units not in ["mm/hr", "mm hr-1"]:
                        raise ValueError(f"Unexpected precipitation units: {units}")

                    dt_val = str(ds["time"].values[0])[:10]
                    ym = dt_val[:7]
                    year, month = int(ym[:4]), int(ym[5:7])
                    days_in_month = calendar.monthrange(year, month)[1]

                    sub_grid = ds["precipitation"].sel(lon=slice(88.0, 92.8), lat=slice(20.4, 26.8))
                    rate_grid = sub_grid.values[0].T  # transpose to (64, 48)
                    accum_grid = rate_grid * 24.0 * float(days_in_month)

                    for div_name, mask in div_masks.items():
                        wts = area_wts[mask]
                        vals = accum_grid[mask]
                        valid = ~np.isnan(vals)
                        div_precip = float(np.sum(vals[valid] * wts[valid]) / np.sum(wts[valid])) if valid.sum() > 0 else np.nan

                        extracted_rows.append({
                            "ym": ym,
                            "date": f"{ym}-01",
                            "division": div_name,
                            "imerg_precip_mm": round(div_precip, 2),
                            "days_in_month": days_in_month,
                            "units": "mm/month"
                        })
            finally:
                if fpath.exists():
                    for _ in range(5):
                        try:
                            fpath.unlink()
                            break
                        except Exception:
                            time.sleep(0.5)

        # Clean any stray temp partial files
        for p in TEMP_DIR.glob("*"):
            try:
                p.unlink()
            except Exception:
                pass

        # Update checkpoint CSV
        chk_df = pd.DataFrame(extracted_rows).drop_duplicates(subset=["ym", "division"]).sort_values(["ym", "division"])
        chk_df.to_csv(CHECKPOINT_CSV, index=False)
        elapsed = time.time() - t_start
        rate_sec_per_batch = elapsed / b_num
        rem_sec = rate_sec_per_batch * (n_batches - b_num)
        print(f"    -> Extracted. Total months: {chk_df['ym'].nunique()}/285. Elapsed: {elapsed/60:.1f}m, Remaining: {rem_sec/60:.1f}m")

    print("\n" + "=" * 80)
    print(f"  EXTRACTION COMPLETE: {chk_df['ym'].nunique()} months saved to {CHECKPOINT_CSV.name}")
    print("=" * 80)


if __name__ == "__main__":
    main()
