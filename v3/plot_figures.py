"""
NASA Space Apps 2026 – Bengal Hydro Detective
v3 Workstream 0: Advanced Publication Figures Suite
===================================================
Generates:
  1. fig2_seasonal_storage_response_24yr.png: 24-Season Rebound & Seasonal Storage Response Ratio Dynamics
  2. fig3_epoch_comparison.png: Forest Plot Comparing Epoch 1 vs Epoch 2 Slopes
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from v3.windows import REGIONS, OUTPUTS_V3_FULL

RECHARGE_CSV = OUTPUTS_V3_FULL / "seasonal_recharge_24yr.csv"
EPOCH_CSV = OUTPUTS_V3_FULL / "epoch_comparison.csv"


def plot_fig2_seasonal_storage_response():
    if not RECHARGE_CSV.exists():
        print(f"Skipping Fig 2: {RECHARGE_CSV.name} not found.")
        return

    df = pd.read_csv(RECHARGE_CSV)
    df = df[df["valid"] == True]

    reg_colors = {
        "NW": "#dc2626",
        "NE": "#8b5cf6",
        "Central": "#0284c7",
        "SW": "#059669",
        "SE": "#ea580c",
        "National": "#1f2937",
    }

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

    # Notable flood years
    flood_years = [2004, 2007, 2017, 2020, 2022]
    for fy in flood_years:
        ax1.axvline(fy, color="#94a3b8", linestyle="--", alpha=0.6)
        ax2.axvline(fy, color="#94a3b8", linestyle="--", alpha=0.6)

    # Panel 1: Storage Rebound (cm)
    for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
        sub = df[df["region"] == reg]
        ax1.plot(sub["year"], sub["rebound_cm"], marker="o", color=reg_colors[reg],
                 label=REGIONS[reg]["name_long"], lw=1.8 if reg != "National" else 2.5,
                 linestyle="-" if reg != "National" else "--")

    ax1.set_title("A. Annual Monsoon Storage Rebound (ΔTWS = Peak - Dry Season Low)", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Storage Rebound (cm)", fontsize=10)
    ax1.grid(True, linestyle=":", alpha=0.5)
    ax1.legend(loc="upper right", ncol=3, fontsize=8)

    # Panel 2: Seasonal Storage Response Ratio (%)
    for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
        sub = df[df["region"] == reg]
        eff_pct = sub["storage_response_ratio_imerg"] * 100.0
        ax2.plot(sub["year"], eff_pct, marker="s", color=reg_colors[reg],
                 label=f"{reg} Response Ratio", lw=1.8 if reg != "National" else 2.5,
                 linestyle="-" if reg != "National" else "--")

    ax2.set_title("B. Seasonal Storage Response Ratio: [ΔTWS (cm) / (0.1 × Monsoon Precip (cm))] × 100%", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Seasonal Storage Response Ratio (%)", fontsize=10)
    ax2.set_xlabel("Hydrological Year (2002–2025)", fontsize=11)
    ax2.grid(True, linestyle=":", alpha=0.5)

    # Add annotation for notable flood events
    for fy in flood_years:
        ax1.text(fy, 75, f"{fy} Flood", rotation=90, verticalalignment="bottom", fontsize=8, color="#475569")

    plt.suptitle("Bengal Basin Hydrological Recovery & Seasonal Storage Response Dynamics (2002–2025)\n"
                 "PRELIMINARY — 24 Monsoon Seasons Analysis | Team Tenstral", fontsize=13, fontweight="bold", y=0.98)
    plt.tight_layout()
    fig2_path = OUTPUTS_V3_FULL / "fig2_seasonal_storage_response_24yr.png"
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"  [OK] Saved Figure 2: {fig2_path.name}")


def plot_fig3_epoch_comparison():
    if not EPOCH_CSV.exists():
        print(f"Skipping Fig 3: {EPOCH_CSV.name} not found.")
        return

    df = pd.read_csv(EPOCH_CSV)
    regions = df["region"].tolist()
    y_pos = np.arange(len(regions))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

    # Left Panel: Epoch 1 vs Epoch 2 slopes
    ax1.axvline(0, color="black", linestyle="--", lw=0.8, alpha=0.7)
    
    # Epoch 1 (GRACE 2002-2017)
    ep1_slopes = df["epoch1_slope_cm_yr"]
    ep1_err_low = ep1_slopes - df["epoch1_ci95_low"]
    ep1_err_high = df["epoch1_ci95_high"] - ep1_slopes
    ax1.errorbar(ep1_slopes, y_pos - 0.15, xerr=[ep1_err_low, ep1_err_high], fmt="o", color="#2563eb",
                  label="Epoch 1: GRACE (2002–2017)", capsize=4, markersize=7)

    # Epoch 2 (GRACE-FO 2018-2026)
    ep2_slopes = df["epoch2_slope_cm_yr"]
    ep2_err_low = ep2_slopes - df["epoch2_ci95_low"]
    ep2_err_high = df["epoch2_ci95_high"] - ep2_slopes
    ax1.errorbar(ep2_slopes, y_pos + 0.15, xerr=[ep2_err_low, ep2_err_high], fmt="s", color="#dc2626",
                  label="Epoch 2: GRACE-FO (2018–2026)", capsize=4, markersize=7)

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels([REGIONS[r]["name_long"] for r in regions], fontsize=10)
    ax1.set_xlabel("Theil-Sen Slope (cm/yr)", fontsize=10)
    ax1.set_title("A. TWS Anomaly Slopes by Mission Epoch (95% CI)", fontsize=11, fontweight="bold")
    ax1.grid(True, linestyle=":", alpha=0.5)
    ax1.legend(loc="lower left", fontsize=9)

    # Right Panel: Slope Difference (Epoch 2 - Epoch 1)
    ax2.axvline(0, color="red", linestyle="--", lw=1.2, alpha=0.8, label="Zero Difference (Equal Rate)")
    diffs = df["diff_slope_cm_yr"]
    diff_err_low = diffs - df["diff_ci95_low"]
    diff_err_high = df["diff_ci95_high"] - diffs
    ax2.errorbar(diffs, y_pos, xerr=[diff_err_low, diff_err_high], fmt="D", color="#10b981",
                 label="Paired Bootstrap Difference (Δ Slope)", capsize=4, markersize=7)

    # Annotate verdict
    for i, r in df.iterrows():
        ax2.text(diffs[i], y_pos[i] + 0.22, r["verdict"], fontsize=8, color="#1f2937",
                 ha="center", bbox=dict(boxstyle="round,pad=0.2", facecolor="#f1f5f9", alpha=0.8))

    ax2.set_xlabel("Slope Difference: Epoch 2 - Epoch 1 (cm/yr)", fontsize=10)
    ax2.set_title("B. Paired Bootstrap Slope Difference Test (95% CI)", fontsize=11, fontweight="bold")
    ax2.grid(True, linestyle=":", alpha=0.5)
    ax2.legend(loc="lower left", fontsize=9)

    plt.suptitle("Instrumental Transition Comparison: GRACE vs GRACE-FO Trends in Bangladesh\n"
                 "PRELIMINARY — Paired Circular Block Bootstrap (B=9,999) | Team Tenstral", fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig3_path = OUTPUTS_V3_FULL / "fig3_epoch_comparison.png"
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    print(f"  [OK] Saved Figure 3: {fig3_path.name}")


if __name__ == "__main__":
    plot_fig2_seasonal_storage_response()
    plot_fig3_epoch_comparison()
