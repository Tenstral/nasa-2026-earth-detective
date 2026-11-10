"""
v3/ingest_modis_aod.py
======================
Ingests NASA Giovanni area-averaged monthly AOD CSV exports for:
  1. Dhaka Region (89.8°E–91.0°E, 23.3°N–24.4°N)
  2. All Bangladesh (88.0°E–92.7°E, 20.5°N–26.7°N)

Saves standardized outputs to outputs/v3/aerosols/
"""

import sys
import io
import re
from pathlib import Path
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "data_raw" / "modis_aod"
OUT_DIR = REPO_ROOT / "outputs" / "v3" / "aerosols"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def parse_giovanni_csv(csv_path: Path, box_label: str) -> pd.DataFrame:
    """Robust parser for NASA Giovanni CSV exports with metadata headers."""
    if not csv_path.exists():
        return None

    with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    header_line_idx = -1
    metadata_lines = []
    for idx, l in enumerate(lines):
        l_str = l.strip().lower()
        if "time" in l_str or "date" in l_str:
            header_line_idx = idx
            break
        else:
            metadata_lines.append(l.strip())

    if header_line_idx == -1:
        df_raw = pd.read_csv(csv_path, comment="#")
    else:
        df_raw = pd.read_csv(io.StringIO("".join(lines[header_line_idx:])))

    cols = df_raw.columns.tolist()
    time_col = [c for c in cols if "time" in c.lower() or "date" in c.lower()][0]
    val_cols = [c for c in cols if c != time_col]
    val_col = val_cols[0]

    df = pd.DataFrame()
    df["raw_time"] = df_raw[time_col].astype(str).str.strip()
    df["ym"] = df["raw_time"].str.slice(0, 7)
    df["aod_550"] = pd.to_numeric(df_raw[val_col], errors="coerce")

    # Clean missing / fill values
    df = df.dropna(subset=["aod_550"])
    df = df[(df["aod_550"] >= 0) & (df["aod_550"] < 10.0)]
    df["year"] = df["ym"].str.slice(0, 4).astype(int)
    df["month"] = df["ym"].str.slice(5, 7).astype(int)
    df["decimal_year"] = (df["year"] + (df["month"] - 0.5) / 12.0).round(4)
    df["source"] = f"NASA_MODIS_Aqua_MYD08_M3_{box_label}"

    clean = df[["ym", "year", "month", "decimal_year", "aod_550", "source"]].sort_values("ym").reset_index(drop=True)
    return clean


def main():
    dhaka_raw = RAW_DIR / "giovanni_dhaka.csv"
    bd_raw = RAW_DIR / "giovanni_bangladesh.csv"

    dhaka_df = parse_giovanni_csv(dhaka_raw, "Dhaka_Box")
    bd_df = parse_giovanni_csv(bd_raw, "Bangladesh_National")

    if dhaka_df is not None:
        out_dhaka = OUT_DIR / "modis_aod_dhaka_monthly.csv"
        dhaka_df.to_csv(out_dhaka, index=False)
        print(f"[OK] Saved Dhaka MODIS AOD ({len(dhaka_df)} months) -> {out_dhaka}")
    else:
        print(f"[INFO] {dhaka_raw} not found yet. Ready to ingest when provided.")

    if bd_df is not None:
        out_bd = OUT_DIR / "modis_aod_bangladesh_monthly.csv"
        bd_df.to_csv(out_bd, index=False)
        print(f"[OK] Saved Bangladesh MODIS AOD ({len(bd_df)} months) -> {out_bd}")
    else:
        print(f"[INFO] {bd_raw} not found yet. Ready to ingest when provided.")


if __name__ == "__main__":
    main()
