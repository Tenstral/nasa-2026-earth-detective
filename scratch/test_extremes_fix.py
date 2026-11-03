import sys
from pathlib import Path
REPO_ROOT = Path(r"c:\Users\LEON\OneDrive\Documents\GitHub\nasa-2026-earth-detective")
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import pandas as pd
import numpy as np
from v3.trend_engine import run_ess_mann_kendall
ann_csv = REPO_ROOT / "outputs" / "v3" / "extremes" / "imerg_extreme_indices_annual.csv"
mon_csv = REPO_ROOT / "outputs" / "v3" / "extremes" / "imerg_extreme_indices_monsoon.csv"

df_ann = pd.read_csv(ann_csv)
df_mon = pd.read_csv(mon_csv)

print("--- ANNUAL INDICES ---")
for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
    sub = df_ann[df_ann["region"] == reg].sort_values("year")
    t = sub["year"].values.astype(float)
    for col in ["annual_total_mm", "rx1day_mm", "rx5day_mm", "days_ge_50mm"]:
        y = sub[col].values.astype(float)
        res = run_ess_mann_kendall(t, y)
        ci_excludes_zero = (res["ci_low"] > 0 and res["ci_high"] > 0) or (res["ci_low"] < 0 and res["ci_high"] < 0)
        p_sig = res["p_value"] < 0.05
        mismatch = ci_excludes_zero != p_sig
        if mismatch or reg in ["NW", "National"]:
            print(f"{reg} {col:16s} slope={res['slope']:+7.3f} CI=[{res['ci_low']:+7.3f}, {res['ci_high']:+7.3f}] p={res['p_value']:.4f} mismatch={mismatch}")

print("\n--- MONSOON INDICES ---")
for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
    sub = df_mon[df_mon["region"] == reg].sort_values("year")
    t = sub["year"].values.astype(float)
    for col in ["monsoon_total_mm", "monsoon_rx1day_mm", "monsoon_rx5day_mm", "monsoon_days_ge_50mm"]:
        y = sub[col].values.astype(float)
        res = run_ess_mann_kendall(t, y)
        ci_excludes_zero = (res["ci_low"] > 0 and res["ci_high"] > 0) or (res["ci_low"] < 0 and res["ci_high"] < 0)
        p_sig = res["p_value"] < 0.05
        mismatch = ci_excludes_zero != p_sig
        if mismatch or reg in ["NW", "Central", "SE"]:
            print(f"{reg} {col:22s} slope={res['slope']:+7.3f} CI=[{res['ci_low']:+7.3f}, {res['ci_high']:+7.3f}] p={res['p_value']:.4f} mismatch={mismatch}")
