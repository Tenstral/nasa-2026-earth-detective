"""
NASA Space Apps 2026 – Bengal Hydro Detective
v3 Workstream A: GPM IMERG vs NASA POWER Precipitation Comparison
==================================================================
1. Authenticates with NASA Earthdata using:
     a) Environment variables (EARTHDATA_USERNAME, EARTHDATA_PASSWORD)
     b) Netrc file (~/.netrc or ~/_netrc)
2. Searches NASA CMR for monthly GPM_3IMERGM v07 granules covering Bangladesh (2002–2026).
3. Downloads & subsets precipitation rate (mm/hr), converting to monthly accumulation (mm/month)
   using calendar-exact days per month. Asserts units and runs unit tests.
4. Builds divisional and regional series using identical spatial polygons and weights as POWER.
5. Computes comprehensive comparison metrics against NASA POWER:
     - Monthly Pearson r and Spearman rho
     - Mean Bias Error (MBE = IMERG - POWER) and RMSE
     - 12-Month Climatology cycle
     - Annual and seasonal (monsoon Jun-Sep, dry Dec-Mar) totals
     - Trend engine evaluation across all 4 windows
     - Sensor-mix step test on difference series (Delta P_t = IMERG_t - POWER_t)

Outputs:
  outputs/v3/imerg_vs_power/imerg_division_series.csv
  outputs/v3/imerg_vs_power/imerg_region_series.csv
  outputs/v3/imerg_vs_power/imerg_vs_power_comparison.csv
  outputs/v3/imerg_vs_power/imerg_vs_power_climatology.csv
  outputs/v3/imerg_vs_power/imerg_vs_power_summary.json
  outputs/v3/imerg_vs_power/fig_imerg_vs_power_comparison.png
"""

import os
import sys
import json
import calendar
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import numpy as np
import pandas as pd
import xarray as xr
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from v3.windows import REGIONS, DIV_AREAS, SEASONS, OUTPUTS_V3
from tests.test_imerg_units import convert_imerg_rate_to_monthly_accumulation

OUTPUT_DIR = OUTPUTS_V3 / "imerg_vs_power"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def check_auth_credentials() -> dict:
    """
    Checks for presence of Earthdata credentials in environment variables or netrc.
    Returns status dict.
    """
    u = os.environ.get("EARTHDATA_USERNAME")
    p = os.environ.get("EARTHDATA_PASSWORD")
    tok = os.environ.get("EARTHDATA_TOKEN")

    if (u and p) or tok:
        return {"authenticated": True, "source": "environment_variables", "username": u or "TOKEN_USER"}

    home = Path.home()
    for netrc_path in [home / ".netrc", home / "_netrc"]:
        if netrc_path.exists():
            content = netrc_path.read_text(encoding="utf-8")
            if "urs.earthdata.nasa.gov" in content:
                return {"authenticated": True, "source": str(netrc_path), "username": "NETRC_USER"}

    return {"authenticated": False, "source": None, "username": None}


def authenticate_earthaccess():
    """
    Authenticates earthaccess with environment variables or netrc.
    Raises RuntimeError if neither is available.
    """
    import earthaccess
    cred_info = check_auth_credentials()
    if not cred_info["authenticated"]:
        raise RuntimeError(
            "Earthdata credentials NOT FOUND. Please provide credentials via:\n"
            "  1. Environment variables: EARTHDATA_USERNAME and EARTHDATA_PASSWORD (or EARTHDATA_TOKEN)\n"
            "  2. Netrc file at ~/.netrc or ~/_netrc containing machine urs.earthdata.nasa.gov"
        )

    if cred_info["source"] == "environment_variables":
        auth = earthaccess.login(strategy="environment")
    else:
        auth = earthaccess.login(strategy="netrc")

    if not auth.authenticated:
        raise RuntimeError("Failed to authenticate with NASA Earthdata. Check username/password validity.")
    print(f"  [OK] Authenticated with NASA Earthdata via {cred_info['source']} ({cred_info['username']})")
    return auth


def compare_series(imerg_reg_df: pd.DataFrame, power_reg_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """
    Computes comparative metrics between IMERG and POWER precipitation across regions.
    """
    merged = pd.merge(
        imerg_reg_df[["region", "ym", "date", "imerg_precip_mm"]],
        power_reg_df[["region", "ym", "power_precip_mm"]],
        on=["region", "ym"],
        how="inner"
    ).dropna(subset=["imerg_precip_mm", "power_precip_mm"]).copy()

    merged["date"] = pd.to_datetime(merged["date"])
    merged["month"] = merged["date"].dt.month
    merged["year"] = merged["date"].dt.year
    merged["diff_mm"] = merged["imerg_precip_mm"] - merged["power_precip_mm"]

    comp_rows = []
    clim_rows = []

    for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
        sub = merged[merged["region"] == reg].copy()
        n = len(sub)
        if n < 12:
            continue

        im = sub["imerg_precip_mm"].values
        pw = sub["power_precip_mm"].values
        diff = sub["diff_mm"].values

        # Monthly metrics
        r, p_r = stats.pearsonr(im, pw)
        rho, p_rho = stats.spearmanr(im, pw)
        bias = float(np.mean(diff))
        mae = float(np.mean(np.abs(diff)))
        rmse = float(np.sqrt(np.mean(diff ** 2)))
        pbias = float(bias / np.mean(pw) * 100.0) if np.mean(pw) > 0 else 0.0

        # Seasonal totals
        monsoon_im = sub[sub["month"].isin([6, 7, 8, 9])]["imerg_precip_mm"].mean() * 4.0
        monsoon_pw = sub[sub["month"].isin([6, 7, 8, 9])]["power_precip_mm"].mean() * 4.0
        dry_im = sub[sub["month"].isin([12, 1, 2, 3])]["imerg_precip_mm"].mean() * 4.0
        dry_pw = sub[sub["month"].isin([12, 1, 2, 3])]["power_precip_mm"].mean() * 4.0

        comp_rows.append({
            "region": reg,
            "region_name": REGIONS[reg]["name_long"],
            "n_months": n,
            "pearson_r": round(float(r), 4),
            "pearson_p": round(float(p_r), 6),
            "spearman_rho": round(float(rho), 4),
            "mean_imerg_mm_mo": round(float(np.mean(im)), 2),
            "mean_power_mm_mo": round(float(np.mean(pw)), 2),
            "bias_mbe_mm_mo": round(bias, 2),
            "percent_bias_pct": round(pbias, 2),
            "mae_mm_mo": round(mae, 2),
            "rmse_mm_mo": round(rmse, 2),
            "monsoon_mean_imerg_mm": round(float(monsoon_im), 1),
            "monsoon_mean_power_mm": round(float(monsoon_pw), 1),
            "dry_mean_imerg_mm": round(float(dry_im), 1),
            "dry_mean_power_mm": round(float(dry_pw), 1),
        })

        # Climatology
        for m in range(1, 13):
            m_sub = sub[sub["month"] == m]
            clim_rows.append({
                "region": reg,
                "month": m,
                "imerg_climatology_mm": round(float(m_sub["imerg_precip_mm"].mean()), 2),
                "power_climatology_mm": round(float(m_sub["power_precip_mm"].mean()), 2),
                "bias_mm": round(float(m_sub["diff_mm"].mean()), 2),
            })

    comp_df = pd.DataFrame(comp_rows)
    clim_df = pd.DataFrame(clim_rows)
    return comp_df, clim_df, merged


def plot_comparison_figures(merged_df: pd.DataFrame, clim_df: pd.DataFrame, comp_df: pd.DataFrame):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Panel 1: Scatter National IMERG vs POWER
    nat = merged_df[merged_df["region"] == "National"]
    ax1.scatter(nat["power_precip_mm"], nat["imerg_precip_mm"], color="#0284c7", alpha=0.5, s=20)
    max_val = max(nat["power_precip_mm"].max(), nat["imerg_precip_mm"].max()) + 50
    ax1.plot([0, max_val], [0, max_val], "r--", label="1:1 Perfect Agreement")
    
    r_val = comp_df[comp_df["region"] == "National"]["pearson_r"].iloc[0]
    bias_val = comp_df[comp_df["region"] == "National"]["bias_mbe_mm_mo"].iloc[0]
    ax1.set_title(f"A. National Monthly Precipitation: IMERG vs POWER (r = {r_val:.3f}, Bias = {bias_val:+.1f} mm/mo)",
                  fontsize=11, fontweight="bold")
    ax1.set_xlabel("NASA POWER (mm/month)", fontsize=10)
    ax1.set_ylabel("GPM IMERG V07 (mm/month)", fontsize=10)
    ax1.grid(True, linestyle=":", alpha=0.5)
    ax1.legend(loc="upper left")

    # Panel 2: National Climatology
    nat_clim = clim_df[clim_df["region"] == "National"]
    months = np.arange(1, 13)
    ax2.plot(months, nat_clim["power_climatology_mm"], "b-o", label="NASA POWER Climatology", lw=2)
    ax2.plot(months, nat_clim["imerg_climatology_mm"], "g-s", label="GPM IMERG V07 Climatology", lw=2)
    ax2.bar(months, nat_clim["bias_mm"], alpha=0.3, color="gray", label="Bias (IMERG - POWER)")
    ax2.set_xticks(months)
    ax2.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    ax2.set_title("B. National Mean Annual Climatology Cycle (2002–2026)", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Monthly Accumulation (mm/month)", fontsize=10)
    ax2.grid(True, linestyle=":", alpha=0.5)
    ax2.legend(loc="upper left")

    plt.suptitle("GPM IMERG V07 vs NASA POWER Precipitation Cross-Validation\n"
                 "PRELIMINARY — Bangladesh Hydro Detective | Team Tenstral", fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig_path = OUTPUT_DIR / "fig_imerg_vs_power_comparison.png"
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"  [OK] Saved Comparison Figure: {fig_path.name}")
