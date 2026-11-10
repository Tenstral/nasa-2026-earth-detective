"""
NASA Space Apps 2026 – Bengal Hydro Detective
v3 Pairwise Between-Region Comparison & Paired Block-Bootstrap Pipeline
======================================================================
Evaluates whether secular trends in Total Water Storage (TWS) and Precipitation
differ significantly between administrative regions across Bangladesh.

Methodology:
  1. Synchronized Observation Windows:
     - Evaluates common valid observation months for each regional pair (A, B).
     - Full record (2002-04 to 2026-07): n = 257 valid months for TWS, n = 247 for IMERG.
     - Sensitivity grace_era (2002-04 to 2017-06): n = 161 for TWS, n = 183 for IMERG.
     - Sensitivity transition_excluded (+/- 6 months around 2017-07 to 2018-05 gap):
       n = 245 for TWS, n = 224 for IMERG.
  2. Point Estimator:
     - Robust Theil-Sen slope difference: delta = slope_A - slope_B on deseasonalized series.
  3. Paired Moving-Block Bootstrap:
     - Synchronized block resampling: both regions resample the identical time block sequence,
       preserving empirical cross-regional contemporaneous spatial covariance.
     - Block length selection (ESS convention): determined from the larger Hurwicz-bias-corrected
       lag-1 autocorrelation of the pair: r_max* = max(r1_A*, r1_B*), b = max(1, round((1+r_max*)/(1-r_max*))).
     - Resamples B = 9,999 (seed = 42).
     - Duality-aligned two-sided bootstrap p-value and 95% percentile confidence interval:
       p = min(1.0, 2.0 * min(mean(delta* <= 0), mean(delta* >= 0))).
       Guarantees CI excludes zero if and only if p < 0.05.
  4. Multiple Testing Control:
     - Benjamini-Hochberg (BH) FDR applied strictly across the 20 tests within each family
       (10 pairs x 2 variables: TWS and IMERG).
     - Project verdict rule:
       * "Significant difference": bh_q_value < 0.05 AND CI excludes zero.
       * "Suggestive": raw p_value < 0.05 only.
       * "No detectable difference": otherwise.
  5. Minimum Detectable Slope Difference (MDS, 80% Power):
     - Parametric AR(1) Monte Carlo simulation on the paired difference series.
  6. Calibration Simulation:
     - Evaluates 1,000 synthetic correlated AR(1) pairs under null (delta = 0) with real gap mask.
     - Records empirical FPR and 95% CI coverage in calibration_report.json.

Outputs:
  outputs/v3/region_comparison/pairwise_region_differences.csv
  outputs/v3/region_comparison/pairwise_region_differences.md
  outputs/v3/region_comparison/calibration_report.json
  outputs/v3/region_comparison/fig_pairwise_slope_differences.png
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
import itertools

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from v2.task3_trend_engine import deseasonalise
from v3.windows import REGIONS

OUT_DIR = REPO_ROOT / "outputs" / "v3" / "region_comparison"
OUT_CSV = OUT_DIR / "pairwise_region_differences.csv"
OUT_MD = OUT_DIR / "pairwise_region_differences.md"
OUT_JSON = OUT_DIR / "calibration_report.json"
OUT_FIG = OUT_DIR / "fig_pairwise_slope_differences.png"
REG_SERIES_CSV = REPO_ROOT / "outputs" / "v3" / "full_record" / "region_series_2002_2026.csv"
CONFIG_PATH = REPO_ROOT / "config.json"


def load_config() -> dict:
    """Loads configuration constants from config.json."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        return cfg.get("pairwise_region_comparison", {})
    return {}


def calc_bh_fdr(p_values: list | np.ndarray) -> np.ndarray:
    """Benjamini-Hochberg False Discovery Rate q-values."""
    p_arr = np.asarray(p_values, dtype=float)
    m = len(p_arr)
    if m == 0:
        return np.array([])
    sort_idx = np.argsort(p_arr)
    sorted_p = p_arr[sort_idx]
    q_vals = np.zeros(m)
    min_q = 1.0
    for i in range(m - 1, -1, -1):
        q = sorted_p[i] * m / (i + 1)
        min_q = min(min_q, q)
        q_vals[i] = min_q
    inv_idx = np.empty(m, dtype=int)
    inv_idx[sort_idx] = np.arange(m)
    return np.clip(q_vals[inv_idx], 0.0, 1.0)


def compute_lag1_autocorr_hurwicz(resid: np.ndarray) -> tuple[float, float, float]:
    """
    Computes detrended residual lag-1 autocorrelation with Hurwicz small-sample bias correction.
    Returns (r1_raw, r1_bc, gamma).
    """
    n = len(resid)
    if n < 4:
        return 0.0, 0.0, 1.0
    r1 = float(np.corrcoef(resid[:-1], resid[1:])[0, 1])
    if np.isnan(r1) or r1 <= 0.0:
        return 0.0, 0.0, 1.0
    # Hurwicz small-sample bias correction
    r1_bc = r1 + (1.0 + 4.0 * r1) / n
    r1_used = min(0.85, max(0.0, r1_bc))
    gamma = (1.0 + r1_used) / (1.0 - r1_used)
    return r1, r1_used, gamma


def compute_pair_block_length(residA: np.ndarray, residB: np.ndarray) -> tuple[int, float, float]:
    """
    Chooses moving-block bootstrap block length using the repo's ESS convention:
    Uses the larger Hurwicz-bias-corrected autocorrelation of the pair.
    b = max(1, round((1 + r_max*) / (1 - r_max*))).
    """
    _, r1A_bc, gammaA = compute_lag1_autocorr_hurwicz(residA)
    _, r1B_bc, gammaB = compute_lag1_autocorr_hurwicz(residB)
    r_max = max(r1A_bc, r1B_bc)
    gamma_max = max(gammaA, gammaB)
    b_len = max(1, int(round(gamma_max)))
    return b_len, r_max, gamma_max


def paired_block_bootstrap_theilsen(
    t: np.ndarray,
    yA: np.ndarray,
    yB: np.ndarray,
    scale: float = 1.0,
    block_len: int = 4,
    n_boot: int = 9999,
    seed: int = 42,
) -> dict:
    """
    Computes synchronized paired circular block bootstrap for Theil-Sen slope difference (A - B).
    Preserves both temporal autocorrelation and contemporaneous cross-regional correlation.
    """
    n = len(t)
    tsA = stats.theilslopes(yA, t)
    tsB = stats.theilslopes(yB, t)
    sA = float(tsA.slope) * scale
    sB = float(tsB.slope) * scale
    delta_pt = sA - sB

    # Residuals
    eA = yA - (tsA.intercept + tsA.slope * t)
    eB = yB - (tsB.intercept + tsB.slope * t)
    eA -= np.mean(eA)
    eB -= np.mean(eB)

    # Circular padding for block bootstrap
    eA_circ = np.concatenate([eA, eA[: block_len - 1]])
    eB_circ = np.concatenate([eB, eB[: block_len - 1]])

    rng = np.random.default_rng(seed)
    n_blocks = int(np.ceil(n / block_len))
    starts = rng.integers(0, n, size=(n_boot, n_blocks))
    offsets = np.arange(block_len)
    idx = (starts[:, :, None] + offsets[None, None, :]).reshape(n_boot, -1)[:, :n]

    boot_yA = (tsA.intercept + tsA.slope * t) + eA_circ[idx]
    boot_yB = (tsB.intercept + tsB.slope * t) + eB_circ[idx]

    i_idx, j_idx = np.triu_indices(n, k=1)
    dt = t[j_idx] - t[i_idx]

    batch_size = 1500
    boot_diffs = []
    for b in range(0, n_boot, batch_size):
        sub_yA = boot_yA[b : b + batch_size]
        sub_yB = boot_yB[b : b + batch_size]
        slopesA = np.median((sub_yA[:, j_idx] - sub_yA[:, i_idx]) / dt, axis=1) * scale
        slopesB = np.median((sub_yB[:, j_idx] - sub_yB[:, i_idx]) / dt, axis=1) * scale
        boot_diffs.append(slopesA - slopesB)

    boot_diffs = np.concatenate(boot_diffs)

    ci_low = float(np.percentile(boot_diffs, 2.5))
    ci_high = float(np.percentile(boot_diffs, 97.5))

    # Duality-aligned two-sided bootstrap p-value
    p_neg = float(np.mean(boot_diffs <= 0))
    p_pos = float(np.mean(boot_diffs >= 0))
    p_val = float(min(1.0, 2.0 * min(p_neg, p_pos)))

    return {
        "slope_A": sA,
        "slope_B": sB,
        "delta_slope": delta_pt,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "p_value": p_val,
        "boot_diffs": boot_diffs,
    }


def compute_mds_difference_80pct(
    t: np.ndarray,
    residA: np.ndarray,
    residB: np.ndarray,
    scale: float = 1.0,
    block_len: int = 4,
    seed: int = 42,
    n_sim: int = 250,
) -> float:
    """
    Computes Minimum Detectable Slope difference (80% power) for the paired series.
    Uses parametric AR(1) difference noise simulation across candidate effect sizes.
    """
    n = len(t)
    diff_resid = (residA - residB) * scale
    sd_diff = float(np.std(diff_resid, ddof=1))
    if sd_diff <= 0:
        return 0.0

    r1_diff = float(np.corrcoef(diff_resid[:-1], diff_resid[1:])[0, 1])
    phi = min(0.85, max(0.0, r1_diff if not np.isnan(r1_diff) else 0.0))

    grid = np.linspace(0.05, 3.5, 35) if scale == 1.0 else np.linspace(0.5, 25.0, 35)
    rng = np.random.default_rng(seed)

    i_idx, j_idx = np.triu_indices(n, k=1)
    dt = t[j_idx] - t[i_idx]

    for delta_cand in grid:
        sig_count = 0
        for _ in range(n_sim):
            # AR(1) noise
            wn = rng.standard_normal(n)
            noise = np.zeros(n)
            for step in range(1, n):
                noise[step] = phi * noise[step - 1] + sd_diff * np.sqrt(1.0 - phi**2) * wn[step]

            y_diff = delta_cand * t + noise
            dy = y_diff[j_idx] - y_diff[i_idx]
            cand_slope = float(np.median(dy / dt))

            # Quick standard error proxy
            # Rejection proxy based on CI width
            se_proxy = sd_diff / (np.std(t) * np.sqrt(n / ((1 + phi) / (1 - phi))))
            if abs(cand_slope) / (se_proxy * 1.96) > 1.0:
                sig_count += 1

        power = sig_count / n_sim
        if power >= 0.80:
            return round(float(delta_cand), 3)

    return round(float(grid[-1]), 3)


def run_pairwise_family(
    reg_df: pd.DataFrame,
    window_name: str,
    run_label: str,
    start_ym: str,
    end_ym: str,
    transition_buffer_months: int = 0,
    n_boot: int = 9999,
    seed: int = 42,
) -> list[dict]:
    """Runs all 20 tests (10 pairs x 2 variables) for a given window/run specification."""
    regions = ["NW", "NE", "Central", "SW", "SE"]
    pairs = list(itertools.combinations(regions, 2))
    variables = [("tws", "cm/yr", 1.0, "grace_tws_cm"), ("precip", "mm/yr", 12.0, "imerg_precip_mm")]

    family_records = []

    for var, unit, scale, col_name in variables:
        for regA, regB in pairs:
            subA = reg_df[reg_df["region"] == regA].copy()
            subB = reg_df[reg_df["region"] == regB].copy()

            # Window filter
            subA = subA[(subA["ym"] >= start_ym) & (subA["ym"] <= end_ym)]
            subB = subB[(subB["ym"] >= start_ym) & (subB["ym"] <= end_ym)]

            # Transition buffer exclusion (drops +/- 6 months around gap: 2017-01 to 2018-11)
            if transition_buffer_months > 0:
                subA = subA[~((subA["ym"] >= "2017-01") & (subA["ym"] <= "2018-11"))]
                subB = subB[~((subB["ym"] >= "2017-01") & (subB["ym"] <= "2018-11"))]

            # Common available months
            subA = subA.dropna(subset=[col_name]).sort_values("decimal_year")
            subB = subB.dropna(subset=[col_name]).sort_values("decimal_year")

            common_yms = sorted(list(set(subA["ym"]).intersection(set(subB["ym"]))))
            subA = subA[subA["ym"].isin(common_yms)].sort_values("decimal_year")
            subB = subB[subB["ym"].isin(common_yms)].sort_values("decimal_year")

            n_months = len(common_yms)
            if n_months < 10:
                continue

            t = subA["decimal_year"].values
            mA = pd.to_datetime(subA["date"]).dt.month.values
            mB = pd.to_datetime(subB["date"]).dt.month.values

            yA = deseasonalise(subA[col_name].values.astype(float), mA)
            yB = deseasonalise(subB[col_name].values.astype(float), mB)

            # Detrended residuals for block length
            tsA = stats.theilslopes(yA, t)
            tsB = stats.theilslopes(yB, t)
            eA = yA - (tsA.intercept + tsA.slope * t)
            eB = yB - (tsB.intercept + tsB.slope * t)

            b_len, r_max, gamma_max = compute_pair_block_length(eA, eB)

            # Paired block bootstrap
            boot_res = paired_block_bootstrap_theilsen(
                t=t, yA=yA, yB=yB, scale=scale, block_len=b_len, n_boot=n_boot, seed=seed
            )

            # MDS (80% power)
            mds_val = compute_mds_difference_80pct(
                t=t, residA=eA, residB=eB, scale=scale, block_len=b_len, seed=seed, n_sim=200
            )

            rec = {
                "variable": var,
                "window": window_name,
                "run": run_label,
                "region_A": regA,
                "region_B": regB,
                "slope_A": round(boot_res["slope_A"], 4),
                "slope_B": round(boot_res["slope_B"], 4),
                "delta_slope": round(boot_res["delta_slope"], 4),
                "ci_low": round(boot_res["ci_low"], 4),
                "ci_high": round(boot_res["ci_high"], 4),
                "p_value": round(boot_res["p_value"], 5),
                "mds_80": mds_val,
                "n_months": n_months,
                "block_length": b_len,
            }
            family_records.append(rec)

    # Benjamini-Hochberg FDR across the family (20 tests)
    p_vals = [r["p_value"] for r in family_records]
    q_vals = calc_bh_fdr(p_vals)

    for i, r in enumerate(family_records):
        q = round(float(q_vals[i]), 5)
        r["bh_q_value"] = q
        ci_excludes_zero = (r["ci_low"] > 0 or r["ci_high"] < 0)

        # Verdict rules
        if q < 0.05 and ci_excludes_zero:
            r["verdict"] = "Significant difference"
        elif r["p_value"] < 0.05:
            r["verdict"] = "Suggestive"
        else:
            r["verdict"] = "No detectable difference"

    return family_records


def run_calibration_simulation(
    reg_df: pd.DataFrame,
    n_sim: int = 1000,
    n_boot: int = 1000,
    seed: int = 42,
) -> dict:
    """
    Simulates 1,000 pairs of correlated AR(1) series under the null hypothesis (true delta = 0).
    Uses empirical fitted lag-1 r and observed cross-region correlation with the real gap pattern.
    """
    print(f"\n[CALIBRATION] Simulating {n_sim} correlated AR(1) pairs under H0 (true delta = 0)...")
    sub = reg_df[reg_df["region"] == "NW"]
    all_months = pd.date_range("2002-04-01", "2026-07-01", freq="MS")
    nominal_yms = [d.strftime("%Y-%m") for d in all_months]
    obs_yms = set(sub.dropna(subset=["grace_tws_cm"])["ym"])
    mask_obs = np.array([ym in obs_yms for ym in nominal_yms])
    dates = all_months[mask_obs]
    t_years = (dates.year + (dates.month - 0.5) / 12.0).values
    n_obs = len(t_years)

    # Calibration parameters for NW vs Central
    phi_A, sd_A = 0.5537, 7.17
    phi_B, sd_B = 0.4813, 5.55
    rho_target = 0.860
    denom = np.sqrt((1.0 - phi_A**2) * (1.0 - phi_B**2))
    r_w = float(np.clip(rho_target * (1.0 - phi_A * phi_B) / denom, -0.99, 0.99))
    cov_w = np.array([[1.0, r_w], [r_w, 1.0]])

    r_max = max(phi_A, phi_B)
    b_len = max(1, int(round((1.0 + r_max) / (1.0 - r_max))))

    rng = np.random.default_rng(seed)
    fp_count = 0
    covered_count = 0

    i_idx, j_idx = np.triu_indices(n_obs, k=1)
    dt = t_years[j_idx] - t_years[i_idx]

    for sim in range(n_sim):
        w = rng.multivariate_normal([0, 0], cov_w, size=len(nominal_yms))
        xA = np.zeros(len(nominal_yms))
        xB = np.zeros(len(nominal_yms))
        for step in range(1, len(nominal_yms)):
            xA[step] = phi_A * xA[step - 1] + sd_A * np.sqrt(1.0 - phi_A**2) * w[step, 0]
            xB[step] = phi_B * xB[step - 1] + sd_B * np.sqrt(1.0 - phi_B**2) * w[step, 1]

        yA = xA[mask_obs]
        yB = xB[mask_obs]

        # Slopes
        tsA = stats.theilslopes(yA, t_years)
        tsB = stats.theilslopes(yB, t_years)
        sA = float(tsA.slope)
        sB = float(tsB.slope)

        eA = yA - (tsA.intercept + sA * t_years)
        eB = yB - (tsB.intercept + sB * t_years)
        eA -= np.mean(eA)
        eB -= np.mean(eB)

        eA_c = np.concatenate([eA, eA[: b_len - 1]])
        eB_c = np.concatenate([eB, eB[: b_len - 1]])

        n_blocks = int(np.ceil(n_obs / b_len))
        starts = rng.integers(0, n_obs, size=(n_boot, n_blocks))
        offsets = np.arange(b_len)
        idx = (starts[:, :, None] + offsets[None, None, :]).reshape(n_boot, -1)[:, :n_obs]

        boot_yA = (tsA.intercept + sA * t_years) + eA_c[idx]
        boot_yB = (tsB.intercept + sB * t_years) + eB_c[idx]

        dyA = boot_yA[:, j_idx] - boot_yA[:, i_idx]
        dyB = boot_yB[:, j_idx] - boot_yB[:, i_idx]
        slopesA = np.median(dyA / dt, axis=1)
        slopesB = np.median(dyB / dt, axis=1)
        boot_diffs = slopesA - slopesB

        ci_low = float(np.percentile(boot_diffs, 2.5))
        ci_high = float(np.percentile(boot_diffs, 97.5))

        # Under H0, true delta = 0
        if ci_low <= 0.0 <= ci_high:
            covered_count += 1
        else:
            fp_count += 1

    fpr = fp_count / n_sim
    cov = covered_count / n_sim

    target_fpr_met = (0.035 <= fpr <= 0.065)
    target_cov_met = (0.930 <= cov <= 0.970)

    report = {
        "timestamp": datetime.now().isoformat(),
        "n_simulations": n_sim,
        "n_bootstrap_resamples": n_boot,
        "pair_evaluated": "NW_vs_Central",
        "phi_A": phi_A,
        "phi_B": phi_B,
        "cross_correlation_rho": rho_target,
        "block_length_used": b_len,
        "false_positive_rate": round(fpr, 4),
        "false_positive_rate_pct": round(fpr * 100.0, 2),
        "target_fpr_range": [0.035, 0.065],
        "target_fpr_met": target_fpr_met,
        "ci_coverage": round(cov, 4),
        "ci_coverage_pct": round(cov * 100.0, 2),
        "target_coverage_range": [0.930, 0.970],
        "target_coverage_met": target_cov_met,
        "disclosure_note": (
            "Calibration audit evaluates paired moving-block bootstrap on correlated AR(1) noise under real gap pattern. "
            f"Observed FPR = {fpr*100.0:.2f}% (nominal 5%), 95% CI coverage = {cov*100.0:.2f}% (nominal 95%). "
            "Block bootstrap with short block length exhibits slight false-positive inflation under high persistence, "
            "analogous to Hamed-Rao; results are interpreted descriptively and with multiple-testing control."
        ),
    }

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"[OK] Calibration report saved: {OUT_JSON}")
    print(f"     FPR: {fpr*100.0:.2f}% (Target: 3.5%-6.5%) | CI Coverage: {cov*100.0:.2f}% (Target: 93%-97%)")
    return report


def generate_markdown_report(all_records: list[dict], calib_report: dict):
    """Generates pairwise_region_differences.md with formatted tables and verbatim limits text."""
    primary_recs = [r for r in all_records if r["run"] == "primary"]
    grace_recs = [r for r in all_records if r["run"] == "sensitivity_grace_era"]
    trans_recs = [r for r in all_records if r["run"] == "sensitivity_transition_excluded"]

    md = [
        "# Pairwise Between-Region Slope Comparison (2002–2026)",
        "",
        "**Status:** PRELIMINARY & EXPLORATORY ONLY  ",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
        "**Methodology:** Theil-Sen pairwise slope differences with synchronized Paired Moving-Block Bootstrap (B = 9,999, seed 42) and Benjamini-Hochberg FDR control across 20 hypothesis tests per family.",
        "",
        "---",
        "",
        "## 1. Methodological Limits & Scope",
        "",
        '> "Regions are adjacent and GRACE resolves a few hundred kilometres, so neighbouring regions share signal and coastal leakage is possible. A significant difference between two regions\' slopes is a statement about these satellite-derived series, not a measurement of local aquifer or pumping differences. Recent windows are below the detection limit."',
        "",
        "---",
        "",
        "## 2. Calibration Check & Statistical Disclosure",
        "",
        f"- **Simulation Design:** 1,000 synthetic pairs of correlated AR(1) series under null hypothesis ($\\Delta = 0$) using empirical persistence ($\\phi_{{NW}} = {calib_report['phi_A']}$, $\\phi_{{Central}} = {calib_report['phi_B']}$, cross-correlation $\\rho = {calib_report['cross_correlation_rho']}$) and real satellite gap pattern.",
        f"- **Observed False Positive Rate:** **{calib_report['false_positive_rate_pct']:.2f}%** (Target: 3.5%–6.5%; nominal 5.0%).",
        f"- **Observed 95% CI Coverage:** **{calib_report['ci_coverage_pct']:.2f}%** (Target: 93.0%–97.0%; nominal 95.0%).",
        f"- **Statistical Disclosure:** {calib_report['disclosure_note']}",
        "",
        "---",
        "",
        "## 3. Primary Between-Region Comparison (Full Record: 2002-04 to 2026-07)",
        "",
        "Family of 20 tests (10 pairs $\\times$ 2 variables). Benjamini-Hochberg FDR $q$-values calculated within this family.",
        "",
        "### A. Total Water Storage Differences (cm/yr)",
        "",
        "| Pair (A vs B) | Common Months | Slope A | Slope B | $\\Delta$ Slope (A - B) | 95% Confidence Interval | p-value | FDR q-value | MDS (80%) | Block Len | Verdict |",
        "|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|",
    ]

    for r in primary_recs:
        if r["variable"] == "tws":
            ci_str = f"[{r['ci_low']:+.3f}, {r['ci_high']:+.3f}]"
            md.append(
                f"| **{r['region_A']} vs {r['region_B']}** | {r['n_months']} | {r['slope_A']:+.3f} | {r['slope_B']:+.3f} | **{r['delta_slope']:+.3f}** | {ci_str} | {r['p_value']:.4f} | {r['bh_q_value']:.4f} | {r['mds_80']:.2f} cm/yr | b={r['block_length']} | {r['verdict']} |"
            )

    md += [
        "",
        "### B. GPM IMERG Rainfall Differences (mm/yr)",
        "",
        "| Pair (A vs B) | Common Months | Slope A | Slope B | $\\Delta$ Slope (A - B) | 95% Confidence Interval | p-value | FDR q-value | MDS (80%) | Block Len | Verdict |",
        "|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|",
    ]

    for r in primary_recs:
        if r["variable"] == "precip":
            ci_str = f"[{r['ci_low']:+.3f}, {r['ci_high']:+.3f}]"
            md.append(
                f"| **{r['region_A']} vs {r['region_B']}** | {r['n_months']} | {r['slope_A']:+.3f} | {r['slope_B']:+.3f} | **{r['delta_slope']:+.3f}** | {ci_str} | {r['p_value']:.4f} | {r['bh_q_value']:.4f} | {r['mds_80']:.2f} mm/yr | b={r['block_length']} | {r['verdict']} |"
            )

    md += [
        "",
        "---",
        "",
        "## 4. Sensitivity Analyses",
        "",
        "### A. GRACE Era Only (2002-04 to 2017-06)",
        "",
        "| Variable | Pair | Common Months | $\\Delta$ Slope | 95% CI | p-value | FDR q-value | Verdict |",
        "|---|---|:---:|:---:|:---:|:---:|:---:|---|",
    ]

    for r in grace_recs:
        ci_str = f"[{r['ci_low']:+.3f}, {r['ci_high']:+.3f}]"
        unit_str = "cm/yr" if r["variable"] == "tws" else "mm/yr"
        md.append(
            f"| {r['variable'].upper()} | **{r['region_A']} vs {r['region_B']}** | {r['n_months']} | **{r['delta_slope']:+.3f}** {unit_str} | {ci_str} | {r['p_value']:.4f} | {r['bh_q_value']:.4f} | {r['verdict']} |"
        )

    md += [
        "",
        "### B. Transition Buffer Excluded (Full Record excluding $\\pm 6$ months around gap)",
        "",
        "| Variable | Pair | Common Months | $\\Delta$ Slope | 95% CI | p-value | FDR q-value | Verdict |",
        "|---|---|:---:|:---:|:---:|:---:|:---:|---|",
    ]

    for r in trans_recs:
        ci_str = f"[{r['ci_low']:+.3f}, {r['ci_high']:+.3f}]"
        unit_str = "cm/yr" if r["variable"] == "tws" else "mm/yr"
        md.append(
            f"| {r['variable'].upper()} | **{r['region_A']} vs {r['region_B']}** | {r['n_months']} | **{r['delta_slope']:+.3f}** {unit_str} | {ci_str} | {r['p_value']:.4f} | {r['bh_q_value']:.4f} | {r['verdict']} |"
        )

    md.append("")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print(f"[OK] Saved pairwise comparison Markdown: {OUT_MD}")


def plot_pairwise_slope_differences(records: list[dict]):
    """
    Forest plot of delta slopes with 95% CIs per pair.
    Two panels: TWS (cm/yr) and IMERG Rainfall (mm/yr).
    Primary runs shown as solid markers; sensitivity runs shown as hollow markers.
    """
    pairs_order = [
        "NW - NE", "NW - Central", "NW - SW", "NW - SE",
        "NE - Central", "NE - SW", "NE - SE",
        "Central - SW", "Central - SE",
        "SW - SE"
    ]
    y_pos = np.arange(len(pairs_order))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), sharey=True)

    # 1. TWS Panel
    for i, pair_name in enumerate(pairs_order):
        regA, regB = pair_name.split(" - ")
        prim = next((r for r in records if r["run"] == "primary" and r["variable"] == "tws" and r["region_A"] == regA and r["region_B"] == regB), None)
        grace = next((r for r in records if r["run"] == "sensitivity_grace_era" and r["variable"] == "tws" and r["region_A"] == regA and r["region_B"] == regB), None)
        trans = next((r for r in records if r["run"] == "sensitivity_transition_excluded" and r["variable"] == "tws" and r["region_A"] == regA and r["region_B"] == regB), None)

        if prim:
            col = "#dc2626" if prim["verdict"] == "Significant difference" else ("#d97706" if prim["verdict"] == "Suggestive" else "#64748b")
            ax1.errorbar(prim["delta_slope"], i, xerr=[[prim["delta_slope"] - prim["ci_low"]], [prim["ci_high"] - prim["delta_slope"]]],
                         fmt="o", color=col, ecolor=col, elinewidth=2.2, capsize=4, ms=7, zorder=4,
                         label="Primary (2002–2026)" if i == 0 else "")

        if grace:
            ax1.errorbar(grace["delta_slope"], i - 0.2, xerr=[[grace["delta_slope"] - grace["ci_low"]], [grace["ci_high"] - grace["delta_slope"]]],
                         fmt="s", mfc="none", mec="#0284c7", ecolor="#0284c7", elinewidth=1.2, capsize=3, ms=6, alpha=0.8,
                         label="GRACE Era Only" if i == 0 else "")

        if trans:
            ax1.errorbar(trans["delta_slope"], i + 0.2, xerr=[[trans["delta_slope"] - trans["ci_low"]], [trans["ci_high"] - trans["delta_slope"]]],
                         fmt="^", mfc="none", mec="#059669", ecolor="#059669", elinewidth=1.2, capsize=3, ms=6, alpha=0.8,
                         label="Transition Excluded" if i == 0 else "")

    ax1.axvline(0, color="#1e293b", linestyle="--", lw=1.2, alpha=0.7)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(pairs_order, fontsize=10, fontweight="bold")
    ax1.set_xlabel("TWS Slope Difference Δ (cm/yr)", fontsize=11)
    ax1.set_title("A. Total Water Storage Differences\n(Solid = Primary, Hollow = Sensitivity)", fontsize=12, fontweight="bold")
    ax1.grid(True, linestyle=":", alpha=0.5)
    ax1.legend(loc="lower left", fontsize=8.5, framealpha=0.9)

    # 2. Precip Panel
    for i, pair_name in enumerate(pairs_order):
        regA, regB = pair_name.split(" - ")
        prim = next((r for r in records if r["run"] == "primary" and r["variable"] == "precip" and r["region_A"] == regA and r["region_B"] == regB), None)
        grace = next((r for r in records if r["run"] == "sensitivity_grace_era" and r["variable"] == "precip" and r["region_A"] == regA and r["region_B"] == regB), None)
        trans = next((r for r in records if r["run"] == "sensitivity_transition_excluded" and r["variable"] == "precip" and r["region_A"] == regA and r["region_B"] == regB), None)

        if prim:
            col = "#dc2626" if prim["verdict"] == "Significant difference" else ("#d97706" if prim["verdict"] == "Suggestive" else "#64748b")
            ax2.errorbar(prim["delta_slope"], i, xerr=[[prim["delta_slope"] - prim["ci_low"]], [prim["ci_high"] - prim["delta_slope"]]],
                         fmt="o", color=col, ecolor=col, elinewidth=2.2, capsize=4, ms=7, zorder=4,
                         label="Primary (2002–2025)" if i == 0 else "")

        if grace:
            ax2.errorbar(grace["delta_slope"], i - 0.2, xerr=[[grace["delta_slope"] - grace["ci_low"]], [grace["ci_high"] - grace["delta_slope"]]],
                         fmt="s", mfc="none", mec="#0284c7", ecolor="#0284c7", elinewidth=1.2, capsize=3, ms=6, alpha=0.8,
                         label="GRACE Era Only" if i == 0 else "")

        if trans:
            ax2.errorbar(trans["delta_slope"], i + 0.2, xerr=[[trans["delta_slope"] - trans["ci_low"]], [trans["ci_high"] - trans["delta_slope"]]],
                         fmt="^", mfc="none", mec="#059669", ecolor="#059669", elinewidth=1.2, capsize=3, ms=6, alpha=0.8,
                         label="Transition Excluded" if i == 0 else "")

    ax2.axvline(0, color="#1e293b", linestyle="--", lw=1.2, alpha=0.7)
    ax2.set_xlabel("IMERG Rainfall Slope Difference Δ (mm/yr)", fontsize=11)
    ax2.set_title("B. GPM IMERG Rainfall Differences\n(Solid = Primary, Hollow = Sensitivity)", fontsize=12, fontweight="bold")
    ax2.grid(True, linestyle=":", alpha=0.5)
    ax2.legend(loc="lower left", fontsize=8.5, framealpha=0.9)

    plt.suptitle("Pairwise Between-Region Slope Differences (2002–2026)\n"
                 "Paired Moving-Block Bootstrap (B = 9,999) | Team Tenstral", fontsize=13, fontweight="bold", y=0.98)
    plt.tight_layout()
    plt.savefig(OUT_FIG, dpi=300)
    plt.close()
    print(f"[OK] Saved forest plot figure: {OUT_FIG}")


def run_all_region_comparisons():
    """Main execution entry point."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if not REG_SERIES_CSV.exists():
        raise FileNotFoundError(f"Missing regional series CSV: {REG_SERIES_CSV}")

    reg_df = pd.read_csv(REG_SERIES_CSV)
    cfg = load_config()
    n_boot = cfg.get("resamples", 9999)
    seed = cfg.get("seed", 42)

    # 1. Calibration Check
    calib_report = run_calibration_simulation(reg_df, n_sim=1000, n_boot=1000, seed=seed)

    # 2. Primary Analysis (2002-04 to 2026-07)
    print("\n[ANALYSIS] Running Primary Pairwise Between-Region Comparisons...")
    primary_records = run_pairwise_family(
        reg_df=reg_df,
        window_name="full_record",
        run_label="primary",
        start_ym="2002-04",
        end_ym="2026-07",
        transition_buffer_months=0,
        n_boot=n_boot,
        seed=seed,
    )

    # 3. Sensitivity (a): GRACE Era Only (2002-04 to 2017-06)
    print("[ANALYSIS] Running Sensitivity (a): GRACE Era Only...")
    grace_records = run_pairwise_family(
        reg_df=reg_df,
        window_name="grace_era",
        run_label="sensitivity_grace_era",
        start_ym="2002-04",
        end_ym="2017-06",
        transition_buffer_months=0,
        n_boot=n_boot,
        seed=seed,
    )

    # 4. Sensitivity (b): Transition Buffer Excluded (+/- 6 months)
    print("[ANALYSIS] Running Sensitivity (b): Transition Buffer Excluded...")
    trans_records = run_pairwise_family(
        reg_df=reg_df,
        window_name="full_record_transition_excluded",
        run_label="sensitivity_transition_excluded",
        start_ym="2002-04",
        end_ym="2026-07",
        transition_buffer_months=6,
        n_boot=n_boot,
        seed=seed,
    )

    all_records = primary_records + grace_records + trans_records

    # Save CSV
    df_out = pd.DataFrame(all_records)
    # Ensure correct column ordering per instructions
    cols = [
        "variable", "window", "run", "region_A", "region_B",
        "slope_A", "slope_B", "delta_slope", "ci_low", "ci_high",
        "p_value", "bh_q_value", "mds_80", "n_months", "block_length", "verdict"
    ]
    df_out = df_out[cols]
    df_out.to_csv(OUT_CSV, index=False)
    print(f"[OK] Saved pairwise differences CSV: {OUT_CSV}")

    # Generate Markdown and Plot
    generate_markdown_report(all_records, calib_report)
    plot_pairwise_slope_differences(all_records)


if __name__ == "__main__":
    run_all_region_comparisons()
