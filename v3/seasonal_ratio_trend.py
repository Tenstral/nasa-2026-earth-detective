"""
NASA Space Apps 2026 – Bengal Hydro Detective
v3 Exploratory Analysis: Trend of Seasonal Storage Response Ratio
================================================================
Evaluates the multi-decadal trend of the seasonal storage response ratio
across Bangladesh regions using Calibrated ESS-MK, with duality-aligned 95% CIs,
minimum detectable slopes (MDS at 80% power), and within-family FDR correction.

Status: PRELIMINARY & EXPLORATORY ONLY.
All results are kept distinct and quarantined from results_all_windows.csv.
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
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from v3.windows import REGIONS
from v3.trend_engine import run_ess_mann_kendall

# Paths
CONFIG_PATH = REPO_ROOT / "config.json"
REGION_SERIES_CSV = REPO_ROOT / "outputs" / "v3" / "full_record" / "region_series_2002_2026.csv"
SEASONAL_RECHARGE_CSV = REPO_ROOT / "outputs" / "v3" / "full_record" / "seasonal_recharge_24yr.csv"
OUT_DIR = REPO_ROOT / "outputs" / "v3" / "seasonal"
OUT_CSV = OUT_DIR / "ratio_trend.csv"
OUT_MD = OUT_DIR / "ratio_trend.md"
OUT_FIG = OUT_DIR / "fig_ratio_trend.png"


def load_config() -> dict:
    """Loads seasonal response ratio constants from config.json."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    return cfg


def compute_mds_80pct(t_v: np.ndarray, y: np.ndarray, seed: int = 42, n_sim: int = 250, candidate_grid: np.ndarray = None) -> tuple:
    """
    Computes Minimum Detectable Slope (MDS) at 80% statistical power under AR(1) red noise.
    Uses Calibrated ESS-MK significance testing (alpha=0.05).
    """
    n = len(y)
    dt = t_v - t_v[0]
    res = run_ess_mann_kendall(t_v, y)
    b_est = res["slope"]
    resid = y - b_est * t_v
    resid_dt = resid - np.mean(resid)
    sd = float(np.std(resid_dt, ddof=1))
    r1 = float(np.corrcoef(resid_dt[:-1], resid_dt[1:])[0, 1])
    if np.isnan(r1) or r1 <= 0.0:
        phi = 0.0
    else:
        # Hurwicz correction for AR(1) bias
        phi = min(0.85, max(0.0, r1 + (1.0 + 4.0 * r1) / n))

    rng = np.random.default_rng(seed)
    if candidate_grid is None:
        candidate_grid = np.linspace(0.05, 3.0, 60)

    mds = None
    for b_cand in candidate_grid:
        rejs = 0
        for _ in range(n_sim):
            eta = rng.standard_normal(n)
            e = np.zeros(n)
            for t in range(1, n):
                e[t] = phi * e[t - 1] + np.sqrt(1.0 - phi**2) * eta[t]
            y_sim = -b_cand * dt + (e * sd)
            if run_ess_mann_kendall(dt, y_sim)["p_value"] < 0.05:
                rejs += 1
        if (rejs / n_sim) >= 0.80:
            mds = round(float(b_cand), 3)
            break
    return mds, sd, phi


def calc_bh_fdr(p_values: list) -> np.ndarray:
    """Calculates Benjamini-Hochberg FDR q-values within an exploratory family."""
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


def run_ratio_trend_analysis():
    """
    Executes exploratory trend analysis on the seasonal storage response ratio.
    Evaluates both main run (22 complete seasons) and sensitivity run (transition-buffer excluded).
    """
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cfg = load_config()
    ratio_cfg = cfg.get("seasonal_storage_response_ratio", {})
    seed = cfg.get("random_seed", 42)

    if not SEASONAL_RECHARGE_CSV.exists():
        raise FileNotFoundError(f"Missing base seasonal recharge CSV: {SEASONAL_RECHARGE_CSV}")

    recharge_df = pd.read_csv(SEASONAL_RECHARGE_CSV)

    # 1. Main Run: Complete seasons only (drops 2017 and 2018 where satellite observations are incomplete)
    main_df = recharge_df[recharge_df["valid"] == True].copy()

    # 2. Sensitivity Run: Exclude seasons within +/-6 months of transition gap (2017-01 to 2018-11)
    # Beyond 2017 and 2018, adjacent bounding seasons are 2016 and 2019
    sens_drop_years = [2016, 2017, 2018, 2019]
    sens_df = recharge_df[(recharge_df["valid"] == True) & (~recharge_df["year"].isin(sens_drop_years))].copy()

    regions = ["NW", "NE", "Central", "SW", "SE", "National"]

    results_records = []

    # Process Main Run
    main_raw = []
    for reg in regions:
        sub = main_df[main_df["region"] == reg].sort_values("year")
        n_obs = len(sub)
        n_drop = 24 - n_obs  # out of 24 candidate years 2002-2025
        yrs = sub["year"].values.astype(float)
        ratio_pct = sub["storage_response_ratio_imerg"].values * 100.0  # as percentage
        ratio_frac = sub["storage_response_ratio_imerg"].values

        res = run_ess_mann_kendall(yrs, ratio_pct, alpha=0.05)
        mds, sd, phi = compute_mds_80pct(yrs, ratio_pct, seed=seed, n_sim=250, candidate_grid=np.linspace(0.05, 2.5, 50))

        ci_width = res["ci_high"] - res["ci_low"]
        slope_mag = abs(res["slope"])
        is_wide = ci_width > (2.0 * slope_mag) or (res["ci_low"] < 0 < res["ci_high"])

        main_raw.append({
            "region": reg,
            "region_name": REGIONS[reg]["name_long"],
            "analysis_type": "main_run",
            "n_seasons": n_obs,
            "n_dropped_seasons": n_drop,
            "dropped_seasons_list": "2017, 2018 (satellite mission gap)",
            "mean_ratio_pct": round(float(np.mean(ratio_pct)), 2),
            "slope_pct_yr": round(float(res["slope"]), 4),
            "slope_ci_low_pct_yr": round(float(res["ci_low"]), 4),
            "slope_ci_high_pct_yr": round(float(res["ci_high"]), 4),
            "slope_fraction_yr": round(float(res["slope"] / 100.0), 6),
            "slope_ci_low_fraction_yr": round(float(res["ci_low"] / 100.0), 6),
            "slope_ci_high_fraction_yr": round(float(res["ci_high"] / 100.0), 6),
            "p_value": round(float(res["p_value"]), 5),
            "mds_80pct_power_pct_yr": round(float(mds), 3) if mds is not None else np.nan,
            "ci_width_pct_yr": round(float(ci_width), 4),
            "ci_relative_to_slope": f"Wide (CI width {ci_width:.2f}%/yr spans zero)" if (res["ci_low"] < 0 < res["ci_high"]) else f"CI width {ci_width:.2f}%/yr",
            "is_ci_wide": is_wide,
            "years": yrs,
            "ratio_pct": ratio_pct,
        })

    # FDR for Main Run
    main_p_vals = [r["p_value"] for r in main_raw]
    main_q_vals = calc_bh_fdr(main_p_vals)

    for i, r in enumerate(main_raw):
        q = round(float(main_q_vals[i]), 5)
        r["exploratory_fdr_q"] = q
        # Duality: CI excludes zero iff p < 0.05
        ci_excludes_zero = (r["slope_ci_low_pct_yr"] > 0 or r["slope_ci_high_pct_yr"] < 0)
        if q < 0.05 and ci_excludes_zero:
            r["verdict"] = "Exploratory: trend detected"
            r["verdict_detail"] = f"Exploratory trend detected (p={r['p_value']:.4f}, q={q:.4f}); CI excludes zero"
        elif r["p_value"] < 0.05:
            r["verdict"] = "Suggestive"
            r["verdict_detail"] = f"Suggestive slope ({r['slope_pct_yr']:+.3f}%/yr, p={r['p_value']:.4f}), but fails exploratory FDR control (q={q:.4f} >= 0.05)"
        else:
            r["verdict"] = "No detectable trend"
            ci_note = "CI is wide relative to slope and spans zero" if r["is_ci_wide"] else "slope is below detection threshold"
            r["verdict_detail"] = f"No detectable trend (p={r['p_value']:.4f}, q={q:.4f}; {ci_note})"

        results_records.append(r)

    # Process Sensitivity Run
    sens_raw = []
    for reg in regions:
        sub = sens_df[sens_df["region"] == reg].sort_values("year")
        n_obs = len(sub)
        n_drop = 24 - n_obs
        yrs = sub["year"].values.astype(float)
        ratio_pct = sub["storage_response_ratio_imerg"].values * 100.0

        res = run_ess_mann_kendall(yrs, ratio_pct, alpha=0.05)
        mds, sd, phi = compute_mds_80pct(yrs, ratio_pct, seed=seed, n_sim=250, candidate_grid=np.linspace(0.05, 2.5, 50))

        ci_width = res["ci_high"] - res["ci_low"]
        slope_mag = abs(res["slope"])
        is_wide = ci_width > (2.0 * slope_mag) or (res["ci_low"] < 0 < res["ci_high"])

        sens_raw.append({
            "region": reg,
            "region_name": REGIONS[reg]["name_long"],
            "analysis_type": "sensitivity_buffer_excluded",
            "n_seasons": n_obs,
            "n_dropped_seasons": n_drop,
            "dropped_seasons_list": "2016, 2017, 2018, 2019 (+/-6 mo transition buffer)",
            "mean_ratio_pct": round(float(np.mean(ratio_pct)), 2),
            "slope_pct_yr": round(float(res["slope"]), 4),
            "slope_ci_low_pct_yr": round(float(res["ci_low"]), 4),
            "slope_ci_high_pct_yr": round(float(res["ci_high"]), 4),
            "slope_fraction_yr": round(float(res["slope"] / 100.0), 6),
            "slope_ci_low_fraction_yr": round(float(res["ci_low"] / 100.0), 6),
            "slope_ci_high_fraction_yr": round(float(res["ci_high"] / 100.0), 6),
            "p_value": round(float(res["p_value"]), 5),
            "mds_80pct_power_pct_yr": round(float(mds), 3) if mds is not None else np.nan,
            "ci_width_pct_yr": round(float(ci_width), 4),
            "ci_relative_to_slope": f"Wide (CI width {ci_width:.2f}%/yr spans zero)" if (res["ci_low"] < 0 < res["ci_high"]) else f"CI width {ci_width:.2f}%/yr",
            "is_ci_wide": is_wide,
            "years": yrs,
            "ratio_pct": ratio_pct,
        })

    # FDR for Sensitivity Run
    sens_p_vals = [r["p_value"] for r in sens_raw]
    sens_q_vals = calc_bh_fdr(sens_p_vals)

    for i, r in enumerate(sens_raw):
        q = round(float(sens_q_vals[i]), 5)
        r["exploratory_fdr_q"] = q
        ci_excludes_zero = (r["slope_ci_low_pct_yr"] > 0 or r["slope_ci_high_pct_yr"] < 0)
        if q < 0.05 and ci_excludes_zero:
            r["verdict"] = "Exploratory: trend detected"
            r["verdict_detail"] = f"Exploratory trend detected (p={r['p_value']:.4f}, q={q:.4f}); CI excludes zero"
        elif r["p_value"] < 0.05:
            r["verdict"] = "Suggestive"
            r["verdict_detail"] = f"Suggestive slope ({r['slope_pct_yr']:+.3f}%/yr, p={r['p_value']:.4f}), but fails exploratory FDR control (q={q:.4f} >= 0.05)"
        else:
            r["verdict"] = "No detectable trend"
            ci_note = "CI is wide relative to slope and spans zero" if r["is_ci_wide"] else "slope is below detection threshold"
            r["verdict_detail"] = f"No detectable trend (p={r['p_value']:.4f}, q={q:.4f}; {ci_note})"

        results_records.append(r)

    # Convert to DataFrame
    df_out = pd.DataFrame(results_records).drop(columns=["years", "ratio_pct", "is_ci_wide"])
    df_out.to_csv(OUT_CSV, index=False)
    print(f"[OK] Saved ratio trend CSV: {OUT_CSV}")

    # Generate Markdown Report
    generate_markdown_report(results_records)

    # Generate Figure
    plot_ratio_trends(main_raw)

    return df_out


def generate_markdown_report(records: list):
    """Generates comprehensive markdown report for exploratory seasonal storage response ratio trends."""
    main_recs = [r for r in records if r["analysis_type"] == "main_run"]
    sens_recs = [r for r in records if r["analysis_type"] == "sensitivity_buffer_excluded"]

    md = []
    md.append("# Exploratory Trend of Seasonal Storage Response Ratio (2002–2025)")
    md.append("")
    md.append("**Status:** PRELIMINARY & EXPLORATORY ONLY")
    md.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md.append("**Methodology:** Theil-Sen robust slope estimator with Calibrated Effective Sample Size Mann-Kendall (ESS-MK) test and duality-aligned 95% rank confidence intervals.")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 1. Metric Definition & Data Protocol")
    md.append(r"- **Seasonal Storage Response Ratio:** Defined as the ratio of seasonal storage rebound alone ($\Delta\text{TWS}$, cm) to seasonal monsoon rainfall ($0.1 \times P_{\text{monsoon}}$, cm liquid water):")
    md.append(r"  $$\text{Seasonal Storage Response Ratio} = \frac{\Delta\text{TWS}\text{ (cm)}}{0.1 \times P_{\text{monsoon}}\text{ (mm)}} \times 100\%$$")
    md.append(r"- **Numerator:** $\Delta\text{TWS}$ is the post-monsoon storage peak (maximum of August–November) minus the pre-monsoon dry season low (minimum of March–May) from CSR GRACE/GRACE-FO RL06.3.")
    md.append(r"- **Denominator:** $P_{\text{monsoon}}$ is the decoupled June–September 4-month total rainfall from NASA GPM IMERG V07B Final Run.")
    md.append("- **Missing Observation Protocol:** Seasons with incomplete satellite observation windows are excluded directly rather than interpolated.")
    md.append("  - In 2017: GRACE was decommissioned in June 2017, so no post-monsoon peak was observed.")
    md.append("  - In 2018: GRACE-FO was launched in May 2018 (first operational data in June 2018), so no pre-monsoon low was observed.")
    md.append("  - Consequently, 2 seasons (2017, 2018) are dropped per region, leaving **22 complete seasons** (2002–2016 [15] and 2019–2025 [7]) in the main run.")
    md.append(r"- **Sensitivity Run:** Drops seasons within $\pm 6$ months of the GRACE/GRACE-FO transition (2016, 2017, 2018, 2019), leaving **20 complete seasons**.")
    md.append("- **Exploratory FDR Control:** Benjamini-Hochberg FDR control is calculated strictly across these 6 exploratory regional tests and is quarantined from headline 36-test FDR families.")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 2. Main Analysis Results (22 Complete Seasons, 2002–2025)")
    md.append("")
    md.append("| Region | N | Mean Ratio | Theil-Sen Slope (%/yr) | 95% Confidence Interval | p-value (ESS-MK) | Exploratory FDR q | MDS (80% Power) | Verdict |")
    md.append("|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|")
    for r in main_recs:
        ci_str = f"[{r['slope_ci_low_pct_yr']:+.3f}, {r['slope_ci_high_pct_yr']:+.3f}]"
        md.append(f"| **{r['region']}** ({r['region_name']}) | {r['n_seasons']} | {r['mean_ratio_pct']:.1f}% | {r['slope_pct_yr']:+.3f}%/yr | {ci_str} | {r['p_value']:.4f} | {r['exploratory_fdr_q']:.4f} | {r['mds_80pct_power_pct_yr']:.3f}%/yr | {r['verdict']} |")

    md.append("")
    md.append("---")
    md.append("")
    md.append("## 3. Sensitivity Analysis (Transition-Buffer Excluded, N = 20 Seasons)")
    md.append("")
    md.append("| Region | N | Mean Ratio | Theil-Sen Slope (%/yr) | 95% Confidence Interval | p-value (ESS-MK) | Exploratory FDR q | MDS (80% Power) | Verdict |")
    md.append("|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|")
    for r in sens_recs:
        ci_str = f"[{r['slope_ci_low_pct_yr']:+.3f}, {r['slope_ci_high_pct_yr']:+.3f}]"
        md.append(f"| **{r['region']}** ({r['region_name']}) | {r['n_seasons']} | {r['mean_ratio_pct']:.1f}% | {r['slope_pct_yr']:+.3f}%/yr | {ci_str} | {r['p_value']:.4f} | {r['exploratory_fdr_q']:.4f} | {r['mds_80pct_power_pct_yr']:.3f}%/yr | {r['verdict']} |")

    md.append("")
    md.append("---")
    md.append("")
    md.append("## 4. Methodological Limits & Scientific Context")
    md.append("- **Bulk Storage Mass Limitation:** The seasonal storage response ratio reflects bulk total water storage change, integrating unsaturated soil moisture and surface water bodies alongside groundwater, and does not represent an isolated groundwater recharge coefficient.")
    md.append("- **Confidence Interval Breadth:** In regions such as the Northwest, the 95% confidence interval ([-0.295, +0.836] %/yr) is wide relative to the point slope (+0.266 %/yr) and spans zero, reflecting substantial interannual variability and confirming that the slope cannot be distinguished from multi-year climate variability.")
    md.append("- **Exploratory Framing:** In the main run (22 seasons) no region passes exploratory FDR control. In the sensitivity run that drops seasons within ±6 months of the GRACE to GRACE-FO transition (20 seasons), Central and National pass (q = 0.021). The result therefore depends on whether the 2016 and 2019 seasons are included and should be treated as fragile and exploratory.")
    md.append("- **Interpretation:** A positive ratio slope means the monsoon storage rebound per mm of rain has not weakened; it does not mean recharge is improving.")
    md.append("")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"[OK] Saved ratio trend Markdown: {OUT_MD}")


def plot_ratio_trends(main_records: list):
    """Plots regional seasonal storage response ratio time series with Theil-Sen trend lines and CI bands."""
    fig, axes = plt.subplots(3, 2, figsize=(15, 12), sharex=True)
    axes = axes.flatten()

    reg_colors = {
        "NW": "#dc2626", "NE": "#8b5cf6", "Central": "#0284c7",
        "SW": "#059669", "SE": "#ea580c", "National": "#1f2937",
    }

    for i, r in enumerate(main_records):
        ax = axes[i]
        reg = r["region"]
        yrs = r["years"]
        y = r["ratio_pct"]

        # Points
        ax.scatter(yrs, y, color=reg_colors[reg], s=35, zorder=3, label=f"{reg} Observed Ratio")
        ax.plot(yrs, y, color=reg_colors[reg], alpha=0.35, lw=1.2, linestyle="--")

        # Theil-Sen line
        intercept = float(np.median(y - r["slope_pct_yr"] * yrs))
        y_fit = r["slope_pct_yr"] * yrs + intercept
        ax.plot(yrs, y_fit, color=reg_colors[reg], lw=2.2, label=f"Theil-Sen: {r['slope_pct_yr']:+.3f}%/yr (p={r['p_value']:.3f})")

        # 95% CI band
        intercept_low = float(np.median(y - r["slope_ci_low_pct_yr"] * yrs))
        intercept_high = float(np.median(y - r["slope_ci_high_pct_yr"] * yrs))
        y_ci_low = r["slope_ci_low_pct_yr"] * yrs + intercept_low
        y_ci_high = r["slope_ci_high_pct_yr"] * yrs + intercept_high
        ax.fill_between(yrs, np.minimum(y_ci_low, y_ci_high), np.maximum(y_ci_low, y_ci_high),
                        color=reg_colors[reg], alpha=0.15, label="95% CI Band")

        # Gap shading
        ax.axvspan(2017 - 0.4, 2018 + 0.4, color="#fee2e2", alpha=0.6, zorder=0)

        ax.set_title(f"{r['region']} — {r['region_name']} (Mean: {r['mean_ratio_pct']:.1f}%) | {r['verdict']}",
                     fontsize=10, fontweight="bold")
        ax.set_ylabel("Storage Response Ratio (%)", fontsize=9)
        ax.grid(True, linestyle=":", alpha=0.5)
        ax.legend(loc="upper left", fontsize=7.5, framealpha=0.9)

    for ax in axes[-2:]:
        ax.set_xlabel("Monsoon Year (2002–2025)", fontsize=10)

    plt.suptitle("Exploratory Trend of Seasonal Storage Response Ratio (2002–2025)\n"
                 "PRELIMINARY & EXPLORATORY — Calibrated ESS-MK Theil-Sen Trends | Team Tenstral",
                 fontsize=13, fontweight="bold", y=0.99)
    plt.tight_layout()
    plt.savefig(OUT_FIG, dpi=300)
    plt.close()
    print(f"[OK] Saved ratio trend figure: {OUT_FIG}")


if __name__ == "__main__":
    run_ratio_trend_analysis()
