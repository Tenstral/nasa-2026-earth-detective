"""
v3/process_harmony_modis_aod.py
===============================
Monitors the NASA Harmony transformation job (C1443775657-LAADS / MYD08_M3 v6.1),
incrementally downloads each subsetted monthly AOD granule (~295 KB) as it becomes
ready, extracts:
  1. Dhaka Region (Lat 23.81°N, Lon 90.41°E; Row 66, Col 270)
  2. All-Bangladesh Bounding Box Average (Lat 20.5–26.7°N, Lon 88.0–92.7°E)

Saves standardized monthly time series incrementally to:
  - outputs/v3/aerosols/modis_aod_dhaka_monthly.csv
  - outputs/v3/aerosols/modis_aod_bangladesh_monthly.csv

And automatically triggers v3/build_webapp_data.py on each new batch.
"""

import sys
import os
import re
import time
import json
import tempfile
import urllib.request
import subprocess
from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd
from pyhdf.SD import SD, SDC

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "outputs" / "v3" / "aerosols"
OUT_DIR.mkdir(parents=True, exist_ok=True)

JOB_ID = "7057b6bb-dca3-421d-b5e5-a0a53ddf8d77"
HARMONY_JOB_URL = f"https://harmony.earthdata.nasa.gov/jobs/{JOB_ID}"

# Dhaka cell (Lat 23.81, Lon 90.41 in 1-deg grid: Row = int(90 - 23.81) = 66, Col = int(90.41 + 180) = 270)
DHAKA_ROW = 66
DHAKA_COL = 270

# Bangladesh Box (Lat 20.5–26.7: Rows 63..69; Lon 88.0–92.7: Cols 268..272)
BD_ROW_START = 63
BD_ROW_END = 70
BD_COL_START = 268
BD_COL_END = 273


def fetch_job_status(token: str) -> dict:
    req = urllib.request.Request(
        f"{HARMONY_JOB_URL}?page=1&limit=2000",
        headers={"Authorization": f"Bearer {token}", "User-Agent": "NASA-SpaceApps/1.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def process_hdf_file(file_path: str):
    """Extracts Dhaka point AOD and Bangladesh area-average AOD from a subsetted HDF file."""
    try:
        hdf = SD(file_path, SDC.READ)
        sds_names = list(hdf.datasets().keys())
        if not sds_names:
            return None, None
        sds = hdf.select(sds_names[0])
        raw = sds.get()
        attrs = sds.attributes()
        scale = float(attrs.get("scale_factor", 0.001))
        fill = attrs.get("_FillValue", -9999)
        hdf.end()

        # 1. Dhaka value
        val_dhaka = raw[DHAKA_ROW, DHAKA_COL]
        dhaka_aod = float(val_dhaka * scale) if val_dhaka != fill else np.nan

        # 2. Bangladesh area-average
        bd_sub = raw[BD_ROW_START:BD_ROW_END, BD_COL_START:BD_COL_END].astype(float)
        bd_valid = bd_sub[bd_sub != fill]
        bd_aod = float(np.mean(bd_valid) * scale) if len(bd_valid) > 0 else np.nan

        return dhaka_aod, bd_aod
    except Exception as e:
        print(f"[WARN] Error reading {file_path}: {e}")
        return None, None


def load_existing():
    out_dhaka = OUT_DIR / "modis_aod_dhaka_monthly.csv"
    out_bd = OUT_DIR / "modis_aod_bangladesh_monthly.csv"
    dhaka_rows = []
    bd_rows = []
    seen_ym = set()

    if out_dhaka.exists():
        try:
            df = pd.read_csv(out_dhaka)
            dhaka_rows = df.to_dict("records")
            seen_ym.update(df["ym"].tolist())
        except Exception:
            pass

    if out_bd.exists():
        try:
            df = pd.read_csv(out_bd)
            bd_rows = df.to_dict("records")
        except Exception:
            pass

    return dhaka_rows, bd_rows, seen_ym


def save_and_rebuild(dhaka_rows, bd_rows):
    out_dhaka = OUT_DIR / "modis_aod_dhaka_monthly.csv"
    out_bd = OUT_DIR / "modis_aod_bangladesh_monthly.csv"

    if dhaka_rows:
        df_d = pd.DataFrame(dhaka_rows).sort_values("ym").drop_duplicates(subset=["ym"]).reset_index(drop=True)
        df_d.to_csv(out_dhaka, index=False)

    if bd_rows:
        df_b = pd.DataFrame(bd_rows).sort_values("ym").drop_duplicates(subset=["ym"]).reset_index(drop=True)
        df_b.to_csv(out_bd, index=False)

    # Re-run build_webapp_data.py
    subprocess.run([sys.executable, str(REPO_ROOT / "v3/build_webapp_data.py")], check=True)


def main():
    if len(sys.argv) < 2:
        print("Usage: python process_harmony_modis_aod.py <EARTHDATA_TOKEN>")
        sys.exit(1)

    token = sys.argv[1].strip()
    dhaka_rows, bd_rows, seen_ym = load_existing()
    print(f"[*] Starting incremental extraction. Existing processed months: {len(seen_ym)}")

    with tempfile.TemporaryDirectory() as tmpdir:
        while True:
            try:
                status_data = fetch_job_status(token)
            except Exception as e:
                print(f"[WARN] Error fetching job status ({e}), retrying in 10s...")
                time.sleep(10)
                continue

            status = status_data.get("status")
            progress = status_data.get("progress", 0)
            data_links = [l for l in status_data.get("links", []) if l.get("rel") == "data"]
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Job Status: {status} | Progress: {progress}% | Granules Ready: {len(data_links)}/289")

            newly_processed = 0
            for link in data_links:
                href = link.get("href")
                filename = link.get("title") or href.split("/")[-1]

                # Parse date from filename: e.g. MYD08_M3.A2020001...
                m = re.search(r"\.A(\d{4})(\d{3})\.", filename)
                if not m:
                    continue

                year_str, doy_str = m.group(1), m.group(2)
                try:
                    dt = datetime.strptime(f"{year_str}{doy_str}", "%Y%j")
                except Exception:
                    continue

                ym = dt.strftime("%Y-%m")
                if ym in seen_ym:
                    continue

                year = dt.year
                month = dt.month
                dec_year = round(year + (month - 0.5) / 12.0, 4)

                # Download granule
                tmp_path = os.path.join(tmpdir, filename)
                req = urllib.request.Request(
                    href,
                    headers={"Authorization": f"Bearer {token}", "User-Agent": "NASA-SpaceApps/1.0"}
                )
                try:
                    with urllib.request.urlopen(req, timeout=30) as resp, open(tmp_path, "wb") as f_out:
                        f_out.write(resp.read())

                    dhaka_val, bd_val = process_hdf_file(tmp_path)
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)

                    if dhaka_val is not None and not np.isnan(dhaka_val):
                        dhaka_rows.append({
                            "ym": ym,
                            "year": year,
                            "month": month,
                            "decimal_year": dec_year,
                            "aod_550": round(dhaka_val, 3),
                            "source": "NASA_MODIS_Aqua_MYD08_M3_Dhaka_Box"
                        })

                    if bd_val is not None and not np.isnan(bd_val):
                        bd_rows.append({
                            "ym": ym,
                            "year": year,
                            "month": month,
                            "decimal_year": dec_year,
                            "aod_550": round(bd_val, 3),
                            "source": "NASA_MODIS_Aqua_MYD08_M3_Bangladesh_National"
                        })

                    seen_ym.add(ym)
                    newly_processed += 1
                    print(f"  + Ingested {ym}: Dhaka AOD = {dhaka_val:.3f}, BD Mean = {bd_val:.3f}")

                except Exception as e:
                    print(f"[WARN] Failed fetching {filename}: {e}")

            if newly_processed > 0:
                print(f"[*] Saving {len(seen_ym)} cumulative months and updating webapp payloads...")
                save_and_rebuild(dhaka_rows, bd_rows)

            if status in ("successful", "complete") and len(data_links) == len(seen_ym):
                print(f"\n[DONE] All {len(seen_ym)} granules processed successfully!")
                break
            elif status in ("failed", "canceled"):
                print(f"[ERROR] Harmony job ended with status: {status}")
                break

            time.sleep(12)


if __name__ == "__main__":
    main()
