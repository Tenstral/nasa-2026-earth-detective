import sys
from pathlib import Path
REPO_ROOT = Path(r"c:\Users\LEON\OneDrive\Documents\GitHub\nasa-2026-earth-detective")
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import numpy as np
import pandas as pd
from scipy import stats
import pymannkendall as mk
from v2.task3_trend_engine import deseasonalise, RANDOM_SEED
from v3.trend_engine import run_ess_mann_kendall

reg_df = pd.read_csv(REPO_ROOT / "outputs/v3/full_record/region_series_2002_2026.csv")
reg_df['date'] = pd.to_datetime(reg_df['date'])
reg_df['month'] = reg_df['date'].dt.month

all_months = pd.date_range("2002-04-01", "2026-07-01", freq="MS")
nominal_yms = [d.strftime("%Y-%m") for d in all_months]
sub_nw = reg_df[reg_df["region"] == "NW"].dropna(subset=["grace_tws_cm"])
obs_yms = set(sub_nw["ym"].unique())
mask_obs = np.array([ym in obs_yms for ym in nominal_yms])

n_nom = len(nominal_yms)
dates_obs = all_months[mask_obs]
t_years = (dates_obs.year + (dates_obs.month - 0.5) / 12.0).values
t_years_zeroed = t_years - t_years[0]

n_sim = 2000
regions = ["NW", "NE", "Central", "SW", "SE", "National"]

for reg in regions:
    sub = reg_df[reg_df["region"] == reg].dropna(subset=["grace_tws_cm"]).copy()
    sub["t"] = sub["decimal_year"] - sub["decimal_year"].iloc[0]
    y_des = deseasonalise(sub["grace_tws_cm"].values, sub["month"].values)
    slope, intercept, _, _, _ = stats.linregress(sub["t"].values, y_des)
    e_detrend = y_des - (intercept + slope * sub["t"].values)
    phi = float(np.corrcoef(e_detrend[:-1], e_detrend[1:])[0, 1])
    sd = float(np.std(e_detrend, ddof=1))
    
    rng = np.random.default_rng(RANDOM_SEED + int(phi * 1000))
    rejs_ess = 0
    cov_ess = 0
    rejs_hr = 0
    
    for _ in range(n_sim):
        eta = rng.standard_normal(n_nom)
        e = np.zeros(n_nom)
        for t in range(1, n_nom):
            e[t] = phi * e[t-1] + np.sqrt(1.0 - phi**2) * eta[t]
        e_obs = e[mask_obs] * sd
        
        # ESS-MK
        res_ess = run_ess_mann_kendall(t_years_zeroed, e_obs)
        if res_ess["p_value"] < 0.05:
            rejs_ess += 1
        if res_ess["ci_low"] <= 0.0 <= res_ess["ci_high"]:
            cov_ess += 1
            
        # Hamed-Rao
        res_hr = mk.hamed_rao_modification_test(e_obs)
        if not np.isnan(res_hr.p) and res_hr.p < 0.05:
            rejs_hr += 1
            
    fpr_ess = rejs_ess / n_sim
    cov_ess_rate = cov_ess / n_sim
    fpr_hr = rejs_hr / n_sim
    pass_ess = (0.035 <= fpr_ess <= 0.065) and (0.930 <= cov_ess_rate <= 0.970)
    print(f"{reg:10s} (phi={phi:.4f}, sd={sd:.2f}): ESS FPR={fpr_ess:.4f}, Cov={cov_ess_rate:.4f} [Pass: {pass_ess}] | HR FPR={fpr_hr:.4f}")
