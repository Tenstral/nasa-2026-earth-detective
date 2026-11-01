"""
NASA Space Apps 2026 – Bengal Hydro Detective
v3 Epoch Comparison: GRACE Era vs GRACE-FO Era Trend Comparison
================================================================
Compares TWS slopes between:
  Epoch 1: GRACE Primary Era   (2002-04 to 2017-06)
  Epoch 2: GRACE-FO Single Era (2018-06 to 2026-07)

Uses paired circular block bootstrap (B = 9,999, seed 42) to test
the slope difference (Epoch 2 minus Epoch 1).

Permitted Verdicts:
  - "No clear evidence of change" (95% CI includes zero)
  - "Continuing at a similar rate" (CI includes zero and magnitude difference < 0.25 cm/yr)
  - "Faster depletion" (CI strictly negative and baseline is negative)
  - "Slower depletion" (CI strictly positive and baseline is negative)

Outputs:
  outputs/v3/full_record/epoch_comparison.csv
  outputs/v3/full_record/epoch_comparison_summary.json
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

from v2.task3_trend_engine import (
    deseasonalise,
    choose_block_length,
    circular_block_bootstrap_slope,
    RANDOM_SEED,
    N_BOOT,
)
from v3.windows import REGIONS, OUTPUTS_V3_FULL

CSV_PATH = OUTPUTS_V3_FULL / "epoch_comparison.csv"
JSON_PATH = OUTPUTS_V3_FULL / "epoch_comparison_summary.json"


def paired_bootstrap_slope_difference(
    t1: np.ndarray, y1: np.ndarray,
    t2: np.ndarray, y2: np.ndarray,
    b1: int = 12, b2: int = 12,
    n_boot: int = N_BOOT,
    seed: int = RANDOM_SEED
) -> tuple[float, float, float, float]:
    """
    Computes paired circular block-bootstrap distribution of (slope2 - slope1).
    Returns (diff_point, ci_low, ci_high, p_value).
    """
    rng = np.random.default_rng(seed)
    
    # 1. Point slopes
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
        raise FileNotFoundError(f"Missing regional series: {reg_file}. Run series_extractor first.")

    reg_df = pd.read_csv(reg_file)
    rows = []

    print("\nRunning GRACE Era (2002–2017) vs GRACE-FO Era (2018–2026) Epoch Comparisons...")
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

        # Epoch 1 slope + CI
        s1 = float(stats.theilslopes(y1, t1).slope)
        ci1_low, ci1_high = circular_block_bootstrap_slope(t1, y1, block_len=12)

        # Epoch 2 slope + CI
        s2 = float(stats.theilslopes(y2, t2).slope)
        ci2_low, ci2_high = circular_block_bootstrap_slope(t2, y2, block_len=12)

        # Difference test
        diff_pt, diff_ci_low, diff_ci_high, p_val = paired_bootstrap_slope_difference(
            t1, y1, t2, y2, b1=12, b2=12
        )

        # Verdict assignment
        ci_excludes_zero = (diff_ci_low > 0) or (diff_ci_high < 0)
        if not ci_excludes_zero:
            if abs(diff_pt) < 0.25:
                verdict = "Continuing at a similar rate"
            else:
                verdict = "No clear evidence of change (95% CI includes zero)"
        else:
            if diff_ci_high < 0:
                verdict = "Faster depletion" if (s1 < 0 or s2 < 0) else "Slower accumulation"
            else:
                verdict = "Slower depletion" if (s1 < 0 or s2 < 0) else "Faster accumulation"

        rows.append({
            "region": reg,
            "region_name": REGIONS[reg]["name_long"],
            "epoch1_n_obs": len(y1),
            "epoch1_slope_cm_yr": round(s1, 4),
            "epoch1_ci95_low": round(ci1_low, 4),
            "epoch1_ci95_high": round(ci1_high, 4),
            "epoch2_n_obs": len(y2),
            "epoch2_slope_cm_yr": round(s2, 4),
            "epoch2_ci95_low": round(ci2_low, 4),
            "epoch2_ci95_high": round(ci2_high, 4),
            "diff_slope_cm_yr": round(diff_pt, 4),
            "diff_ci95_low": round(diff_ci_low, 4),
            "diff_ci95_high": round(diff_ci_high, 4),
            "diff_p_value": round(p_val, 5),
            "verdict": verdict,
        })
        print(f"  {reg:10s} Ep1: {s1:+.2f} cm/yr | Ep2: {s2:+.2f} cm/yr | Diff: {diff_pt:+.2f} [{diff_ci_low:+.2f}, {diff_ci_high:+.2f}] -> {verdict}")

    out_df = pd.DataFrame(rows)
    out_df.to_csv(CSV_PATH, index=False)

    summary = {
        "timestamp": datetime.now().isoformat(),
        "epoch1": "2002-04 to 2017-06 (GRACE Primary)",
        "epoch2": "2018-06 to 2026-07 (GRACE-FO Single)",
        "n_boot": N_BOOT,
        "seed": RANDOM_SEED,
        "results": rows,
    }
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"\n[OK] Saved epoch comparison deliverables:")
    print(f"  CSV:  {CSV_PATH.name}")
    print(f"  JSON: {JSON_PATH.name}")
    return out_df


if __name__ == "__main__":
    run_epoch_comparison()
