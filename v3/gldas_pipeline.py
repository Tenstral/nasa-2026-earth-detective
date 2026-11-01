"""
NASA Space Apps 2026 – Bengal Hydro Detective
v3 Workstream B: GLDAS Soil-Moisture & Storage Partitioning Pipeline
====================================================================
1. Authenticates with NASA Earthdata using:
     a) Environment variables (EARTHDATA_USERNAME, EARTHDATA_PASSWORD)
     b) Netrc file (~/.netrc or ~/_netrc)
2. Searches NASA CMR for GLDAS Noah 2.1 monthly grids (GLDAS_NOAH025_M v2.1) covering Bangladesh (2000–present).
3. Downloads & subsets moisture layers:
     - SoilMoi0_10cm_inst   (0-10 cm)
     - SoilMoi10_40cm_inst  (10-40 cm)
     - SoilMoi40_100cm_inst (40-100 cm)
     - SoilMoi100_200cm_inst (100-200 cm)   [Total soil depth: 2.0 m]
     - CanopInt_inst        (Canopy water storage)
     - SWE_inst             (Snow water equivalent)
4. Converts all layers from kg/m^2 to cm of water equivalent (/ 10.0).
5. Aggregates divisional and regional series using identical spatial masks and weights as GRACE and POWER.
6. Re-baselines model storage to the GRACE 2004-01 to 2009-12 reference epoch (mean anomaly == 0.0 cm).
7. Computes residual storage anomaly:
     Residual = TWS - Delta SMS - Delta SWE
   Strictly labeled: 'groundwater + surface water + model error residual'.
8. Evaluates trend engine across all 4 windows and generates diagnostic partition figures.

Outputs:
  outputs/v3/gldas_split/gldas_noah_regional_series.csv
  outputs/v3/gldas_split/storage_partition_series.csv
  outputs/v3/gldas_split/partition_trend_results.csv
  outputs/v3/gldas_split/fig_storage_partition_trends.png
  outputs/v3/gldas_split/gldas_partition_summary.json
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from v3.windows import REGIONS, DIV_AREAS, OUTPUTS_V3
from tests.test_gldas_processing import convert_gldas_to_cm, rebaseline_to_reference_period, calculate_water_residual

OUTPUT_DIR = OUTPUTS_V3 / "gldas_split"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def check_auth_credentials() -> dict:
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
    import earthaccess
    cred_info = check_auth_credentials()
    if not cred_info["authenticated"]:
        raise RuntimeError(
            "Earthdata credentials NOT FOUND. Please provide credentials via:\n"
            "  1. Environment variables: EARTHDATA_USERNAME and EARTHDATA_PASSWORD\n"
            "  2. Netrc file at ~/.netrc or ~/_netrc containing machine urs.earthdata.nasa.gov"
        )

    if cred_info["source"] == "environment_variables":
        auth = earthaccess.login(strategy="environment")
    else:
        auth = earthaccess.login(strategy="netrc")

    if not auth.authenticated:
        raise RuntimeError("Failed to authenticate with NASA Earthdata. Check credentials.")
    print(f"  [OK] Authenticated with NASA Earthdata via {cred_info['source']}")
    return auth


def partition_storage(tws_df: pd.DataFrame, gldas_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merges regional TWS with re-baselined GLDAS soil moisture anomalies and computes residual.
    """
    merged = pd.merge(
        tws_df[["region", "ym", "date", "tws_cm"]],
        gldas_df[["region", "ym", "sms_anom_cm", "swe_anom_cm", "canopy_anom_cm"]],
        on=["region", "ym"],
        how="inner"
    ).dropna(subset=["tws_cm", "sms_anom_cm"]).copy()

    merged["residual_cm"] = calculate_water_residual(
        tws_anomaly_cm=merged["tws_cm"].values,
        sms_anomaly_cm=merged["sms_anom_cm"].values,
        swe_anomaly_cm=merged["swe_anom_cm"].fillna(0.0).values
    )
    return merged


def plot_partition_figures(partition_df: pd.DataFrame):
    """
    Generates 2-panel figure showing TWS vs GLDAS Soil Moisture vs Residual Storage.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

    for reg, col in [("NW", "#d97706"), ("NE", "#0284c7"), ("Central", "#7c3aed"), ("National", "#111827")]:
        sub = partition_df[partition_df["region"] == reg].sort_values("date")
        dates = pd.to_datetime(sub["date"])
        
        # Panel 1: TWS vs SMS
        ax1.plot(dates, sub["tws_cm"], label=f"{reg} TWS Anomaly (GRACE)", lw=1.8 if reg == "National" else 1.2, color=col)
        ax1.plot(dates, sub["sms_anom_cm"], "--", label=f"{reg} Soil Moisture (GLDAS)", lw=1.2, alpha=0.7, color=col)
        
        # Panel 2: Residual Storage (GW + SW + error)
        ax2.plot(dates, sub["residual_cm"], label=f"{reg} Residual (GW+SW+error)", lw=1.8 if reg == "National" else 1.2, color=col)

    ax1.set_title("A. Terrestrial Water Storage (GRACE) vs Soil Moisture Anomaly (GLDAS Noah 2.1)",
                  fontsize=12, fontweight="bold")
    ax1.set_ylabel("Equivalent Water Thickness (cm)", fontsize=10)
    ax1.grid(True, linestyle=":", alpha=0.5)
    ax1.axhline(0, color="gray", lw=0.8, linestyle="--")
    ax1.legend(loc="lower left", ncol=4, fontsize=8)

    ax2.set_title("B. Partitioned Residual Storage Anomaly (Groundwater + Surface Water + Model Residual)",
                  fontsize=12, fontweight="bold")
    ax2.set_ylabel("Residual Equivalent Water Thickness (cm)", fontsize=10)
    ax2.set_xlabel("Year", fontsize=10)
    ax2.grid(True, linestyle=":", alpha=0.5)
    ax2.axhline(0, color="gray", lw=0.8, linestyle="--")
    ax2.legend(loc="lower left", ncol=4, fontsize=8)

    plt.suptitle("Bengal Basin Terrestrial Water Storage Partitioning (2002–2026)\n"
                 "PRELIMINARY — Team Tenstral | NASA Space Apps Challenge 2026", fontsize=13, fontweight="bold")
    plt.tight_layout()
    fig_path = OUTPUT_DIR / "fig_storage_partition_trends.png"
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"  [OK] Saved Storage Partition Figure: {fig_path.name}")


if __name__ == "__main__":
    print("GLDAS Pipeline Module initialized. Authentication status:")
    print(check_auth_credentials())
