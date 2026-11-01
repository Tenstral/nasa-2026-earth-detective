"""
NASA Space Apps 2026 – Bengal Hydro Detective
v3 Seasonal Recharge Dynamics: 24-Season Rebound & Efficiency
==============================================================
Analyzes hydrological recovery dynamics across ~24 monsoon seasons (2002–2025):
  - Pre-monsoon dry season low (Apr/May) to post-monsoon peak (Sep/Oct) storage rebound (Delta TWS, cm)
  - Seasonal monsoon precipitation accumulation (P_monsoon, mm)
  - Recharge efficiency ratio: RE = Delta TWS (cm) / (0.1 * P_monsoon, cm)
  - Theil-Sen trend and Hamed-Rao test on 24-year recharge metrics.
  - Exploratory segmented regression break-point analysis (labeled exploratory, no Pettitt).

Outputs:
  outputs/v3/full_record/seasonal_recharge_24yr.csv
  outputs/v3/full_record/seasonal_recharge_summary.json
"""

import json
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import numpy as np
import pandas as pd
from scipy import stats
import pymannkendall as mk

from v2.task3_trend_engine import (
    choose_block_length,
    circular_block_bootstrap_slope,
    RANDOM_SEED,
    N_BOOT,
)
from v3.windows import REGIONS, OUTPUTS_V3_FULL

CSV_PATH = OUTPUTS_V3_FULL / "seasonal_recharge_24yr.csv"
JSON_PATH = OUTPUTS_V3_FULL / "seasonal_recharge_summary.json"


def compute_seasonal_recharge_table(reg_df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes year-by-year dry-season low, post-monsoon peak, rebound,
    monsoon precipitation, and recharge efficiency per region.
    """
    df = reg_df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    rows = []
    years = sorted(df["year"].unique())
    # Exclude 2026 if incomplete monsoon
    years = [y for y in years if y <= 2025]

    for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
        sub = df[df["region"] == reg]

        for y in years:
            # 1. Pre-monsoon dry low: Apr/May of year y (or Mar if Apr missing)
            pre_sub = sub[(sub["year"] == y) & (sub["month"].isin([3, 4, 5]))]
            # 2. Post-monsoon high: Sep/Oct of year y (or Aug/Nov)
            post_sub = sub[(sub["year"] == y) & (sub["month"].isin([8, 9, 10]))]
            # 3. Monsoon precipitation: Jun-Sep total
            monsoon_p = sub[(sub["year"] == y) & (sub["month"].isin([6, 7, 8, 9]))]["power_precip_mm"].sum()

            tws_pre = pre_sub["grace_tws_cm"].min() if not pre_sub.dropna(subset=["grace_tws_cm"]).empty else np.nan
            tws_post = post_sub["grace_tws_cm"].max() if not post_sub.dropna(subset=["grace_tws_cm"]).empty else np.nan

            if not np.isnan(tws_pre) and not np.isnan(tws_post) and monsoon_p > 0:
                rebound_cm = tws_post - tws_pre
                p_cm = monsoon_p * 0.1  # mm to cm
                eff = rebound_cm / p_cm if p_cm > 0 else np.nan
                has_data = True
            else:
                rebound_cm = np.nan
                eff = np.nan
                has_data = False

            rows.append({
                "region": reg,
                "region_name": REGIONS[reg]["name_long"],
                "year": y,
                "pre_monsoon_low_cm": round(tws_pre, 3) if not np.isnan(tws_pre) else np.nan,
                "post_monsoon_peak_cm": round(tws_post, 3) if not np.isnan(tws_post) else np.nan,
                "rebound_cm": round(rebound_cm, 3) if not np.isnan(rebound_cm) else np.nan,
                "monsoon_precip_mm": round(monsoon_p, 1) if monsoon_p > 0 else np.nan,
                "recharge_efficiency_ratio": round(eff, 4) if not np.isnan(eff) else np.nan,
                "valid": has_data,
            })

    return pd.DataFrame(rows)


def fit_exploratory_segmented_regression(years: np.ndarray, y: np.ndarray) -> dict:
    """
    Fits continuous two-phase piecewise linear regression over candidate breakpoint years.
    Returns best breakpoint year, slopes, and RSS.
    """
    n = len(years)
    if n < 8:
        return {"breakpoint_year": None, "note": "Insufficient points"}

    best_rss = float("inf")
    best_bp = None
    best_sl_b = None
    best_sl_a = None

    # Search candidates leaving at least 4 seasons on either side
    candidates = years[4:-4]
    for bp in candidates:
        tb = years[years <= bp]
        yb = y[years <= bp]
        ta = years[years > bp]
        ya = y[years > bp]

        if len(tb) < 3 or len(ta) < 3:
            continue

        def ols_fit(tx, yx):
            A = np.column_stack([np.ones_like(tx), tx])
            coef, _, _, _ = np.linalg.lstsq(A, yx, rcond=None)
            resid = yx - A @ coef
            return float(np.sum(resid ** 2)), float(coef[1])

        rss_b, sl_b = ols_fit(tb, yb)
        rss_a, sl_a = ols_fit(ta, ya)
        tot_rss = rss_b + rss_a

        if tot_rss < best_rss:
            best_rss = tot_rss
            best_bp = int(bp)
            best_sl_b = float(sl_b)
            best_sl_a = float(sl_a)

    return {
        "breakpoint_year": best_bp,
        "slope_before": round(best_sl_b, 5) if best_sl_b is not None else None,
        "slope_after": round(best_sl_a, 5) if best_sl_a is not None else None,
        "status": "EXPLORATORY ONLY — Segmented regression; not used for headline claims",
    }


def run_seasonal_recharge_analysis():
    reg_file = OUTPUTS_V3_FULL / "region_series_2002_2026.csv"
    if not reg_file.exists():
        raise FileNotFoundError(f"Missing regional series: {reg_file}. Run series_extractor first.")

    reg_df = pd.read_csv(reg_file)
    table_df = compute_seasonal_recharge_table(reg_df)
    table_df.to_csv(CSV_PATH, index=False)

    summary_results = []
    print("\nRunning Seasonal Recharge & Efficiency Trends across 24 Monsoon Seasons (2002–2025)...")

    for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
        sub = table_df[(table_df["region"] == reg) & (table_df["valid"] == True)].copy()
        n_seasons = len(sub)

        yrs = sub["year"].values.astype(float)
        rebound = sub["rebound_cm"].values
        eff = sub["recharge_efficiency_ratio"].values

        # 1. Trend in Rebound (Delta TWS)
        ts_reb = stats.theilslopes(rebound, yrs)
        hr_reb = mk.hamed_rao_modification_test(rebound)
        reb_slope = float(ts_reb.slope)
        reb_p = float(hr_reb.p) if not np.isnan(hr_reb.p) else 1.0

        # 2. Trend in Recharge Efficiency (RE)
        ts_eff = stats.theilslopes(eff, yrs)
        hr_eff = mk.hamed_rao_modification_test(eff)
        eff_slope = float(ts_eff.slope)
        eff_p = float(hr_eff.p) if not np.isnan(hr_eff.p) else 1.0

        # 3. Exploratory Segmented Regression on Efficiency
        seg_res = fit_exploratory_segmented_regression(yrs, eff)

        summary_results.append({
            "region": reg,
            "region_name": REGIONS[reg]["name_long"],
            "n_seasons": n_seasons,
            "rebound_mean_cm": round(float(np.mean(rebound)), 2),
            "rebound_slope_cm_yr": round(reb_slope, 4),
            "rebound_p_value": round(reb_p, 5),
            "rebound_verdict": "Decreasing rebound" if (reb_p < 0.05 and reb_slope < 0) else "No detectable trend",
            "efficiency_mean": round(float(np.mean(eff)), 4),
            "efficiency_slope_per_yr": round(eff_slope, 5),
            "efficiency_p_value": round(eff_p, 5),
            "efficiency_verdict": "Declining efficiency" if (eff_p < 0.05 and eff_slope < 0) else "No detectable trend",
            "exploratory_segmented_breakpoint": seg_res["breakpoint_year"],
            "exploratory_slope_before": seg_res["slope_before"],
            "exploratory_slope_after": seg_res["slope_after"],
        })

        print(
            f"  {reg:10s} (N={n_seasons} seasons): Mean Rebound = {np.mean(rebound):.1f} cm "
            f"(slope: {reb_slope:+.3f} cm/yr, p={reb_p:.4f}) | "
            f"Mean Efficiency = {np.mean(eff)*100:.1f}% (slope: {eff_slope*100:+.3f}%/yr, p={eff_p:.4f})"
        )

    summary = {
        "timestamp": datetime.now().isoformat(),
        "period": "2002 to 2025 (24 hydrological monsoon seasons)",
        "definitions": {
            "rebound_cm": "TWS_peak (Sep/Oct) minus TWS_pre (Apr/May) in cm",
            "recharge_efficiency": "rebound_cm / (0.1 * monsoon_precip_mm) [fractional recovery]",
        },
        "results": summary_results,
    }

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"\n[OK] Saved seasonal recharge deliverables:")
    print(f"  CSV:  {CSV_PATH.name} ({len(table_df)} rows)")
    print(f"  JSON: {JSON_PATH.name}")
    return table_df, summary_results


if __name__ == "__main__":
    run_seasonal_recharge_analysis()
