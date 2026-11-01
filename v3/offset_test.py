"""
NASA Space Apps 2026 – Bengal Hydro Detective
v3 Offset Test: GRACE to GRACE-FO Instrument Transition Step Test
==================================================================
Tests for an instrumental calibration offset/step at the 2018-06 boundary
between the original GRACE mission (ended June 2017) and GRACE-FO (started June 2018).

Model:
    y_t = beta_0 + beta_1 * t + delta * 1_{t >= 2018.5} + eps_t

Specifications:
  - Fits model across all 5 approved regions + National composite.
  - Computes robust standard errors (HAC / HC3 sandwich estimator).
  - Also performs sensitivity exclusion run: excluding +/- 6 months around
    the transition gap (2017-01 to 2018-11).
  - Reports slopes with and without the step term.
  - Verdict: "Significant Step Offset" (p < 0.05) vs "No Detectable Offset" (p >= 0.05).

Outputs:
  outputs/v3/full_record/offset_test.csv
  outputs/v3/full_record/offset_test_summary.json
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

from v3.windows import REGIONS, OUTPUTS_V3_FULL

CSV_PATH = OUTPUTS_V3_FULL / "offset_test.csv"
JSON_PATH = OUTPUTS_V3_FULL / "offset_test_summary.json"


def newey_west_ols(X: np.ndarray, y: np.ndarray, max_lags: int = 12):
    """
    Ordinary Least Squares with Newey-West (1987) HAC robust standard errors.
    Uses Bartlett kernel with lag truncation = max_lags.
    """
    n, k = X.shape
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ (X.T @ y)
    e = y - X @ beta

    xe = X * e[:, None]
    S = xe.T @ xe
    for l in range(1, max_lags + 1):
        w = 1.0 - l / (max_lags + 1.0)
        gamma_l = xe[l:].T @ xe[:-l]
        S += w * (gamma_l + gamma_l.T)

    V = XtX_inv @ S @ XtX_inv
    se = np.sqrt(np.maximum(0.0, np.diag(V)))
    t_stat = np.where(se > 1e-12, beta / se, 0.0)
    p_vals = 2.0 * (1.0 - stats.norm.cdf(np.abs(t_stat)))
    ci_low = beta - 1.95996 * se
    ci_high = beta + 1.95996 * se
    return beta, se, p_vals, ci_low, ci_high


def fit_step_model(sub_df: pd.DataFrame, exclude_buffer_months: bool = False) -> dict:
    df = sub_df.dropna(subset=["grace_tws_cm", "decimal_year"]).copy()
    
    if exclude_buffer_months:
        # Exclude 2017-01 to 2018-11 (+/- 6 months around the gap)
        df = df[(df["ym"] < "2017-01") | (df["ym"] > "2018-11")]

    t = df["decimal_year"].values
    y = df["grace_tws_cm"].values
    n = len(y)
    
    # Step indicator: 1 for GRACE-FO (from 2018-06 onward)
    step = (df["ym"] >= "2018-06").astype(float).values

    # 1. Model WITHOUT step term: y = b0 + b1*t
    X_base = np.column_stack([np.ones(n), t])
    b_base, se_base, p_base, ci_l_base, ci_h_base = newey_west_ols(X_base, y, max_lags=12)
    slope_no_step = float(b_base[1])
    se_no_step = float(se_base[1])
    ci_no_step = [float(ci_l_base[1]), float(ci_h_base[1])]

    # 2. Model WITH step term: y = b0 + b1*t + delta * step
    X_step = np.column_stack([np.ones(n), t, step])
    b_step, se_step, p_step, ci_l_step, ci_h_step = newey_west_ols(X_step, y, max_lags=12)
    
    slope_with_step = float(b_step[1])
    se_with_step = float(se_step[1])
    ci_with_step = [float(ci_l_step[1]), float(ci_h_step[1])]
    
    delta = float(b_step[2])
    delta_se = float(se_step[2])
    delta_p = float(p_step[2])
    delta_ci = [float(ci_l_step[2]), float(ci_h_step[2])]

    return {
        "n_obs": n,
        "slope_without_step_cm_yr": round(slope_no_step, 4),
        "slope_without_step_se": round(se_no_step, 4),
        "slope_without_step_ci95": [round(ci_no_step[0], 4), round(ci_no_step[1], 4)],
        "slope_with_step_cm_yr": round(slope_with_step, 4),
        "slope_with_step_se": round(se_with_step, 4),
        "slope_with_step_ci95": [round(ci_with_step[0], 4), round(ci_with_step[1], 4)],
        "step_delta_cm": round(delta, 4),
        "step_delta_se": round(delta_se, 4),
        "step_delta_p_value": round(delta_p, 5),
        "step_delta_ci95": [round(delta_ci[0], 4), round(delta_ci[1], 4)],
        "step_significant": bool(delta_p < 0.05),
    }


def run_offset_tests():
    reg_file = OUTPUTS_V3_FULL / "region_series_2002_2026.csv"
    if not reg_file.exists():
        raise FileNotFoundError(f"Missing regional series: {reg_file}. Run series_extractor first.")

    reg_df = pd.read_csv(reg_file)
    rows = []

    print("Running GRACE to GRACE-FO Step Offset Tests (2018-06 transition)...")
    for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
        sub = reg_df[reg_df["region"] == reg].copy()
        
        # Standard run across all valid months
        std_res = fit_step_model(sub, exclude_buffer_months=False)
        
        # Robustness run: excluding +/- 6 months around gap
        excl_res = fit_step_model(sub, exclude_buffer_months=True)

        verdict = (
            "Significant Step Offset" if std_res["step_significant"]
            else "No Detectable Offset (p >= 0.05)"
        )

        rows.append({
            "region": reg,
            "region_name": REGIONS[reg]["name_long"],
            "n_obs": std_res["n_obs"],
            "slope_without_step_cm_yr": std_res["slope_without_step_cm_yr"],
            "slope_with_step_cm_yr": std_res["slope_with_step_cm_yr"],
            "step_delta_cm": std_res["step_delta_cm"],
            "step_delta_se": std_res["step_delta_se"],
            "step_delta_ci95_low": std_res["step_delta_ci95"][0],
            "step_delta_ci95_high": std_res["step_delta_ci95"][1],
            "step_p_value": std_res["step_delta_p_value"],
            "step_verdict": verdict,
            "excl_n_obs": excl_res["n_obs"],
            "excl_step_delta_cm": excl_res["step_delta_cm"],
            "excl_step_p_value": excl_res["step_delta_p_value"],
            "excl_step_significant": excl_res["step_significant"],
        })
        print(f"  {reg:10s} Step delta = {std_res['step_delta_cm']:+.3f} cm (p = {std_res['step_delta_p_value']:.4f}) -> {verdict}")

    out_df = pd.DataFrame(rows)
    out_df.to_csv(CSV_PATH, index=False)

    summary = {
        "timestamp": datetime.now().isoformat(),
        "transition_date": "2018-06",
        "model": "y_t = beta_0 + beta_1 * t + delta * 1_{t >= 2018.5} + eps_t",
        "covariance_estimator": "HAC Newey-West (maxlags=12)",
        "results": rows,
    }
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"\n[OK] Saved offset test deliverables:")
    print(f"  CSV:  {CSV_PATH.name}")
    print(f"  JSON: {JSON_PATH.name}")
    return out_df


if __name__ == "__main__":
    run_offset_tests()
