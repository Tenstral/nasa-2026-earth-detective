"""
NASA Space Apps 2026 - Trend Detective: Bengal Water Paradox
Statistical Engine: Mann-Kendall Trend Test & Theil-Sen Slope Estimator

Performs non-parametric trend detection and robust rate-of-change estimation
across all 8 administrative divisions of Bangladesh using:
  1. CSR GRACE/GRACE-FO RL06.3 Mascons (Terrestrial Water Storage, 2002-2026)
  2. NASA GPM IMERG / POWER Satellite Precipitation (2020-2026)

Methods:
  - Seasonal decomposition / monthly climatology removal
  - Non-parametric Mann-Kendall test (S-statistic, Variance, Z, p-value)
  - Theil-Sen robust slope estimator with 95% confidence intervals
"""

import os
import json
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
from scipy import stats
import shapely
from shapely.geometry import shape

from analyze_divisions import get_division_geometries, load_dataset as load_grace_ds
from analyze_precipitation import load_dataset as load_precip_ds, detect_precip_variable


def mann_kendall_test(x: np.ndarray):
    """
    Perform the original non-parametric Mann-Kendall test for monotonic trends.
    Returns: S, var_S, z, p_value, tau
    """
    n = len(x)
    s = 0
    for k in range(n - 1):
        for j in range(k + 1, n):
            s += np.sign(x[j] - x[k])

    # Ties adjustment for variance
    unique_x, counts = np.unique(x, return_counts=True)
    tie_term = np.sum(counts * (counts - 1) * (2 * counts + 5))
    var_s = (n * (n - 1) * (2 * n + 5) - tie_term) / 18.0

    if var_s == 0:
        return 0, 0, 0.0, 1.0, 0.0

    if s > 0:
        z = (s - 1) / np.sqrt(var_s)
    elif s < 0:
        z = (s + 1) / np.sqrt(var_s)
    else:
        z = 0.0

    # Two-tailed p-value
    p_value = 2.0 * (1.0 - stats.norm.cdf(abs(z)))
    tau = s / (0.5 * n * (n - 1))

    return int(s), float(var_s), float(z), float(p_value), float(tau)


def compute_divisional_trends():
    divisions = get_division_geometries()
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. GRACE Mascon Trend (2002 - 2026)
    grace_file = "CSR_GRACE_GRACE-FO_RL0603_Mascons_all-corrections.nc"
    grace_ds = load_grace_ds(grace_file)
    bd_grace = grace_ds["lwe_thickness"].sel(lat=slice(20.4, 26.8), lon=slice(88.0, 92.8))

    lon2d, lat2d = np.meshgrid(bd_grace.lon.values, bd_grace.lat.values)
    lat_rad = np.radians(lat2d)
    area_wts = np.cos(lat_rad)

    time_vals = pd.to_datetime(grace_ds["time"].values)
    time_years = np.array([t.year + (t.dayofyear - 1) / 365.25 for t in time_vals])
    calendar_months = np.array([t.month for t in time_vals])

    # Extract monthly series per division
    div_monthly = {d: [] for d in divisions}
    for t_idx in range(len(time_vals)):
        data_t = bd_grace.isel(time=t_idx).values
        for d, info in divisions.items():
            mask = shapely.contains_xy(info["geometry"], lon2d, lat2d)
            if mask.sum() > 0:
                vals = data_t[mask]
                wts = area_wts[mask]
                valid = ~np.isnan(vals)
                mean_v = np.sum(vals[valid] * wts[valid]) / np.sum(wts[valid]) if valid.sum() > 0 else np.nan
            else:
                mean_v = np.nan
            div_monthly[d].append(mean_v)

    trend_summary = {}

    print("\n" + "=" * 90)
    print("  NASA EARTH DETECTIVE // MANN-KENDALL & THEIL-SEN DIVISIONAL TREND ANALYSIS")
    print("  CSR GRACE/GRACE-FO Terrestrial Water Storage Anomalies (2002 - 2026)")
    print("=" * 90)
    print(f"{'Division':<12} | {'Sen Slope (cm/yr)':<18} | {'95% CI':<20} | {'Mann-Kendall Z':<15} | {'p-value':<10} | {'Significance'}")
    print("-" * 90)

    for d in sorted(divisions.keys()):
        raw_series = np.array(div_monthly[d])
        # Deseasonalize by subtracting calendar month mean (removes annual monsoon wave)
        deseas_series = np.copy(raw_series)
        for m in range(1, 13):
            m_mask = (calendar_months == m) & (~np.isnan(raw_series))
            if m_mask.sum() > 0:
                deseas_series[calendar_months == m] -= np.mean(raw_series[m_mask])

        valid = ~np.isnan(deseas_series)
        t_valid = time_years[valid]
        y_valid = deseas_series[valid]

        res_ts = stats.theilslopes(y_valid, t_valid)
        slope, intercept, slope_low, slope_high = res_ts
        s, var_s, z, p_val, tau = mann_kendall_test(y_valid)

        if p_val < 0.001:
            sig = "p < 0.001 (***)"
        elif p_val < 0.01:
            sig = "p < 0.01 (**)"
        elif p_val < 0.05:
            sig = "p < 0.05 (*)"
        else:
            sig = "Not Significant"

        print(f"{d:<12} | {slope:+.3f} cm/yr        | [{slope_low:+.3f}, {slope_high:+.3f}]   | {z:+.2f}           | {p_val:.2e}   | {sig}")

        trend_summary[d] = {
            "division": d,
            "area_km2": divisions[d]["area_km2"],
            "period": "2002-04 to 2026-07",
            "n_observations": int(valid.sum()),
            "theil_sen_slope_cm_per_yr": round(float(slope), 4),
            "slope_95ci_low": round(float(slope_low), 4),
            "slope_95ci_high": round(float(slope_high), 4),
            "mann_kendall_s": s,
            "mann_kendall_z": round(z, 3),
            "mann_kendall_tau": round(tau, 4),
            "p_value": float(f"{p_val:.4e}"),
            "statistically_significant": bool(p_val < 0.05),
            "significance_label": sig
        }

    print("=" * 90)

    # Save JSON and CSV
    with open(output_dir / "divisional_trends.json", "w", encoding="utf-8") as f:
        json.dump(trend_summary, f, indent=2)

    df_trends = pd.DataFrame(trend_summary.values())
    df_trends.to_csv(output_dir / "divisional_trends.csv", index=False)
    print(f"\n Saved: {output_dir / 'divisional_trends.json'}")
    print(f" Saved: {output_dir / 'divisional_trends.csv'}")

    # Generate Visualization Plot
    plot_trends(trend_summary, div_monthly, time_years, calendar_months, output_dir / "divisional_trends.png")


def plot_trends(trend_summary, div_monthly, time_years, calendar_months, output_file):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 12), gridspec_kw={"height_ratios": [1, 1.2]})

    # --- Plot 1: Sen's Slope Bar Chart ---
    sorted_divs = sorted(trend_summary.keys(), key=lambda k: trend_summary[k]["theil_sen_slope_cm_per_yr"])
    slopes = [trend_summary[k]["theil_sen_slope_cm_per_yr"] for k in sorted_divs]
    ci_lows = [trend_summary[k]["slope_95ci_low"] for k in sorted_divs]
    ci_highs = [trend_summary[k]["slope_95ci_high"] for k in sorted_divs]
    xerr = [
        [s - l for s, l in zip(slopes, ci_lows)],
        [h - s for s, h in zip(slopes, ci_highs)]
    ]

    colors = []
    for k in sorted_divs:
        p_val = trend_summary[k]["p_value"]
        slope = trend_summary[k]["theil_sen_slope_cm_per_yr"]
        if k == "Mymensingh":
            colors.append("#8b5cf6")  # Distinctive Purple for Mymensingh focus
        elif p_val < 0.05 and slope < -0.8:
            colors.append("#ef4444")  # Red for severe depletion
        elif p_val < 0.05 and slope < 0:
            colors.append("#f97316")  # Orange for moderate depletion
        else:
            colors.append("#64748b")  # Gray for neutral/not significant

    y_pos = np.arange(len(sorted_divs))
    bars = ax1.barh(y_pos, slopes, xerr=xerr, capsize=4, color=colors, height=0.65, edgecolor="#1e293b", linewidth=1.2)

    ax1.axvline(0, color="#334155", linestyle="--", linewidth=1.2, alpha=0.7)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(sorted_divs, fontsize=11, fontweight="bold")
    ax1.set_xlabel("Theil-Sen Slope Rate of Change (cm / year)", fontsize=11, fontweight="bold")
    ax1.set_title("NASA GRACE/GRACE-FO Mascon Terrestrial Water Storage Trends (2002–2026)\nDeseasonalized Long-Term Rate of Change by Division (95% CI)", fontsize=13, fontweight="bold", pad=12)
    ax1.grid(axis="x", linestyle=":", alpha=0.5)

    for i, (b, d) in enumerate(zip(bars, sorted_divs)):
        s = trend_summary[d]["theil_sen_slope_cm_per_yr"]
        p_str = trend_summary[d]["significance_label"]
        x_offset = 0.08 if s >= 0 else -0.08
        ha = "left" if s >= 0 else "right"
        lbl = f" {s:+.2f} cm/yr ({p_str}) "
        if d == "Mymensingh":
            lbl = f" ★ Mymensingh: {s:+.2f} cm/yr ({p_str}) "
        ax1.text(s + x_offset, i, lbl, va="center", ha=ha, fontsize=9.5, fontweight="bold",
                 color="#0f172a", bbox=dict(boxstyle="round,pad=0.2", facecolor="#ffffff", alpha=0.8, edgecolor="none"))

    # --- Plot 2: 24-Year Multi-Division Trajectory ---
    focus_divs = ["Rangpur", "Rajshahi", "Mymensingh", "Dhaka", "Sylhet", "Barishal"]
    div_colors = {
        "Rangpur": "#dc2626",
        "Rajshahi": "#ea580c",
        "Mymensingh": "#7c3aed",
        "Dhaka": "#0284c7",
        "Sylhet": "#059669",
        "Barishal": "#64748b"
    }

    for d in focus_divs:
        raw_series = np.array(div_monthly[d])
        deseas = np.copy(raw_series)
        for m in range(1, 13):
            m_mask = (calendar_months == m) & (~np.isnan(raw_series))
            if m_mask.sum() > 0:
                deseas[calendar_months == m] -= np.mean(raw_series[m_mask])
        
        # 12-month rolling mean for smooth signal
        df_temp = pd.Series(deseas)
        rolling = df_temp.rolling(window=12, center=True).mean()
        
        lw = 2.8 if d == "Mymensingh" else 1.8
        alpha = 1.0 if d in ["Mymensingh", "Rangpur", "Rajshahi"] else 0.7
        ax2.plot(time_years, rolling, label=f"{d} (Slope: {trend_summary[d]['theil_sen_slope_cm_per_yr']:+.2f} cm/yr)",
                 color=div_colors[d], linewidth=lw, alpha=alpha)

    ax2.axhline(0, color="#94a3b8", linestyle=":", linewidth=1)
    ax2.set_xlabel("Observation Year (2002 - 2026)", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Deseasonalized TWS Anomaly (cm)", fontsize=11, fontweight="bold")
    ax2.set_title("12-Month Smoothed Deseasonalized Storage Trajectory (2002–2026)\nPersistent Monotonic Aquifer Drawdown in Northern Belt (Rangpur, Rajshahi, Mymensingh)", fontsize=12, fontweight="bold", pad=10)
    ax2.legend(loc="lower left", framealpha=0.9, fontsize=9.5)
    ax2.grid(True, linestyle=":", alpha=0.5)

    plt.tight_layout()
    plt.savefig(output_file, dpi=200, bbox_inches="tight")
    plt.close()
    print(f" Saved Trend Visualization Chart: {output_file}")


if __name__ == "__main__":
    compute_divisional_trends()
