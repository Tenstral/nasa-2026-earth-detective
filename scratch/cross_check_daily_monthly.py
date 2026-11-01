import sys
from pathlib import Path
REPO_ROOT = Path(r"c:\Users\LEON\OneDrive\Documents\GitHub\nasa-2026-earth-detective")
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import pandas as pd

daily_csv = REPO_ROOT / "outputs" / "v3" / "extremes" / "imerg_daily_regional_series.csv"
monthly_csv = REPO_ROOT / "outputs" / "v3" / "imerg_vs_power" / "imerg_region_series.csv"

df_daily = pd.read_csv(daily_csv)
df_monthly = pd.read_csv(monthly_csv)

print("df_monthly columns:", df_monthly.columns.tolist()[:10])

df_daily["year"] = pd.to_datetime(df_daily["date"]).dt.year
df_monthly["year"] = pd.to_datetime(df_monthly["date"]).dt.year

for yr in [2010, 2020]:
    print(f"=== YEAR {yr} ===")
    sub_d = df_daily[df_daily["year"] == yr]
    sub_m = df_monthly[df_monthly["year"] == yr]
    for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
        col_d = f"precip_mm_{reg}"
        sum_d = sub_d[col_d].sum()
        sum_m = sub_m[sub_m["region"] == reg]["imerg_precip_mm"].sum()
        diff = sum_d - sum_m
        pct_diff = (diff / sum_m) * 100.0 if sum_m > 0 else 0
        print(f"  {reg:8s}: Daily Sum = {sum_d:7.1f} mm | Monthly Sum = {sum_m:7.1f} mm | Diff = {diff:+6.1f} mm ({pct_diff:+.2f}%)")
