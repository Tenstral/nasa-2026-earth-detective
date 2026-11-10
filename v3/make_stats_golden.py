"""
v3/make_stats_golden.py
=======================
Generates golden test cases using the Python Calibrated ESS-MK engine
(v3/trend_engine.py) to verify exact mathematical parity in the client-side
JavaScript engine (assets/js/stats.js).

Exports to: tests/fixtures/stats_golden.json
"""

import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from v3.trend_engine import run_ess_mann_kendall, deseasonalise


def generate_golden_cases():
    fixtures = []

    # 1. Real repository series: NW TWS full record
    reg_df = pd.read_csv(REPO_ROOT / "outputs/v3/full_record/region_series_2002_2026.csv")
    nw_tws = reg_df[reg_df["region"] == "NW"].dropna(subset=["grace_tws_cm", "decimal_year"]).copy()
    nw_tws["month"] = nw_tws["ym"].str.slice(5, 7).astype(int)
    y_raw = nw_tws["grace_tws_cm"].values
    months = nw_tws["month"].values
    t_years = nw_tws["decimal_year"].values

    y_des = deseasonalise(y_raw, months)
    res_nw_tws = run_ess_mann_kendall(t_years, y_des)
    fixtures.append({
        "case_id": "nw_tws_full_record_deseasonalized",
        "description": "Northwest Bangladesh GRACE/GRACE-FO Total Water Storage (2002-2026, deseasonalized)",
        "t": t_years.tolist(),
        "y_raw": y_raw.tolist(),
        "months": months.tolist(),
        "y_deseasonalized": y_des.tolist(),
        "expected": res_nw_tws,
    })

    # 2. NW TWS GRACE-FO era only (2018-06 to 2026-07) - The "Is 8 years enough?" Case
    nw_gfo = nw_tws[nw_tws["ym"] >= "2018-06"].copy()
    y_gfo = nw_gfo["grace_tws_cm"].values
    m_gfo = nw_gfo["month"].values
    t_gfo = nw_gfo["decimal_year"].values
    y_gfo_des = deseasonalise(y_gfo, m_gfo)
    res_gfo = run_ess_mann_kendall(t_gfo, y_gfo_des)
    fixtures.append({
        "case_id": "nw_tws_grace_fo_era",
        "description": "Northwest GRACE-FO single era (2018-2026, n=96, borderline significance)",
        "t": t_gfo.tolist(),
        "y_raw": y_gfo.tolist(),
        "months": m_gfo.tolist(),
        "y_deseasonalized": y_gfo_des.tolist(),
        "expected": res_gfo,
    })

    # 3. National Precipitation (IMERG)
    nat_df = reg_df[reg_df["region"] == "National"].dropna(subset=["imerg_precip_mm", "decimal_year"]).copy()
    nat_df["month"] = nat_df["ym"].str.slice(5, 7).astype(int)
    y_rain = nat_df["imerg_precip_mm"].values
    m_rain = nat_df["month"].values
    t_rain = nat_df["decimal_year"].values
    y_rain_des = deseasonalise(y_rain, m_rain)
    res_rain = run_ess_mann_kendall(t_rain, y_rain_des)
    fixtures.append({
        "case_id": "national_imerg_precip",
        "description": "National GPM IMERG Precipitation (2002-2025, deseasonalized)",
        "t": t_rain.tolist(),
        "y_raw": y_rain.tolist(),
        "months": m_rain.tolist(),
        "y_deseasonalized": y_rain_des.tolist(),
        "expected": res_rain,
    })

    # 4. Dhaka AERONET AOD (deseasonalized)
    aod_path = REPO_ROOT / "outputs/v3/aerosols/dhaka_aod_monthly.csv"
    if aod_path.exists():
        aod_df = pd.read_csv(aod_path)
        aod_df = aod_df.dropna(subset=["aod_550", "year", "month"])
        t_aod = (aod_df["year"] + (aod_df["month"] - 0.5) / 12.0).values
        y_aod = aod_df["aod_550"].values
        m_aod = aod_df["month"].values
        y_aod_des = deseasonalise(y_aod, m_aod)
        res_aod = run_ess_mann_kendall(t_aod, y_aod_des)
        fixtures.append({
            "case_id": "dhaka_aeronet_aod",
            "description": "Dhaka AERONET AOD (deseasonalized)",
            "t": t_aod.tolist(),
            "y_raw": y_aod.tolist(),
            "months": m_aod.tolist(),
            "y_deseasonalized": y_aod_des.tolist(),
            "expected": res_aod,
        })

    # 5. Synthetic edge case 1: Negative autocorrelation (r1 <= 0, gamma=1.0)
    rng = np.random.default_rng(42)
    t_syn = np.arange(2000, 2020, 1.0)
    # Alternating sign noise produces negative lag-1 autocorrelation
    y_syn1 = 0.5 * t_syn + np.array([1, -1] * 10) * 2.0
    res_syn1 = run_ess_mann_kendall(t_syn, y_syn1)
    fixtures.append({
        "case_id": "synthetic_negative_autocorr",
        "description": "Synthetic series with negative residual autocorrelation (gamma should clip to 1.0)",
        "t": t_syn.tolist(),
        "y": y_syn1.tolist(),
        "expected": res_syn1,
    })

    # 6. Synthetic edge case 2: Heavy ties in data
    y_syn2 = np.array([5.0, 5.0, 5.0, 6.0, 6.0, 6.0, 7.0, 7.0, 7.0, 8.0, 8.0, 8.0, 9.0, 9.0, 9.0])
    t_syn2 = np.arange(2000, 2015, 1.0)
    res_syn2 = run_ess_mann_kendall(t_syn2, y_syn2)
    fixtures.append({
        "case_id": "synthetic_ties",
        "description": "Synthetic series with repeated ties",
        "t": t_syn2.tolist(),
        "y": y_syn2.tolist(),
        "expected": res_syn2,
    })

    # 7. Synthetic edge case 3: Exactly zero slope
    y_syn3 = np.zeros(20)
    t_syn3 = np.arange(2000, 2020, 1.0)
    res_syn3 = run_ess_mann_kendall(t_syn3, y_syn3)
    fixtures.append({
        "case_id": "synthetic_zero_slope",
        "description": "Synthetic flat series (all zero)",
        "t": t_syn3.tolist(),
        "y": y_syn3.tolist(),
        "expected": res_syn3,
    })

    out_file = REPO_ROOT / "tests/fixtures/stats_golden.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(fixtures, f, indent=2)

    print(f"[OK] Generated {len(fixtures)} golden test cases -> {out_file}")


if __name__ == "__main__":
    generate_golden_cases()
