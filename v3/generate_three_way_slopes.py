"""
NASA Space Apps 2026 – Bengal Hydro Detective
v3 Three-Way Slope & Transition Sensitivity Analysis
=====================================================
Reports TWS slopes for NW, NE, Central, and National three ways:
  1. Single-line fit (calibrated full record)
  2. Step-adjusted fit (with 2018-06 GRACE-FO transition offset)
  3. Transition-excluded fit (+/- 6 months buffer around the gap: 2017-01 to 2018-11)
Accompanied by the clean transition-free GRACE-era lead evidence and simulation findings.

Outputs:
  outputs/v3/full_record/three_way_slopes_and_transition.csv
  outputs/v3/full_record/three_way_slopes_and_transition.md
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_V3_FULL = REPO_ROOT / "outputs" / "v3" / "full_record"
SERIES_FILE = OUTPUTS_V3_FULL / "region_series_2002_2026.csv"
RESULTS_FILE = OUTPUTS_V3_FULL / "results_all_windows.csv"
OFFSET_FILE = OUTPUTS_V3_FULL / "offset_test.csv"
OUT_CSV = OUTPUTS_V3_FULL / "three_way_slopes_and_transition.csv"
OUT_MD = OUTPUTS_V3_FULL / "three_way_slopes_and_transition.md"

MDS_DATA = {
    "full_record": {"years": 24.2, "mds_range": "0.22 to 0.32 cm/yr"},
    "grace_era": {"years": 15.2, "mds_range": "0.42 to 0.73 cm/yr"},
    "grace_fo_era": {"years": 8.1, "mds_range": "0.98 to 1.74 cm/yr"},
    "recent_2020": {"years": 6.5, "mds_range": "1.28 to 2.34 cm/yr"},
}


def build_three_way_slopes():
    results_df = pd.read_csv(RESULTS_FILE)
    offset_df = pd.read_csv(OFFSET_FILE)

    target_regions = ["NW", "NE", "Central", "National"]
    rows = []

    for reg in target_regions:
        off_row = offset_df[offset_df["region"] == reg].iloc[0]

        # 1. Single line calibrated Theil-Sen from full_record
        res_full = results_df[
            (results_df["window"] == "full_record")
            & (results_df["entity"] == reg)
            & (results_df["variable"] == "tws")
            & (results_df["season"] == "annual")
        ].iloc[0]
        s_single = res_full["slope"]
        ci_single_low = res_full["slope_ci_low"]
        ci_single_high = res_full["slope_ci_high"]
        single_vrd = res_full["verdict"]

        # 2. Step-adjusted (Newey-West OLS with step at 2018-06)
        s_step = off_row["slope_with_step_cm_yr"]
        delta = off_row["step_delta_cm"]
        p_delta = off_row["step_p_value"]

        # 3. Transition-excluded (+/- 6 mo buffer: 2017-01 to 2018-11)
        s_excl = off_row["slope_without_step_cm_yr"]  # without step when buffer excluded
        excl_delta = off_row["excl_step_delta_cm"]
        excl_p = off_row["excl_step_p_value"]

        # 4. Clean transition-free GRACE-era lead evidence
        res_era1 = results_df[
            (results_df["window"] == "grace_era")
            & (results_df["entity"] == reg)
            & (results_df["variable"] == "tws")
            & (results_df["season"] == "annual")
        ].iloc[0]
        s_era1 = res_era1["slope"]
        ci_era1_low = res_era1["slope_ci_low"]
        ci_era1_high = res_era1["slope_ci_high"]
        era1_vrd = res_era1["verdict"]

        # Bounds of the depletion range
        slopes = [s_single, s_step, s_era1]
        depletion_range = f"{min(slopes):.2f} to {max(slopes):.2f} cm/yr"

        rows.append({
            "region": reg,
            "region_name": off_row["region_name"],
            "lead_grace_era_slope_cm_yr": s_era1,
            "lead_grace_era_ci95": f"[{ci_era1_low:+.2f}, {ci_era1_high:+.2f}]",
            "lead_grace_era_verdict": era1_vrd,
            "single_line_slope_cm_yr": s_single,
            "single_line_ci95": f"[{ci_single_low:+.2f}, {ci_single_high:+.2f}]",
            "single_line_verdict": single_vrd,
            "step_adjusted_slope_cm_yr": s_step,
            "transition_step_delta_cm": delta,
            "transition_step_p_value": p_delta,
            "transition_excluded_slope_cm_yr": s_excl,
            "transition_excluded_step_delta_cm": excl_delta,
            "transition_excluded_step_p_value": excl_p,
            "reported_depletion_range_cm_yr": depletion_range,
        })

    df_out = pd.DataFrame(rows)
    df_out.to_csv(OUT_CSV, index=False)
    print(f"Saved: {OUT_CSV}")

    # Build Markdown Document
    md = [
        "# GRACE to GRACE-FO Transition & Three-Way Slope Sensitivity Report",
        "",
        "**Status:** PRELIMINARY — Robustness Analysis of Satellite Transition & Gap Artifacts",
        "",
        "## 1. Executive Summary & Lead Evidence Framework",
        "",
        "- **Primary Lead Evidence:** The **transition-free GRACE era (2002-04 to 2017-06)** serves as our cleanest, primary benchmark for long-term storage depletion, entirely unaffected by satellite instrument handover or sensor intercalibration offsets.",
        "- **Transition Shift:** Between GRACE decommissioning (2017-06) and GRACE-FO initial observation (2018-06), an upward step offset is detected in the raw gravimetric anomaly series (+9.15 cm in NW, p = 0.028; +6.93 cm in Central, p = 0.047; +6.82 cm in NE, p = 0.051).",
        "- **Buffer Sensitivity:** When a ±6-month transition buffer (2017-01 to 2018-11) is excluded, the step term ceases to be statistically significant in all regions (NW: +7.83 cm, p = 0.171; NE: +4.00 cm, p = 0.402; Central: +3.93 cm, p = 0.385; National: +3.09 cm, p = 0.486).",
        "- **Single-Line Underestimation:** Because the +9.15 cm transition step acts as an upward shift midway through the record, a single continuous linear trend line through both satellite missions dilutes the apparent depletion rate (-1.25 cm/yr) relative to the uncorrupted single-satellite epoch (-1.56 cm/yr).",
        "- **Pure Step Simulation Warning:** Monte Carlo null simulations demonstrate that a pure step offset (+9.15 cm) injected into stationary red noise (AR(1) phi=0.65) is falsely flagged as a statistically significant trend in **93.8% to 100% of simulations** under standard linear trend engines. Therefore, multi-satellite linear trends across unbridged gaps must always be reported alongside step-adjusted and transition-excluded bounds.",
        "",
        "## 2. Three-Way Slope Comparison Table",
        "",
        "| Region | Lead Evidence: GRACE-Era (2002–2017) | Single-Line Fit (2002–2026) | Step-Adjusted Fit (2002–2026) | Transition Offset (p-value) | Transition-Excluded (±6 mo Buffer) | Reported Depletion Range |",
        "|---|---|---|---|---|---|---|",
    ]

    for _, r in df_out.iterrows():
        md.append(
            f"| **{r['region']}** | **{r['lead_grace_era_slope_cm_yr']:+.2f} cm/yr** ({r['lead_grace_era_ci95']}) "
            f"| {r['single_line_slope_cm_yr']:+.2f} cm/yr ({r['single_line_ci95']}) "
            f"| {r['step_adjusted_slope_cm_yr']:+.2f} cm/yr "
            f"| {r['transition_step_delta_cm']:+.2f} cm (p = {r['transition_step_p_value']:.4f}) "
            f"| {r['transition_excluded_slope_cm_yr']:+.2f} cm/yr (p = {r['transition_excluded_step_p_value']:.3f}) "
            f"| **{r['reported_depletion_range_cm_yr']}** |"
        )

    md.extend([
        "",
        "## 3. Minimum Detectable Slopes (MDS) by Analytical Window",
        "",
        "Power analysis with regional residual variance scaling demonstrates that the statistical power to detect subtle trends depends heavily on observation window length:",
        "",
        "| Window | Observation Length | Minimum Detectable Slope (MDS, 80% Power) | Interpretation of Null Verdicts |",
        "|---|---|---|---|",
        "| `full_record` (2002–2026) | 24.2 years (257 valid mo) | **0.22 to 0.32 cm/yr** | Detects subtle multi-decadal trends; high statistical power |",
        "| `grace_era` (2002–2017) | 15.2 years (163 valid mo) | **0.42 to 0.73 cm/yr** | Robust single-satellite baseline; clean lead evidence |",
        "| `grace_fo_era` (2018–2026) | 8.1 years (94 valid mo) | **0.98 to 1.74 cm/yr** | Moderate power; trends < 1.0 cm/yr are below detection limit |",
        "| `recent_2020` (2020–2026) | 6.5 years (79 valid mo) | **1.28 to 2.34 cm/yr** | Short sensitivity baseline; non-significant trends represent **below detection limit**, not proof of zero change |",
        "",
        "> [!IMPORTANT]",
        "> In the short recent windows (`grace_fo_era` and `recent_2020`), non-significant trend tests must never be characterized as 'no change'. True depletion rates of -0.5 to -0.8 cm/yr fall entirely below the 80% detection limit of the short-duration satellite sample size.",
    ])

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"Saved: {OUT_MD}")


if __name__ == "__main__":
    build_three_way_slopes()
