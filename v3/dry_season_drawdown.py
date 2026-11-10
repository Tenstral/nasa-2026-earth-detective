"""
NASA Space Apps 2026 – Bengal Hydro Detective
v3 Exploratory Analysis: Dry-Season Drawdown Trends & Cropland Overlay
======================================================================
Evaluates the multi-decadal trend of dry-season storage drawdown
(monsoon-peak TWS minus following pre-monsoon minimum TWS) across Bangladesh
regions using Calibrated ESS-MK, with duality-aligned 95% CIs, MDS at 80% power,
within-family FDR correction, and a descriptive cropland exposure overlay.

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
EXPOSURE_CSV = REPO_ROOT / "outputs" / "v3" / "exposure" / "exposure_table.csv"
RESULTS_CSV = REPO_ROOT / "outputs" / "v3" / "full_record" / "results_all_windows.csv"
OUT_DIR = REPO_ROOT / "outputs" / "v3" / "seasonal"
OUT_CSV = OUT_DIR / "dry_season_drawdown.csv"
OUT_MD = OUT_DIR / "dry_season_drawdown.md"
OUT_FIG = OUT_DIR / "fig_dry_season_drawdown.png"


def load_config() -> dict:
    """Loads dry-season drawdown constants from config.json."""
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


def extract_annual_drawdowns(reg_df: pd.DataFrame, peak_months: list, low_months: list) -> pd.DataFrame:
    """
    Computes year-by-year dry-season drawdown:
    drawdown_cm = (peak TWS in peak_months of year y) - (minimum TWS in low_months of year y+1).
    Drops years where either endpoint is missing from the GRACE record.
    """
    df = reg_df.copy()
    df["year"] = df["ym"].str[:4].astype(int)
    df["month"] = df["ym"].str[5:7].astype(int)

    rows = []
    years = [y for y in sorted(df["year"].unique()) if y <= 2025]

    for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
        sub = df[df["region"] == reg]
        for y in years:
            peak_sub = sub[(sub["year"] == y) & (sub["month"].isin(peak_months)) & sub["grace_tws_cm"].notna()]
            low_sub = sub[(sub["year"] == y + 1) & (sub["month"].isin(low_months)) & sub["grace_tws_cm"].notna()]

            peak_val = float(peak_sub["grace_tws_cm"].max()) if not peak_sub.empty else np.nan
            low_val = float(low_sub["grace_tws_cm"].min()) if not low_sub.empty else np.nan

            if not np.isnan(peak_val) and not np.isnan(low_val):
                dd = peak_val - low_val
                valid = True
                note = "Complete peak-to-low observation pair"
            else:
                dd = np.nan
                valid = False
                note = "Missing observation endpoint (satellite mission gap)"

            rows.append({
                "region": reg,
                "region_name": REGIONS[reg]["name_long"],
                "hydrological_cycle_year": y,
                "cycle_label": f"{y}–{y+1}",
                "monsoon_peak_tws_cm": round(peak_val, 3) if not np.isnan(peak_val) else np.nan,
                "following_pre_monsoon_low_tws_cm": round(low_val, 3) if not np.isnan(low_val) else np.nan,
                "dry_season_drawdown_cm": round(dd, 3) if not np.isnan(dd) else np.nan,
                "valid": valid,
                "note": note,
            })

    return pd.DataFrame(rows)


def run_drawdown_analysis():
    """
    Executes exploratory dry-season drawdown analysis and cropland overlay.
    """
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cfg = load_config()
    dd_cfg = cfg.get("dry_season_drawdown", {})
    peak_months = dd_cfg.get("monsoon_peak_months", [8, 9, 10, 11])
    low_months = dd_cfg.get("following_pre_monsoon_min_months", [3, 4, 5])
    seed = cfg.get("random_seed", 42)

    if not REGION_SERIES_CSV.exists():
        raise FileNotFoundError(f"Missing regional series CSV: {REGION_SERIES_CSV}")

    reg_df = pd.read_csv(REGION_SERIES_CSV)
    series_df = extract_annual_drawdowns(reg_df, peak_months, low_months)

    # 1. Main Run: Complete cycles only (drops 2017 where peak is missing in mission gap)
    main_df = series_df[series_df["valid"] == True].copy()

    # 2. Sensitivity Run: Exclude cycles touching +/-6 months of transition gap (drops 2016, 2017, 2018)
    sens_drop_years = [2016, 2017, 2018]
    sens_df = series_df[(series_df["valid"] == True) & (~series_df["hydrological_cycle_year"].isin(sens_drop_years))].copy()

    # Read cropland % and population from exposure table
    exp_df = pd.read_csv(EXPOSURE_CSV).set_index("region")

    # Read full-record TWS slope from results_all_windows.csv
    res_df = pd.read_csv(RESULTS_CSV)
    full_tws = res_df[(res_df["window"] == "full_record") & (res_df["variable"] == "tws") & (res_df["season"] == "annual")].set_index("entity")

    regions = ["NW", "NE", "Central", "SW", "SE", "National"]
    results_records = []

    # Main Run
    main_raw = []
    for reg in regions:
        sub = main_df[main_df["region"] == reg].sort_values("hydrological_cycle_year")
        n_obs = len(sub)
        n_drop = 24 - n_obs
        yrs = sub["hydrological_cycle_year"].values.astype(float)
        dds = sub["dry_season_drawdown_cm"].values

        res = run_ess_mann_kendall(yrs, dds, alpha=0.05)
        mds, sd, phi = compute_mds_80pct(yrs, dds, seed=seed, n_sim=250, candidate_grid=np.linspace(0.05, 3.0, 60))

        ci_width = res["ci_high"] - res["ci_low"]
        slope_mag = abs(res["slope"])
        is_wide = ci_width > (2.0 * slope_mag) or (res["ci_low"] < 0 < res["ci_high"])

        crop_pct = float(exp_df.loc[reg, "cropland_pct_mcd12q1"]) if reg in exp_df.index else np.nan
        pop_m = float(exp_df.loc[reg, "pop_millions_2020"]) if reg in exp_df.index else np.nan
        secular_slope = float(full_tws.loc[reg, "slope"]) if reg in full_tws.index else np.nan
        secular_ci = f"[{full_tws.loc[reg, 'slope_ci_low']:.2f}, {full_tws.loc[reg, 'slope_ci_high']:+.2f}]" if reg in full_tws.index else ""

        main_raw.append({
            "region": reg,
            "region_name": REGIONS[reg]["name_long"],
            "analysis_type": "main_run",
            "n_years": n_obs,
            "n_dropped_years": n_drop,
            "dropped_years_list": "2017 (satellite mission gap: missing autumn peak and spring low)",
            "mean_drawdown_cm": round(float(np.mean(dds)), 2),
            "drawdown_slope_cm_yr": round(float(res["slope"]), 4),
            "drawdown_ci_low_cm_yr": round(float(res["ci_low"]), 4),
            "drawdown_ci_high_cm_yr": round(float(res["ci_high"]), 4),
            "p_value": round(float(res["p_value"]), 5),
            "mds_80pct_power_cm_yr": round(float(mds), 3) if mds is not None else np.nan,
            "ci_width_cm_yr": round(float(ci_width), 4),
            "ci_relative_to_slope": f"Wide (CI width {ci_width:.2f} cm/yr spans zero)" if (res["ci_low"] < 0 < res["ci_high"]) else f"CI width {ci_width:.2f} cm/yr",
            "cropland_pct_mcd12q1": crop_pct,
            "pop_millions_2020": pop_m,
            "secular_tws_slope_cm_yr": secular_slope,
            "secular_tws_ci_95": secular_ci,
            "years": yrs,
            "drawdown_cm": dds,
            "is_ci_wide": is_wide,
        })

    main_p_vals = [r["p_value"] for r in main_raw]
    main_q_vals = calc_bh_fdr(main_p_vals)

    for i, r in enumerate(main_raw):
        q = round(float(main_q_vals[i]), 5)
        r["exploratory_fdr_q"] = q
        ci_excludes_zero = (r["drawdown_ci_low_cm_yr"] > 0 or r["drawdown_ci_high_cm_yr"] < 0)
        if q < 0.05 and ci_excludes_zero:
            r["verdict"] = "Exploratory: trend detected"
            r["verdict_detail"] = f"Exploratory trend detected (p={r['p_value']:.4f}, q={q:.4f}); CI excludes zero"
        elif r["p_value"] < 0.05:
            r["verdict"] = "Suggestive"
            r["verdict_detail"] = f"Suggestive slope ({r['drawdown_slope_cm_yr']:+.3f} cm/yr, p={r['p_value']:.4f}), but fails exploratory FDR control (q={q:.4f} >= 0.05)"
        else:
            r["verdict"] = "No detectable trend"
            ci_note = "CI is wide relative to slope and spans zero" if r["is_ci_wide"] else "slope is below detection threshold"
            r["verdict_detail"] = f"No detectable trend (p={r['p_value']:.4f}, q={q:.4f}; {ci_note})"

        results_records.append(r)

    # Sensitivity Run
    sens_raw = []
    for reg in regions:
        sub = sens_df[sens_df["region"] == reg].sort_values("hydrological_cycle_year")
        n_obs = len(sub)
        n_drop = 24 - n_obs
        yrs = sub["hydrological_cycle_year"].values.astype(float)
        dds = sub["dry_season_drawdown_cm"].values

        res = run_ess_mann_kendall(yrs, dds, alpha=0.05)
        mds, sd, phi = compute_mds_80pct(yrs, dds, seed=seed, n_sim=250, candidate_grid=np.linspace(0.05, 3.0, 60))

        ci_width = res["ci_high"] - res["ci_low"]
        slope_mag = abs(res["slope"])
        is_wide = ci_width > (2.0 * slope_mag) or (res["ci_low"] < 0 < res["ci_high"])

        crop_pct = float(exp_df.loc[reg, "cropland_pct_mcd12q1"]) if reg in exp_df.index else np.nan
        pop_m = float(exp_df.loc[reg, "pop_millions_2020"]) if reg in exp_df.index else np.nan
        secular_slope = float(full_tws.loc[reg, "slope"]) if reg in full_tws.index else np.nan
        secular_ci = f"[{full_tws.loc[reg, 'slope_ci_low']:.2f}, {full_tws.loc[reg, 'slope_ci_high']:+.2f}]" if reg in full_tws.index else ""

        sens_raw.append({
            "region": reg,
            "region_name": REGIONS[reg]["name_long"],
            "analysis_type": "sensitivity_buffer_excluded",
            "n_years": n_obs,
            "n_dropped_years": n_drop,
            "dropped_years_list": "2016, 2017, 2018 (+/-6 mo transition buffer)",
            "mean_drawdown_cm": round(float(np.mean(dds)), 2),
            "drawdown_slope_cm_yr": round(float(res["slope"]), 4),
            "drawdown_ci_low_cm_yr": round(float(res["ci_low"]), 4),
            "drawdown_ci_high_cm_yr": round(float(res["ci_high"]), 4),
            "p_value": round(float(res["p_value"]), 5),
            "mds_80pct_power_cm_yr": round(float(mds), 3) if mds is not None else np.nan,
            "ci_width_cm_yr": round(float(ci_width), 4),
            "ci_relative_to_slope": f"Wide (CI width {ci_width:.2f} cm/yr spans zero)" if (res["ci_low"] < 0 < res["ci_high"]) else f"CI width {ci_width:.2f} cm/yr",
            "cropland_pct_mcd12q1": crop_pct,
            "pop_millions_2020": pop_m,
            "secular_tws_slope_cm_yr": secular_slope,
            "secular_tws_ci_95": secular_ci,
            "years": yrs,
            "drawdown_cm": dds,
            "is_ci_wide": is_wide,
        })

    sens_p_vals = [r["p_value"] for r in sens_raw]
    sens_q_vals = calc_bh_fdr(sens_p_vals)

    for i, r in enumerate(sens_raw):
        q = round(float(sens_q_vals[i]), 5)
        r["exploratory_fdr_q"] = q
        ci_excludes_zero = (r["drawdown_ci_low_cm_yr"] > 0 or r["drawdown_ci_high_cm_yr"] < 0)
        if q < 0.05 and ci_excludes_zero:
            r["verdict"] = "Exploratory: trend detected"
            r["verdict_detail"] = f"Exploratory trend detected (p={r['p_value']:.4f}, q={q:.4f}); CI excludes zero"
        elif r["p_value"] < 0.05:
            r["verdict"] = "Suggestive"
            r["verdict_detail"] = f"Suggestive slope ({r['drawdown_slope_cm_yr']:+.3f} cm/yr, p={r['p_value']:.4f}), but fails exploratory FDR control (q={q:.4f} >= 0.05)"
        else:
            r["verdict"] = "No detectable trend"
            ci_note = "CI is wide relative to slope and spans zero" if r["is_ci_wide"] else "slope is below detection threshold"
            r["verdict_detail"] = f"No detectable trend (p={r['p_value']:.4f}, q={q:.4f}; {ci_note})"

        results_records.append(r)

    # Convert to DataFrame
    df_out = pd.DataFrame(results_records).drop(columns=["years", "drawdown_cm", "is_ci_wide"])
    df_out.to_csv(OUT_CSV, index=False)
    print(f"[OK] Saved dry season drawdown CSV: {OUT_CSV}")

    # Generate Markdown Report
    generate_markdown_report(results_records, peak_months, low_months)

    # Generate Figure
    plot_drawdown_trends(main_raw)

    return df_out


def generate_markdown_report(records: list, peak_months: list, low_months: list):
    """Generates markdown report with descriptive cropland overlay and required limits text."""
    main_recs = [r for r in records if r["analysis_type"] == "main_run"]
    sens_recs = [r for r in records if r["analysis_type"] == "sensitivity_buffer_excluded"]

    month_names = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }
    peak_str = "/".join([month_names[m] for m in peak_months])
    low_str = "/".join([month_names[m] for m in low_months])

    md = []
    md.append("# Exploratory Dry-Season Drawdown Trends & Cropland Overlay (2002–2026)")
    md.append("")
    md.append("**Status:** PRELIMINARY & EXPLORATORY ONLY")
    md.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md.append("**Methodology:** Calibrated ESS-MK Theil-Sen regression with duality-aligned 95% CIs and descriptive overlay.")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 1. Metric Definition & Exact Observation Windows")
    md.append(f"- **Dry-Season Drawdown:** Defined as the total water storage difference between the annual monsoon peak and the subsequent pre-monsoon minimum:")
    md.append("  $$\\text{Drawdown}_{y} = \\text{TWS}_{\\text{peak}, y} - \\text{TWS}_{\\text{min}, y+1}$$")
    md.append(f"- **Config Constants (from `config.json`):**")
    md.append(f"  - Monsoon Peak Months (`monsoon_peak_months`): `{peak_months}` ({peak_str} of year $y$)")
    md.append(f"  - Following Pre-Monsoon Low Months (`following_pre_monsoon_min_months`): `{low_months}` ({low_str} of year $y+1$)")
    md.append("  - Transition Gap Years (`transition_gap_years`): `[2017, 2018]`")
    md.append("  - Transition Buffer (`transition_buffer_months`): `6` months")
    md.append("- **Missing Endpoint Protocol:** Any year missing either endpoint is dropped directly rather than interpolated.")
    md.append("  - Cycle 2017–2018 lacks the autumn 2017 peak and spring 2018 low due to the 11-month GRACE to GRACE-FO transition gap.")
    md.append("  - Consequently, exactly **1 year (2017)** drops out per region, leaving **23 valid observation cycles** (2002–2016 [15] and 2018–2025 [8]) in the main run.")
    md.append(r"- **Sensitivity Run:** Excludes cycles whose endpoints touch the $\pm 6$-month buffer around the gap (2016, 2017, 2018), leaving **21 valid cycles**.")
    md.append("- **Exploratory Multiple Testing:** Benjamini-Hochberg FDR correction is calculated within these 6 exploratory tests only.")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 2. Dry-Season Drawdown Trends (Main Run: N = 23 Cycles, 2002–2026)")
    md.append("")
    md.append("| Region | N | Mean Drawdown (cm) | Theil-Sen Slope (cm/yr) | 95% Confidence Interval | p-value (ESS-MK) | Exploratory FDR q | MDS (80% Power) | Verdict |")
    md.append("|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|")
    for r in main_recs:
        ci_str = f"[{r['drawdown_ci_low_cm_yr']:+.3f}, {r['drawdown_ci_high_cm_yr']:+.3f}]"
        md.append(f"| **{r['region']}** ({r['region_name']}) | {r['n_years']} | {r['mean_drawdown_cm']:.2f} cm | {r['drawdown_slope_cm_yr']:+.3f} cm/yr | {ci_str} | {r['p_value']:.4f} | {r['exploratory_fdr_q']:.4f} | {r['mds_80pct_power_cm_yr']:.3f} cm/yr | {r['verdict']} |")

    md.append("")
    md.append("---")
    md.append("")
    md.append("## 3. Sensitivity Analysis (Transition-Buffer Excluded: N = 21 Cycles)")
    md.append("")
    md.append("| Region | N | Mean Drawdown (cm) | Theil-Sen Slope (cm/yr) | 95% Confidence Interval | p-value (ESS-MK) | Exploratory FDR q | MDS (80% Power) | Verdict |")
    md.append("|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|")
    for r in sens_recs:
        ci_str = f"[{r['drawdown_ci_low_cm_yr']:+.3f}, {r['drawdown_ci_high_cm_yr']:+.3f}]"
        md.append(f"| **{r['region']}** ({r['region_name']}) | {r['n_years']} | {r['mean_drawdown_cm']:.2f} cm | {r['drawdown_slope_cm_yr']:+.3f} cm/yr | {ci_str} | {r['p_value']:.4f} | {r['exploratory_fdr_q']:.4f} | {r['mds_80pct_power_cm_yr']:.3f} cm/yr | {r['verdict']} |")

    md.append("")
    md.append("---")
    md.append("")
    md.append("## 4. Descriptive Cropland & Total Water Storage Overlay")
    md.append("")
    md.append("The table below overlays regional agricultural cropland fraction (MODIS MCD12Q1), human population (NASA SEDAC GPWv4), 24-year full-record secular total water storage slope (`results_all_windows.csv`), and annual dry-season drawdown trend. To prevent ecological fallacy and spurious inference from a sample of 5 spatial aggregations, no correlation or regression is computed across regions; data are presented strictly for descriptive comparison.")
    md.append("")
    md.append("| Region | Cropland Fraction (%) | Population (2020) | Full-Record TWS Slope (cm/yr) | Full-Record TWS 95% CI | Mean Drawdown (cm) | Drawdown Trend (cm/yr) | Drawdown Verdict |")
    md.append("|---|:---:|:---:|:---:|:---:|:---:|:---:|---|")
    for r in main_recs:
        md.append(f"| **{r['region']}** | {r['cropland_pct_mcd12q1']:.1f}% | {r['pop_millions_2020']:.2f}M | {r['secular_tws_slope_cm_yr']:+.2f} | {r['secular_tws_ci_95']} | {r['mean_drawdown_cm']:.2f} cm | {r['drawdown_slope_cm_yr']:+.3f} | {r['verdict']} |")

    md.append("")
    md.append("---")
    md.append("")
    md.append("## 5. Methodological Limits & Scope")
    md.append("")
    md.append("> Gravimetry measures total water storage (groundwater, soil moisture and surface water together). This analysis shows regional patterns that are consistent with dry-season agricultural water use but does not attribute them to irrigation pumping. Testing that would require metered pumping or electricity records (BMDA), BWDB well hydrographs, or irrigated-area mapping.")
    md.append("")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"[OK] Saved dry season drawdown Markdown: {OUT_MD}")


def plot_drawdown_trends(main_records: list):
    """Plots regional dry-season drawdown time series with trend lines and gap annotations."""
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
        y = r["drawdown_cm"]

        # Points
        ax.scatter(yrs, y, color=reg_colors[reg], s=35, zorder=3, label=f"{reg} Drawdown (Peak - Low)")
        ax.plot(yrs, y, color=reg_colors[reg], alpha=0.35, lw=1.2, linestyle="--")

        # Theil-Sen line
        intercept = float(np.median(y - r["drawdown_slope_cm_yr"] * yrs))
        y_fit = r["drawdown_slope_cm_yr"] * yrs + intercept
        ax.plot(yrs, y_fit, color=reg_colors[reg], lw=2.2, label=f"Theil-Sen: {r['drawdown_slope_cm_yr']:+.3f} cm/yr (p={r['p_value']:.3f})")

        # 95% CI band
        intercept_low = float(np.median(y - r["drawdown_ci_low_cm_yr"] * yrs))
        intercept_high = float(np.median(y - r["drawdown_ci_high_cm_yr"] * yrs))
        y_ci_low = r["drawdown_ci_low_cm_yr"] * yrs + intercept_low
        y_ci_high = r["drawdown_ci_high_cm_yr"] * yrs + intercept_high
        ax.fill_between(yrs, np.minimum(y_ci_low, y_ci_high), np.maximum(y_ci_low, y_ci_high),
                        color=reg_colors[reg], alpha=0.15, label="95% CI Band")

        # Gap shading
        ax.axvspan(2017 - 0.4, 2017 + 0.4, color="#fee2e2", alpha=0.6, zorder=0)

        ax.set_title(f"{r['region']} — {r['region_name']} (Mean Drawdown: {r['mean_drawdown_cm']:.1f} cm) | {r['verdict']}",
                     fontsize=10, fontweight="bold")
        ax.set_ylabel("Drawdown (cm)", fontsize=9)
        ax.grid(True, linestyle=":", alpha=0.5)
        ax.legend(loc="upper left", fontsize=7.5, framealpha=0.9)

    for ax in axes[-2:]:
        ax.set_xlabel("Hydrological Cycle Year (Monsoon Year y to Spring y+1)", fontsize=10)

    plt.suptitle("Exploratory Trend of Annual Dry-Season Storage Drawdown (2002–2026)\n"
                 "PRELIMINARY & EXPLORATORY — Calibrated ESS-MK Theil-Sen Trends | Team Tenstral",
                 fontsize=13, fontweight="bold", y=0.99)
    plt.tight_layout()
    plt.savefig(OUT_FIG, dpi=300)
    plt.close()
    print(f"[OK] Saved dry season drawdown figure: {OUT_FIG}")


if __name__ == "__main__":
    run_drawdown_analysis()
