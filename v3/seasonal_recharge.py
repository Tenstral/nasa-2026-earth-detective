"""
NASA Space Apps 2026 – Bengal Hydro Detective
v3 Seasonal Storage Response Dynamics: 24-Season Rebound & Response Ratio
========================================================================
Analyzes hydrological recovery dynamics across 24 monsoon seasons (2002–2025):
  - Pre-monsoon dry season low (Apr/May, or Mar) to post-monsoon peak (Sep/Oct, or Aug/Nov)
    storage rebound alone (Delta TWS, cm) — reported independently so it does not depend
    on the rainfall denominator.
  - Decoupled seasonal monsoon precipitation (P_monsoon, mm) from GPM IMERG V07B (4 complete months Jun-Sep).
  - Seasonal storage response ratio: SRR = Delta TWS (cm) / (0.1 * P_monsoon, cm).
    Limitation: Reflects bulk total water storage change, integrating unsaturated soil moisture
    and surface water bodies alongside groundwater, and does not represent an isolated groundwater recharge coefficient.
  - Explicit flagging of satellite mission gap seasons (2017 lacks post-monsoon peak; 2018 lacks pre-monsoon low).
  - Trend estimation on both storage rebound alone and seasonal storage response ratio.

Outputs:
  outputs/v3/full_record/seasonal_recharge_24yr.csv
  outputs/v3/full_record/seasonal_recharge_summary.json
  outputs/v3/full_record/fig2_seasonal_storage_response_24yr.png
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
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from v3.windows import REGIONS, OUTPUTS_V3_FULL
from v3.trend_engine import run_ess_mann_kendall

CSV_PATH = OUTPUTS_V3_FULL / "seasonal_recharge_24yr.csv"
JSON_PATH = OUTPUTS_V3_FULL / "seasonal_recharge_summary.json"
FIG2_PATH = OUTPUTS_V3_FULL / "fig2_seasonal_storage_response_24yr.png"
SEASONAL_RAIN_CSV = REPO_ROOT / "outputs" / "v3" / "imerg_vs_power" / "rainfall_seasonal_regional.csv"


def compute_seasonal_recharge_table(reg_df: pd.DataFrame, rain_df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes year-by-year dry-season low, post-monsoon peak, storage rebound alone (Delta TWS),
    decoupled IMERG monsoon precipitation, and seasonal storage response ratio per region.
    """
    df = reg_df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    # Filter rain_df to monsoon
    monsoon_rain = rain_df[rain_df["season"] == "monsoon"].copy()

    rows = []
    years = [y for y in sorted(df["year"].unique()) if y <= 2025]

    for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
        sub = df[df["region"] == reg]
        sub_rain = monsoon_rain[monsoon_rain["region"] == reg]

        for y in years:
            # 1. Pre-monsoon dry low: Apr/May of year y (or Mar if Apr missing)
            pre_sub = sub[(sub["year"] == y) & (sub["month"].isin([3, 4, 5]))].dropna(subset=["grace_tws_cm"])
            # 2. Post-monsoon high: Sep/Oct of year y (or Aug/Nov if missing)
            post_sub = sub[(sub["year"] == y) & (sub["month"].isin([8, 9, 10, 11]))].dropna(subset=["grace_tws_cm"])

            tws_pre = float(pre_sub["grace_tws_cm"].min()) if not pre_sub.empty else np.nan
            tws_post = float(post_sub["grace_tws_cm"].max()) if not post_sub.empty else np.nan

            # 3. Decoupled IMERG monsoon rainfall (Jun-Sep complete)
            r_row = sub_rain[sub_rain["year"] == y]
            if not r_row.empty:
                imerg_p = float(r_row["imerg_total_mm"].iloc[0])
                power_p = float(r_row["power_total_mm"].iloc[0]) if pd.notna(r_row["power_total_mm"].iloc[0]) else np.nan
                rain_complete = bool(r_row["is_complete"].iloc[0])
            else:
                imerg_p = np.nan
                power_p = np.nan
                rain_complete = False

            # Check gap artifact
            if y == 2017:
                has_rebound = False
                note = "GRACE mission gap: missing post-monsoon peak"
                rebound_cm = np.nan
                eff_imerg = np.nan
                eff_power = np.nan
            elif y == 2018:
                has_rebound = False
                note = "GRACE-FO launch: missing pre-monsoon low"
                rebound_cm = np.nan
                eff_imerg = np.nan
                eff_power = np.nan
            elif not np.isnan(tws_pre) and not np.isnan(tws_post):
                has_rebound = True
                note = "Complete seasonal pair"
                rebound_cm = tws_post - tws_pre
                p_cm_imerg = imerg_p * 0.1 if (not np.isnan(imerg_p) and imerg_p > 0) else np.nan
                p_cm_power = power_p * 0.1 if (not np.isnan(power_p) and power_p > 0) else np.nan
                eff_imerg = rebound_cm / p_cm_imerg if (p_cm_imerg and not np.isnan(p_cm_imerg)) else np.nan
                eff_power = rebound_cm / p_cm_power if (p_cm_power and not np.isnan(p_cm_power)) else np.nan
            else:
                has_rebound = False
                note = "Incomplete satellite observations"
                rebound_cm = np.nan
                eff_imerg = np.nan
                eff_power = np.nan

            rows.append({
                "region": reg,
                "region_name": REGIONS[reg]["name_long"],
                "year": y,
                "pre_monsoon_low_cm": round(tws_pre, 3) if not np.isnan(tws_pre) else np.nan,
                "post_monsoon_peak_cm": round(tws_post, 3) if not np.isnan(tws_post) else np.nan,
                "rebound_cm": round(rebound_cm, 3) if not np.isnan(rebound_cm) else np.nan,
                "monsoon_precip_imerg_mm": round(imerg_p, 1) if not np.isnan(imerg_p) else np.nan,
                "monsoon_precip_power_mm": round(power_p, 1) if not np.isnan(power_p) else np.nan,
                "storage_response_ratio_imerg": round(eff_imerg, 4) if not np.isnan(eff_imerg) else np.nan,
                "storage_response_ratio_power": round(eff_power, 4) if not np.isnan(eff_power) else np.nan,
                "valid": has_rebound,
                "note": note,
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
        raise FileNotFoundError(f"Missing regional series: {reg_file}")
    if not SEASONAL_RAIN_CSV.exists():
        raise FileNotFoundError(f"Missing seasonal rain series: {SEASONAL_RAIN_CSV}")

    reg_df = pd.read_csv(reg_file)
    rain_df = pd.read_csv(SEASONAL_RAIN_CSV)

    table_df = compute_seasonal_recharge_table(reg_df, rain_df)
    table_df.to_csv(CSV_PATH, index=False)

    summary_results = []
    print("\nRunning Seasonal Storage Response Dynamics (2002–2025)...")

    raw_results = []
    for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
        sub = table_df[(table_df["region"] == reg) & (table_df["valid"] == True)].copy()
        n_seasons = len(sub)

        yrs = sub["year"].values.astype(float)
        rebound = sub["rebound_cm"].values
        eff_imerg = sub["storage_response_ratio_imerg"].values
        eff_power = sub["storage_response_ratio_power"].dropna().values

        # 1. Storage Rebound ALONE (Delta TWS, cm)
        ess_reb = run_ess_mann_kendall(yrs, rebound, alpha=0.05)

        # 2. Storage Response Ratio with IMERG
        ess_eff = run_ess_mann_kendall(yrs, eff_imerg, alpha=0.05)

        # 3. Old POWER Storage Response Ratio (for comparison)
        if len(eff_power) >= 8:
            yrs_pow = sub.dropna(subset=["storage_response_ratio_power"])["year"].values.astype(float)
            ess_pow = run_ess_mann_kendall(yrs_pow, eff_power, alpha=0.05)
            pow_slope = ess_pow["slope"]
            pow_p = ess_pow["p_value"]
            pow_mean = float(np.mean(eff_power))
        else:
            pow_slope = pow_p = pow_mean = np.nan

        # 4. Exploratory Segmented Regression on IMERG Response Ratio
        seg_res = fit_exploratory_segmented_regression(yrs, eff_imerg)

        raw_results.append({
            "region": reg,
            "region_name": REGIONS[reg]["name_long"],
            "n_valid_seasons": n_seasons,
            "rebound_alone_mean_cm": round(float(np.mean(rebound)), 2),
            "rebound_alone_slope_cm_yr": round(ess_reb["slope"], 4),
            "rebound_alone_ci95": [round(ess_reb["ci_low"], 3), round(ess_reb["ci_high"], 3)],
            "rebound_alone_p_value": round(ess_reb["p_value"], 5),
            "response_ratio_mean": round(float(np.mean(eff_imerg)), 4),
            "response_ratio_slope_per_yr": round(ess_eff["slope"], 5),
            "response_ratio_ci95": [round(ess_eff["ci_low"], 4), round(ess_eff["ci_high"], 4)],
            "response_ratio_p_value": round(ess_eff["p_value"], 5),
            "old_power_response_ratio_mean": round(pow_mean, 4) if not np.isnan(pow_mean) else None,
            "old_power_response_ratio_slope_per_yr": round(pow_slope, 5) if not np.isnan(pow_slope) else None,
            "old_power_response_ratio_p_value": round(pow_p, 5) if not np.isnan(pow_p) else None,
            "exploratory_segmented_breakpoint": seg_res["breakpoint_year"],
            "exploratory_slope_before": seg_res["slope_before"],
            "exploratory_slope_after": seg_res["slope_after"],
        })

    # Within-family Benjamini-Hochberg FDR calculation across the 6 entities
    reb_p_vals = [r["rebound_alone_p_value"] for r in raw_results]
    eff_p_vals = [r["response_ratio_p_value"] for r in raw_results]

    def calc_bh_fdr(p_values):
        m = len(p_values)
        s_idx = np.argsort(p_values)
        q_vals = np.zeros(m)
        cummin = 1.0
        for rank in range(m, 0, -1):
            idx = s_idx[rank - 1]
            p = p_values[idx]
            q = (p * m) / rank
            cummin = min(cummin, q)
            q_vals[idx] = min(1.0, cummin)
        return q_vals

    reb_q_vals = calc_bh_fdr(reb_p_vals)
    eff_q_vals = calc_bh_fdr(eff_p_vals)

    def assign_verdict(p, q, slope, ci_low, ci_high):
        ci_excludes_zero = (ci_low > 0 or ci_high < 0)
        if q < 0.05 and ci_excludes_zero:
            return "Significant increase" if slope > 0 else "Significant decrease"
        elif p < 0.05:
            return "Suggestive increase" if slope > 0 else "Suggestive decrease"
        else:
            return "No detectable trend"

    summary_results = []
    for i, r in enumerate(raw_results):
        r["rebound_alone_fdr_q"] = round(float(reb_q_vals[i]), 5)
        r["rebound_alone_verdict"] = assign_verdict(
            r["rebound_alone_p_value"], reb_q_vals[i],
            r["rebound_alone_slope_cm_yr"], r["rebound_alone_ci95"][0], r["rebound_alone_ci95"][1]
        )

        r["response_ratio_fdr_q"] = round(float(eff_q_vals[i]), 5)
        r["response_ratio_verdict"] = assign_verdict(
            r["response_ratio_p_value"], eff_q_vals[i],
            r["response_ratio_slope_per_yr"], r["response_ratio_ci95"][0], r["response_ratio_ci95"][1]
        )

        # Backward compatibility aliases
        r["efficiency_imerg_mean"] = r["response_ratio_mean"]
        r["efficiency_imerg_slope_per_yr"] = r["response_ratio_slope_per_yr"]
        r["efficiency_imerg_ci95"] = r["response_ratio_ci95"]
        r["efficiency_imerg_p_value"] = r["response_ratio_p_value"]
        r["efficiency_imerg_verdict"] = r["response_ratio_verdict"]
        r["old_power_efficiency_mean"] = r["old_power_response_ratio_mean"]
        r["old_power_efficiency_slope_per_yr"] = r["old_power_response_ratio_slope_per_yr"]
        r["old_power_efficiency_p_value"] = r["old_power_response_ratio_p_value"]

        summary_results.append(r)
        print(
            f"  {r['region']:10s} (N={r['n_valid_seasons']} seasons): Mean Rebound = {r['rebound_alone_mean_cm']:.1f} cm "
            f"(slope: {r['rebound_alone_slope_cm_yr']:+.3f} cm/yr, p={r['rebound_alone_p_value']:.4f}, verdict={r['rebound_alone_verdict']}) | "
            f"Response Ratio = {r['response_ratio_mean']*100:.1f}% (slope: {r['response_ratio_slope_per_yr']*100:+.3f}%/yr, p={r['response_ratio_p_value']:.4f}, q={r['response_ratio_fdr_q']:.4f}, verdict={r['response_ratio_verdict']})"
        )

    summary = {
        "timestamp": datetime.now().isoformat(),
        "period": "2002 to 2025 (24 hydrological monsoon seasons; 22 complete observation pairs)",
        "definitions": {
            "rebound_alone_cm": "TWS_peak (Sep/Oct) minus TWS_pre (Apr/May) in cm (independent of rainfall)",
            "seasonal_storage_response_ratio_imerg": "rebound_cm / (0.1 * imerg_monsoon_precip_mm) [fractional bulk storage recovery]",
            "limitation": "The seasonal storage response ratio (ΔTWS / P_monsoon) reflects bulk total water storage change, integrating unsaturated soil moisture and surface water bodies alongside groundwater, and does not represent an isolated groundwater recharge coefficient.",
        },
        "results": summary_results,
    }

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Plot Figure 2
    plot_fig2_seasonal_storage_response(table_df)

    print(f"\n[OK] Saved seasonal recharge deliverables:")
    print(f"  CSV:    {CSV_PATH.name} ({len(table_df)} rows)")
    print(f"  JSON:   {JSON_PATH.name}")
    print(f"  Figure: {FIG2_PATH.name}")
    return table_df, summary_results


def plot_fig2_seasonal_storage_response(df: pd.DataFrame):
    valid_df = df[df["valid"] == True].copy()

    reg_colors = {
        "NW": "#dc2626", "NE": "#8b5cf6", "Central": "#0284c7",
        "SW": "#059669", "SE": "#ea580c", "National": "#1f2937",
    }

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

    flood_years = [2004, 2007, 2020, 2022]
    for fy in flood_years:
        ax1.axvline(fy, color="#94a3b8", linestyle="--", alpha=0.6)
        ax2.axvline(fy, color="#94a3b8", linestyle="--", alpha=0.6)

    # Panel 1: Storage Rebound Alone (Delta TWS, cm)
    for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
        sub = valid_df[valid_df["region"] == reg]
        ax1.plot(sub["year"], sub["rebound_cm"], marker="o", color=reg_colors[reg],
                 label=REGIONS[reg]["name_long"], lw=1.8 if reg != "National" else 2.5,
                 linestyle="-" if reg != "National" else "--")

    ax1.set_title("A. Storage Rebound Alone (ΔTWS = Peak - Dry Season Low, cm) [Independent of Rainfall]",
                  fontsize=12, fontweight="bold")
    ax1.set_ylabel("Storage Rebound (cm)", fontsize=10)
    ax1.grid(True, linestyle=":", alpha=0.5)
    ax1.legend(loc="upper right", ncol=3, fontsize=8)

    # Panel 2: Seasonal Storage Response Ratio (%) with IMERG
    for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
        sub = valid_df[valid_df["region"] == reg]
        eff_pct = sub["storage_response_ratio_imerg"] * 100.0
        ax2.plot(sub["year"], eff_pct, marker="s", color=reg_colors[reg],
                 label=f"{reg} Response Ratio", lw=1.8 if reg != "National" else 2.5,
                 linestyle="-" if reg != "National" else "--")

    ax2.set_title("B. Seasonal Storage Response Ratio: [ΔTWS (cm) / (0.1 × IMERG Monsoon Precip (cm))] × 100%\n"
                  "Limitation: Integrates bulk total water storage (soil moisture + surface water + groundwater), not isolated groundwater recharge",
                  fontsize=11, fontweight="bold")
    ax2.set_ylabel("Storage Response Ratio (%)", fontsize=10)
    ax2.set_xlabel("Hydrological Year (2002–2025)", fontsize=11)
    ax2.grid(True, linestyle=":", alpha=0.5)

    # Annotate flood events
    for fy in flood_years:
        ax1.text(fy, 75, f"{fy} Flood", rotation=90, verticalalignment="bottom", fontsize=8, color="#475569")

    # Annotate 2017-2018 mission gap
    ax1.axvspan(2017 - 0.4, 2018 + 0.4, color="#fee2e2", alpha=0.5, zorder=0)
    ax2.axvspan(2017 - 0.4, 2018 + 0.4, color="#fee2e2", alpha=0.5, zorder=0)
    ax1.text(2017.5, 30, "GRACE/GRACE-FO\nMission Gap", horizontalalignment="center", fontsize=8, color="#b91c1c", fontweight="bold")

    plt.suptitle("Bengal Basin Hydrological Recovery & Storage Response Dynamics (2002–2025)\n"
                 "PRELIMINARY — 24 Monsoon Seasons Analysis | Team Tenstral", fontsize=13, fontweight="bold", y=0.98)
    plt.tight_layout()
    plt.savefig(FIG2_PATH, dpi=300)
    plt.close()


if __name__ == "__main__":
    run_seasonal_recharge_analysis()
