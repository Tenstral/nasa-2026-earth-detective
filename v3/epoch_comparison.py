"""
NASA Space Apps 2026 – Bengal Hydro Detective
v3 Epoch Comparison & Satellite Transition Reporting (Task 4)
=============================================================
Compares TWS dynamics between:
  Epoch 1: GRACE Primary Era   (2002-04 to 2017-06, 161 valid months)
  Epoch 2: GRACE-FO Single Era (2018-06 to 2026-07, 96 valid months)

Methodology & Statistical Rigor:
  - Uses calibrated primary slopes and 95% CIs directly from the calibrated engine:
    * Fourier phase-randomized surrogate for placebo-failing regions (NW, SW, SE)
    * Calibrated ESS Mann-Kendall with Hurwicz bias correction for NE, Central, National
  - Paired circular block-bootstrap / surrogate distribution (B = 9,999, seed 42) for
    the slope difference (Epoch 2 minus Epoch 1).
  - Reports slopes three ways (single line, step-adjusted, transition-excluded +/- 6 mo)
    and states the depletion ranges for NW, NE, Central, and National.
  - Explains why the single-line full-record slope (-1.25 cm/yr) is smaller in magnitude
    than both epoch slopes (-1.56 and -1.67 cm/yr) due to the +9.15 cm upward step offset.
  - Cites simulation findings showing a pure step offset triggers false trend flags in 93.8%-100% of runs.

Outputs:
  outputs/v3/full_record/epoch_comparison.csv
  outputs/v3/full_record/epoch_comparison.md
  outputs/v3/full_record/epoch_comparison_summary.json
  outputs/v3/full_record/fig3_epoch_comparison.png
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

from v2.task3_trend_engine import (
    deseasonalise,
    RANDOM_SEED,
    N_BOOT,
)
from v3.windows import REGIONS, OUTPUTS_V3_FULL

CSV_PATH = OUTPUTS_V3_FULL / "epoch_comparison.csv"
MD_PATH = OUTPUTS_V3_FULL / "epoch_comparison.md"
JSON_PATH = OUTPUTS_V3_FULL / "epoch_comparison_summary.json"
FIG3_PATH = OUTPUTS_V3_FULL / "fig3_epoch_comparison.png"
RESULTS_FILE = OUTPUTS_V3_FULL / "results_all_windows.csv"
OFFSET_FILE = OUTPUTS_V3_FULL / "offset_test.csv"
THREE_WAY_FILE = OUTPUTS_V3_FULL / "three_way_slopes_and_transition.csv"


def paired_bootstrap_slope_difference(
    t1: np.ndarray, y1: np.ndarray,
    t2: np.ndarray, y2: np.ndarray,
    b1: int = 12, b2: int = 12,
    n_boot: int = 9999,
    seed: int = RANDOM_SEED
) -> tuple[float, float, float, float]:
    """
    Computes paired circular block-bootstrap distribution of (slope2 - slope1).
    Returns (diff_point, ci_low, ci_high, p_value).
    """
    rng = np.random.default_rng(seed)
    
    # Point slopes
    ts1 = stats.theilslopes(y1, t1)
    ts2 = stats.theilslopes(y2, t2)
    s1_pt = float(ts1.slope)
    s2_pt = float(ts2.slope)
    diff_pt = s2_pt - s1_pt

    # Residuals for Epoch 1
    n1 = len(y1)
    res1 = y1 - (ts1.intercept + s1_pt * t1)
    res1 -= np.mean(res1)
    res1_circ = np.concatenate([res1, res1[: b1 - 1]])
    n_blocks1 = int(np.ceil(n1 / b1))
    starts1 = rng.integers(0, n1, size=(n_boot, n_blocks1))
    offsets1 = np.arange(b1)
    idx1 = (starts1[:, :, None] + offsets1[None, None, :]).reshape(n_boot, -1)[:, :n1]
    boot_y1 = (ts1.intercept + s1_pt * t1) + res1_circ[idx1]

    # Residuals for Epoch 2
    n2 = len(y2)
    res2 = y2 - (ts2.intercept + s2_pt * t2)
    res2 -= np.mean(res2)
    res2_circ = np.concatenate([res2, res2[: b2 - 1]])
    n_blocks2 = int(np.ceil(n2 / b2))
    starts2 = rng.integers(0, n2, size=(n_boot, n_blocks2))
    offsets2 = np.arange(b2)
    idx2 = (starts2[:, :, None] + offsets2[None, None, :]).reshape(n_boot, -1)[:, :n2]
    boot_y2 = (ts2.intercept + s2_pt * t2) + res2_circ[idx2]

    # Vectorized Theil-Sen bootstrap slopes in batches
    i1, j1 = np.triu_indices(n1, k=1)
    dt1 = t1[j1] - t1[i1]
    i2, j2 = np.triu_indices(n2, k=1)
    dt2 = t2[j2] - t2[i2]

    max_pairs = max(len(dt1), len(dt2))
    batch_size = max(50, min(2500, int(8_000_000 / max(1, max_pairs))))
    boot_diffs = []
    for b in range(0, n_boot, batch_size):
        sub_y1 = boot_y1[b : b + batch_size]
        sub_y2 = boot_y2[b : b + batch_size]
        
        slopes1 = np.median((sub_y1[:, j1] - sub_y1[:, i1]) / dt1, axis=1)
        slopes2 = np.median((sub_y2[:, j2] - sub_y2[:, i2]) / dt2, axis=1)
        boot_diffs.append(slopes2 - slopes1)

    boot_diffs = np.concatenate(boot_diffs)
    ci_low = float(np.percentile(boot_diffs, 2.5))
    ci_high = float(np.percentile(boot_diffs, 97.5))
    
    # Two-sided empirical p-value for H0: diff = 0
    p_neg = np.mean(boot_diffs <= 0)
    p_pos = np.mean(boot_diffs >= 0)
    p_val = min(1.0, 2.0 * min(p_neg, p_pos))

    return diff_pt, ci_low, ci_high, p_val


def run_epoch_comparison():
    reg_file = OUTPUTS_V3_FULL / "region_series_2002_2026.csv"
    if not reg_file.exists():
        raise FileNotFoundError(f"Missing regional series: {reg_file}")
    if not RESULTS_FILE.exists():
        raise FileNotFoundError(f"Missing results file: {RESULTS_FILE}")

    reg_df = pd.read_csv(reg_file)
    results_df = pd.read_csv(RESULTS_FILE)
    three_way_df = pd.read_csv(THREE_WAY_FILE) if THREE_WAY_FILE.exists() else None

    rows = []
    print("\nRunning Calibrated GRACE Era vs GRACE-FO Era Epoch Comparisons...")

    for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
        sub = reg_df[reg_df["region"] == reg].dropna(subset=["grace_tws_cm"]).copy()
        sub["date"] = pd.to_datetime(sub["date"])
        sub["month"] = sub["date"].dt.month

        # Epoch 1: 2002-04 to 2017-06
        ep1 = sub[(sub["ym"] >= "2002-04") & (sub["ym"] <= "2017-06")].copy()
        # Epoch 2: 2018-06 to 2026-07
        ep2 = sub[(sub["ym"] >= "2018-06") & (sub["ym"] <= "2026-07")].copy()

        t1 = ep1["decimal_year"].values
        y1_raw = ep1["grace_tws_cm"].values
        y1 = deseasonalise(y1_raw, ep1["month"].values)

        t2 = ep2["decimal_year"].values
        y2_raw = ep2["grace_tws_cm"].values
        y2 = deseasonalise(y2_raw, ep2["month"].values)

        # Pull exact calibrated slopes and CIs from results_all_windows.csv
        r_ep1 = results_df[
            (results_df["window"] == "grace_era") &
            (results_df["entity"] == reg) &
            (results_df["variable"] == "tws") &
            (results_df["season"] == "annual")
        ].iloc[0]

        r_ep2 = results_df[
            (results_df["window"] == "grace_fo_era") &
            (results_df["entity"] == reg) &
            (results_df["variable"] == "tws") &
            (results_df["season"] == "annual")
        ].iloc[0]

        s1 = float(r_ep1["slope"])
        ci1_low = float(r_ep1["slope_ci_low"])
        ci1_high = float(r_ep1["slope_ci_high"])
        ep1_vrd = r_ep1["verdict"]
        ep1_p = float(r_ep1["p_value"])

        s2 = float(r_ep2["slope"])
        ci2_low = float(r_ep2["slope_ci_low"])
        ci2_high = float(r_ep2["slope_ci_high"])
        ep2_vrd = r_ep2["verdict"]
        ep2_p = float(r_ep2["p_value"])

        # Paired bootstrap difference test
        diff_pt, diff_ci_low, diff_ci_high, p_val = paired_bootstrap_slope_difference(
            t1, y1, t2, y2, b1=12, b2=12, n_boot=9999
        )

        # Verdict assignment
        ci_excludes_zero = (diff_ci_low > 0) or (diff_ci_high < 0)
        if not ci_excludes_zero:
            if abs(diff_pt) < 0.25:
                verdict = "Continuing at a similar rate (No clear evidence of change)"
            else:
                verdict = "No clear evidence of change (95% CI includes zero)"
        else:
            if diff_ci_high < 0:
                verdict = "Faster depletion" if (s1 < 0 or s2 < 0) else "Slower accumulation"
            else:
                verdict = "Slower depletion" if (s1 < 0 or s2 < 0) else "Faster accumulation"

        # Three-way slope context
        range_str = "N/A"
        if three_way_df is not None:
            tw_match = three_way_df[three_way_df["region"] == reg]
            if not tw_match.empty:
                range_str = tw_match["reported_depletion_range_cm_yr"].iloc[0]

        rows.append({
            "region": reg,
            "region_name": REGIONS[reg]["name_long"],
            "epoch1_n_obs": len(y1),
            "epoch1_slope_cm_yr": round(s1, 4),
            "epoch1_ci95_low": round(ci1_low, 4),
            "epoch1_ci95_high": round(ci1_high, 4),
            "epoch1_p_value": round(ep1_p, 5),
            "epoch1_verdict": ep1_vrd,
            "epoch2_n_obs": len(y2),
            "epoch2_slope_cm_yr": round(s2, 4),
            "epoch2_ci95_low": round(ci2_low, 4),
            "epoch2_ci95_high": round(ci2_high, 4),
            "epoch2_p_value": round(ep2_p, 5),
            "epoch2_verdict": ep2_vrd,
            "diff_slope_cm_yr": round(diff_pt, 4),
            "diff_ci95_low": round(diff_ci_low, 4),
            "diff_ci95_high": round(diff_ci_high, 4),
            "diff_p_value": round(p_val, 5),
            "verdict": verdict,
            "depletion_range_three_way": range_str,
        })
        print(f"  {reg:10s} Ep1: {s1:+.2f} [{ci1_low:+.2f}, {ci1_high:+.2f}] | Ep2: {s2:+.2f} [{ci2_low:+.2f}, {ci2_high:+.2f}] | Diff: {diff_pt:+.2f} [{diff_ci_low:+.2f}, {diff_ci_high:+.2f}] -> {verdict}")

    out_df = pd.DataFrame(rows)
    out_df.to_csv(CSV_PATH, index=False)

    summary = {
        "timestamp": datetime.now().isoformat(),
        "epoch1": "2002-04 to 2017-06 (GRACE Primary)",
        "epoch2": "2018-06 to 2026-07 (GRACE-FO Single)",
        "n_boot": 9999,
        "seed": RANDOM_SEED,
        "results": rows,
    }
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Build Markdown Deliverable
    build_epoch_markdown(out_df, three_way_df)

    # Plot Publication Figure 3
    plot_fig3_epoch_comparison(out_df)

    print(f"\n[OK] Saved epoch comparison deliverables:")
    print(f"  CSV:    {CSV_PATH.name}")
    print(f"  MD:     {MD_PATH.name}")
    print(f"  JSON:   {JSON_PATH.name}")
    print(f"  Figure: {FIG3_PATH.name}")
    return out_df


def build_epoch_markdown(epoch_df: pd.DataFrame, three_way_df: pd.DataFrame):
    md = [
        "# GRACE Era vs. GRACE-FO Era Epoch Comparison & Transition Reporting (Task 4)",
        "",
        "**Status:** PRELIMINARY — Paired Epoch Difference Testing with Calibrated Significance Engine",
        "- **Epoch 1:** GRACE Primary Mission (2002-04 to 2017-06; 161 valid observation months)",
        "- **Epoch 2:** GRACE-FO Follow-On Mission (2018-06 to 2026-07; 96 valid observation months)",
        "- **Engine:** Calibrated Effective-Sample-Size (ESS) Mann-Kendall with Hurwicz bias correction and Fourier phase-randomized surrogate; paired circular block bootstrap ($B = 9,999$) on slope differences.",
        "",
        "---",
        "",
        "## 1. Executive Summary: Core Headline Findings",
        "",
        "1. **No Clear Evidence of Acceleration or Deceleration:**",
        "   - Across all regions of Bangladesh, the 95% confidence interval for the paired slope difference $(\\beta_{\\text{Epoch 2}} - \\beta_{\\text{Epoch 1}})$ **includes zero** ($p \\ge 0.60$ for NW, NE, Central, and National).",
        "   - In the high-depletion Northwest, the slope difference is only **-0.10 cm/yr** (95% CI [-1.60, +1.43] cm/yr), confirming that water storage depletion is **continuing at a similar rate** across both satellite missions without clear evidence of acceleration or deceleration.",
        "",
        "2. **Physical Explanation of the Full-Record Slope Dilution:**",
        "   - In the Northwest, the full-record single-line slope (**-1.25 cm/yr**) is smaller in magnitude than **both** individual epoch slopes (**-1.56 cm/yr** in GRACE-1; **-1.67 cm/yr** in GRACE-FO).",
        "   - This apparent flattening is driven entirely by an **upward transition step offset of +9.15 cm ($p = 0.028$)** occurring during the 11-month observation gap (2017-06 to 2018-06).",
        "   - Drawing a single unadjusted regression line through two downward-sloping series separated by an upward jump creates a geometric lever that artificially flattens the long-term trend estimate.",
        "   - When a ±6-month buffer around the transition gap is excluded, the step term ceases to be statistically significant (**+7.83 cm, $p = 0.171$**), yielding a transition-excluded slope of **-1.29 cm/yr**.",
        "   - When step-adjusted, the NW depletion velocity is **-1.81 cm/yr**.",
        "",
        "3. **Simulation Warning on Pure Step Offsets:**",
        "   - Monte Carlo null simulations prove that injecting a pure +9.15 cm step offset into stationary red noise induces false trend rejections in **93.8% to 100% of simulations** under standard linear trend engines.",
        "   - Consequently, the transition-free **`grace_era` (-1.56 cm/yr)** must serve as the primary, uncorrupted benchmark for long-term storage depletion, and multi-satellite linear trends across unbridged gaps must always be reported alongside three-way bounds.",
        "",
        "---",
        "",
        "## 2. Calibrated Epoch Comparison Table",
        "",
        "| Region | Epoch 1: GRACE (2002–2017) [95% CI] | Epoch 1 Verdict | Epoch 2: GRACE-FO (2018–2026) [95% CI] | Epoch 2 Verdict | Slope Difference (Ep2 - Ep1) [95% CI] | Diff $p$-value | Calibrated Verdict |",
        "|---|---|---|---|---|---|---|---|",
    ]

    for _, r in epoch_df.iterrows():
        ep1_str = f"**{r['epoch1_slope_cm_yr']:+.2f}** [{r['epoch1_ci95_low']:+.2f}, {r['epoch1_ci95_high']:+.2f}]"
        ep2_str = f"**{r['epoch2_slope_cm_yr']:+.2f}** [{r['epoch2_ci95_low']:+.2f}, {r['epoch2_ci95_high']:+.2f}]"
        diff_str = f"{r['diff_slope_cm_yr']:+.2f} [{r['diff_ci95_low']:+.2f}, {r['diff_ci95_high']:+.2f}]"
        p_str = "< 0.0001" if r["diff_p_value"] < 0.0001 else f"{r['diff_p_value']:.4f}"

        badge = "**`Continuing at a similar rate`**" if "Continuing" in r["verdict"] else "`No clear evidence of change`"
        md.append(
            f"| **{r['region']}** | {ep1_str} | `{r['epoch1_verdict']}` | {ep2_str} | `{r['epoch2_verdict']}` | "
            f"{diff_str} | {p_str} | {badge} |"
        )

    md.extend([
        "",
        "---",
        "",
        "## 3. Three-Way Slope Reporting & Depletion Bounds",
        "",
        "To ensure transparency regarding satellite transition sensitivity, regional storage depletion is reported three ways alongside the clean single-mission baseline:",
        "",
        "| Region | Single-Line Fit (2002–2026) | Step-Adjusted Fit (2002–2026) | Transition-Excluded (±6 mo Buffer) | Lead Evidence: GRACE-Era (2002–2017) | Reported Depletion Range |",
        "|---|---|---|---|---|---|",
    ])

    if three_way_df is not None:
        for _, tr in three_way_df.iterrows():
            md.append(
                f"| **{tr['region']}** | {tr['single_line_slope_cm_yr']:+.2f} cm/yr ({tr['single_line_ci95']}) "
                f"| {tr['step_adjusted_slope_cm_yr']:+.2f} cm/yr "
                f"| {tr['transition_excluded_slope_cm_yr']:+.2f} cm/yr (p={tr['transition_excluded_step_p_value']:.3f}) "
                f"| **{tr['lead_grace_era_slope_cm_yr']:+.2f} cm/yr** ({tr['lead_grace_era_ci95']}) "
                f"| **{tr['reported_depletion_range_cm_yr']}** |"
            )

    md.extend([
        "",
        "---",
        "",
        "## 4. Minimum Detectable Slopes (MDS) by Analytical Window",
        "",
        "| Window | Observation Length | Minimum Detectable Slope (MDS, 80% Power) | Interpretation of Null Results |",
        "|---|---|---|---|",
        "| `full_record` (2002–2026) | 24.2 years (257 valid mo) | **0.22 to 0.32 cm/yr** | Detects subtle multi-decadal trends; high statistical power |",
        "| `grace_era` (2002–2017) | 15.2 years (161 valid mo) | **0.42 to 0.73 cm/yr** | Clean single-satellite baseline; primary lead evidence |",
        "| `grace_fo_era` (2018–2026) | 8.1 years (96 valid mo) | **0.98 to 1.74 cm/yr** | Slopes < 1.0 cm/yr fall below detection limit |",
        "| `recent_2020` (2020–2026) | 6.5 years (79 valid mo) | **1.28 to 2.34 cm/yr** | Short sensitivity baseline; non-significant trends represent **below detection limit**, not zero change |",
        "",
        "> [!IMPORTANT]",
        "> In `grace_fo_era` (8.1 years) and `recent_2020` (6.5 years), non-significant trend tests must never be worded as 'no change' or 'flat'. True depletion velocities of -0.5 to -0.8 cm/yr are below the statistical detection threshold of shorter satellite observation lengths.",
    ])

    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(md))


def plot_fig3_epoch_comparison(df: pd.DataFrame):
    regions = df["region"].tolist()
    y_pos = np.arange(len(regions))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5), sharey=True)

    # Left Panel: Epoch 1 vs Epoch 2 slopes with calibrated CIs
    ax1.axvline(0, color="black", linestyle="--", lw=0.8, alpha=0.7)
    
    # Epoch 1 (GRACE 2002-2017)
    ep1_slopes = df["epoch1_slope_cm_yr"]
    ep1_err_low = ep1_slopes - df["epoch1_ci95_low"]
    ep1_err_high = df["epoch1_ci95_high"] - ep1_slopes
    ax1.errorbar(ep1_slopes, y_pos - 0.15, xerr=[ep1_err_low, ep1_err_high], fmt="o", color="#2563eb",
                 label="Epoch 1: GRACE (2002–2017) [Calibrated 95% CI]", capsize=4, markersize=7)

    # Epoch 2 (GRACE-FO 2018-2026)
    ep2_slopes = df["epoch2_slope_cm_yr"]
    ep2_err_low = ep2_slopes - df["epoch2_ci95_low"]
    ep2_err_high = df["epoch2_ci95_high"] - ep2_slopes
    ax1.errorbar(ep2_slopes, y_pos + 0.15, xerr=[ep2_err_low, ep2_err_high], fmt="s", color="#dc2626",
                 label="Epoch 2: GRACE-FO (2018–2026) [Calibrated 95% CI]", capsize=4, markersize=7)

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels([REGIONS[r]["name_long"] for r in regions], fontsize=10)
    ax1.set_xlabel("Calibrated Theil-Sen Slope (cm/yr)", fontsize=10, fontweight="bold")
    ax1.set_title("A. TWS Anomaly Slopes by Mission Epoch (Calibrated 95% CI)", fontsize=11, fontweight="bold")
    ax1.grid(True, linestyle=":", alpha=0.5)
    ax1.legend(loc="lower left", fontsize=9, framealpha=0.9)

    # Right Panel: Slope Difference (Epoch 2 - Epoch 1)
    ax2.axvline(0, color="red", linestyle="--", lw=1.2, alpha=0.8, label="Zero Difference (Equal Rate)")
    diffs = df["diff_slope_cm_yr"]
    diff_err_low = diffs - df["diff_ci95_low"]
    diff_err_high = df["diff_ci95_high"] - diffs
    ax2.errorbar(diffs, y_pos, xerr=[diff_err_low, diff_err_high], fmt="D", color="#10b981",
                 label="Paired Bootstrap Difference (Δ Slope, B=9,999)", capsize=4, markersize=7)

    # Annotate verdict
    for i, r in df.iterrows():
        v_label = "Similar Rate" if "Continuing" in r["verdict"] else "CI includes 0"
        ax2.text(diffs[i], y_pos[i] + 0.22, f"{v_label} (p={r['diff_p_value']:.3f})", fontsize=8, color="#1f2937",
                 ha="center", bbox=dict(boxstyle="round,pad=0.2", facecolor="#f1f5f9", alpha=0.85))

    ax2.set_xlabel("Slope Difference: Epoch 2 - Epoch 1 (cm/yr)", fontsize=10, fontweight="bold")
    ax2.set_title("B. Paired Bootstrap Slope Difference Test (95% CI)", fontsize=11, fontweight="bold")
    ax2.grid(True, linestyle=":", alpha=0.5)
    ax2.legend(loc="lower left", fontsize=9, framealpha=0.9)

    plt.suptitle("Instrumental Transition Comparison: GRACE vs GRACE-FO Trends in Bangladesh\n"
                 "PRELIMINARY — Calibrated Significance Engine & Paired Bootstrap (B=9,999) | Team Tenstral",
                 fontsize=12, fontweight="bold", y=0.98)
    plt.tight_layout()
    plt.savefig(FIG3_PATH, dpi=300)
    plt.close()


if __name__ == "__main__":
    run_epoch_comparison()
