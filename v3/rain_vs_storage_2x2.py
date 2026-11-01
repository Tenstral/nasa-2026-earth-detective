"""
NASA Space Apps 2026 – Bengal Hydro Detective
v3 Workstream 0: Rain-vs-Storage 2x2 Hydrological Quadrant Matrix
==================================================================
Classifies all 6 regions and 8 administrative divisions into hydrological
quadrants across annual, monsoon, and dry seasons for the primary full record (2002–2026):
  - TWS Storage verdict (calibrated ESS-MK / Surrogate)
  - Primary Precipitation verdict (calibrated GPM IMERG V07B)

Quadrants:
  - Q1: Decoupled Depletion (Bengal Water Storage Paradox)
        [TWS Significant Decrease + Precip Stable/Increasing]
  - Suggestive: Suggestive Depletion / Inconclusive (Fails FDR)
        [TWS Suggestive Decrease + Precip Stable/Increasing]
  - Q2: Drought-Driven Depletion
        [TWS Decrease + Precip Decrease]
  - Q3: Hydrologically Steady / Below Detection Limit
        [TWS No detectable trend + Precip No detectable trend]
  - Q4: Resilient Buffering
        [TWS Stable/Increasing + Precip Decrease]
  - Q5: Concurrent Accretion
        [TWS Increase + Precip Increase]

Outputs:
  outputs/v3/full_record/rain_vs_storage_2x2_classification.csv
  outputs/v3/full_record/rain_vs_storage_2x2_classification.md
  outputs/v3/full_record/fig_2x2_quadrant_matrix.png
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_V3_FULL = REPO_ROOT / "outputs" / "v3" / "full_record"
RESULTS_FILE = OUTPUTS_V3_FULL / "results_all_windows.csv"
OUT_CSV = OUTPUTS_V3_FULL / "rain_vs_storage_2x2_classification.csv"
OUT_MD = OUTPUTS_V3_FULL / "rain_vs_storage_2x2_classification.md"
OUT_PNG = OUTPUTS_V3_FULL / "fig_2x2_quadrant_matrix.png"


def classify_quadrant(tws_verdict: str, tws_slope: float, tws_q: float,
                      pre_verdict: str, pre_slope: float, pre_q: float) -> tuple[str, str, str]:
    """
    Classify region or division into hydrological quadrants based on trend verdicts and slope signs.
    """
    is_tws_sig_down = (tws_verdict == "Significant") and (tws_slope < 0)
    is_tws_sug_down = (tws_verdict == "Suggestive") and (tws_slope < 0)
    is_tws_sig_up   = (tws_verdict == "Significant") and (tws_slope > 0)
    is_tws_sug_up   = (tws_verdict == "Suggestive") and (tws_slope > 0)

    pre_down = ("Significant" in pre_verdict or "Suggestive" in pre_verdict) and (pre_slope < 0)
    pre_up   = ("Significant" in pre_verdict or "Suggestive" in pre_verdict) and (pre_slope > 0)

    if is_tws_sig_down and not pre_down:
        q_id = "Q1"
        q_name = "Decoupled Depletion (Bengal Water Storage Paradox)"
        q_desc = "Total water storage is depleting significantly (FDR q < 0.05, CI excludes zero) despite stable or normal rainfall influx (consistent with human abstraction exceeding recharge)."
    elif is_tws_sug_down and not pre_down:
        q_id = "Suggestive"
        q_name = "Suggestive Depletion / Inconclusive (Fails FDR)"
        q_desc = "Storage decline is suggestive at raw p < 0.05 but does not pass stringent BH-FDR; rainfall shows no detectable trend."
    elif (is_tws_sig_down or is_tws_sug_down) and pre_down:
        q_id = "Q2"
        q_name = "Drought-Driven Depletion"
        q_desc = "Storage depletion is accompanied by significant precipitation decline."
    elif (not is_tws_sig_down and not is_tws_sug_down and not is_tws_sig_up and not is_tws_sug_up) and not pre_down and not pre_up:
        q_id = "Q3"
        q_name = "Hydrologically Steady / Below Detection Limit"
        q_desc = "Neither storage nor precipitation exhibits a detectable trend (consistent with hydrologic steady-state or trends below detection limit)."
    elif not is_tws_sig_down and not is_tws_sug_down and pre_down:
        q_id = "Q4"
        q_name = "Resilient Buffering"
        q_desc = "Storage remains stable despite declining precipitation."
    elif (is_tws_sig_up or is_tws_sug_up) and pre_up:
        q_id = "Q5"
        q_name = "Concurrent Accretion"
        q_desc = "Both storage and precipitation show significant upward accumulation."
    else:
        q_id = "Q3"
        q_name = "Hydrologically Steady / Below Detection Limit"
        q_desc = "Hydrological metrics remain within normal natural variability bounds."

    return q_id, q_name, q_desc


def run_2x2_analysis():
    if not RESULTS_FILE.exists():
        raise FileNotFoundError(f"Missing {RESULTS_FILE}")

    df = pd.read_csv(RESULTS_FILE)
    df_prim = df[df["window"] == "full_record"].copy()

    entities = [
        ("NW", "region"), ("NE", "region"), ("Central", "region"),
        ("SW", "region"), ("SE", "region"), ("National", "region"),
        ("Dhaka", "division"), ("Chattogram", "division"), ("Rajshahi", "division"),
        ("Rangpur", "division"), ("Khulna", "division"), ("Barishal", "division"),
        ("Sylhet", "division"), ("Mymensingh", "division")
    ]

    records = []
    for ent, ent_type in entities:
        for season in ["annual", "monsoon", "dry"]:
            sub_t = df_prim[(df_prim["entity"] == ent) & (df_prim["season"] == season) & (df_prim["variable"] == "tws")]
            sub_p = df_prim[(df_prim["entity"] == ent) & (df_prim["season"] == season) & (df_prim["variable"] == "precip")]

            if sub_t.empty or sub_p.empty:
                continue

            rt = sub_t.iloc[0]
            rp = sub_p.iloc[0]

            q_id, q_name, q_desc = classify_quadrant(
                rt["verdict"], rt["slope"], rt["bh_fdr_q_value"],
                rp["verdict"], rp["slope"], rp["bh_fdr_q_value"]
            )

            records.append({
                "entity": ent,
                "entity_type": ent_type,
                "season": season,
                "tws_slope_cm_yr": rt["slope"],
                "tws_ci_low": rt["slope_ci_low"],
                "tws_ci_high": rt["slope_ci_high"],
                "tws_p_value": rt["p_value"],
                "tws_fdr_q": rt["bh_fdr_q_value"],
                "tws_verdict": rt["verdict"],
                "precip_source": rp.get("precip_source", "GPM_IMERG_V07B"),
                "precip_slope_mm_yr": rp["slope"],
                "precip_ci_low": rp["slope_ci_low"],
                "precip_ci_high": rp["slope_ci_high"],
                "precip_p_value": rp["p_value"],
                "precip_fdr_q": rp["bh_fdr_q_value"],
                "precip_verdict": rp["verdict"],
                "quadrant_id": q_id,
                "quadrant_name": q_name,
                "quadrant_description": q_desc,
            })

    class_df = pd.DataFrame(records)
    class_df.to_csv(OUT_CSV, index=False)
    print(f"Saved: {OUT_CSV} ({len(class_df)} rows)")

    # Build Markdown Deliverable
    ann_reg = class_df[(class_df["entity_type"] == "region") & (class_df["season"] == "annual")].copy()
    ann_div = class_df[(class_df["entity_type"] == "division") & (class_df["season"] == "annual")].copy()

    md = [
        "# Hydrological Coupling Matrix: Total Water Storage vs. Rainfall Trends (2002–2026)",
        "",
        "**Status:** PRELIMINARY — Primary Full-Record Analytical Window (2002-04 to 2026-07)",
        "- **TWS Storage Engine:** Calibrated Effective-Sample-Size (ESS) Mann-Kendall with Hurwicz bias correction and Fourier phase-randomized surrogate.",
        "- **Primary Precipitation Record:** GPM IMERG V07B Final Run (2002–2025; decoupled from GRACE).",
        "",
        "## 1. Regional Annual Classifications",
        "",
        "| Region | TWS Slope (cm/yr) [95% CI] | TWS Verdict (FDR q) | IMERG Rain Slope (mm/yr) [95% CI] | Rain Verdict (FDR q) | Quadrant ID | Coupling Classification |",
        "|---|---|---|---|---|---|---|",
    ]

    for _, r in ann_reg.iterrows():
        t_str = f"{r['tws_slope_cm_yr']:+.2f} [{r['tws_ci_low']:+.2f}, {r['tws_ci_high']:+.2f}]"
        p_str = f"{r['precip_slope_mm_yr']:+.2f} [{r['precip_ci_low']:+.2f}, {r['precip_ci_high']:+.2f}]"
        t_q = "< 0.0001" if r["tws_fdr_q"] < 0.0001 else f"{r['tws_fdr_q']:.4f}"
        p_q = "< 0.0001" if r["precip_fdr_q"] < 0.0001 else f"{r['precip_fdr_q']:.4f}"

        badge = f"**`{r['quadrant_id']}`**" if r["quadrant_id"] == "Q1" else f"`{r['quadrant_id']}`"
        md.append(
            f"| **{r['entity']}** | {t_str} | `{r['tws_verdict']}` (q={t_q}) | {p_str} | `{r['precip_verdict']}` (q={p_q}) | {badge} | {r['quadrant_name']} |"
        )

    md.extend([
        "",
        "## 2. Divisional Annual Classifications",
        "",
        "| Division | TWS Slope (cm/yr) [95% CI] | TWS Verdict | IMERG Rain Slope (mm/yr) [95% CI] | Rain Verdict | Quadrant ID | Coupling Classification |",
        "|---|---|---|---|---|---|---|",
    ])

    for _, r in ann_div.iterrows():
        t_str = f"{r['tws_slope_cm_yr']:+.2f} [{r['tws_ci_low']:+.2f}, {r['tws_ci_high']:+.2f}]"
        p_str = f"{r['precip_slope_mm_yr']:+.2f} [{r['precip_ci_low']:+.2f}, {r['precip_ci_high']:+.2f}]"
        badge = f"**`{r['quadrant_id']}`**" if r["quadrant_id"] == "Q1" else f"`{r['quadrant_id']}`"
        md.append(
            f"| **{r['entity']}** | {t_str} | `{r['tws_verdict']}` | {p_str} | `{r['precip_verdict']}` | {badge} | {r['quadrant_name']} |"
        )

    md.extend([
        "",
        "## 3. Hydrological Interpretation",
        "",
        "1. **Resolution of the Bengal Water Storage Paradox:**",
        "   - In the **Northwest, Northeast, Central, and National** composite, Total Water Storage exhibits statistically significant multi-decadal depletion (-0.47 to -1.25 cm/yr), while GPM IMERG precipitation shows no detectable trend (-1.9 to +2.0 mm/yr, p >= 0.51).",
        "   - These regions fall unambiguously into **Quadrant 1: Decoupled Depletion (Bengal Water Storage Paradox)**.",
        "   - Because precipitation has remained stationary without secular decline, the observed storage depletion cannot be attributed to meteorological drought.",
        "   - This observation is **consistent with, not proof of**, human water extraction exceeding natural replenishment capacity (such as intensive Boro dry-season groundwater abstraction).",
        "",
        "2. **Hydrologically Steady Coastal Delta:**",
        "   - In the **Southwest and Southeast**, both storage and precipitation exhibit no detectable trend over the 24-year satellite record (-0.05 cm/yr TWS; +1.8 to +2.3 mm/yr rain), falling into **Quadrant 3: Hydrologically Steady / Below Detection Limit**.",
    ])

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"Saved: {OUT_MD}")

    # Generate Publication Figure
    plot_2x2_figure(ann_reg, ann_div)


def plot_2x2_figure(reg_df: pd.DataFrame, div_df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 8))

    # Quadrant background colors
    ax.axhspan(-3.5, 0, xmin=0.45, xmax=1.0, color="#fee2e2", alpha=0.35, zorder=0)  # Q1 (bottom right quadrant if rain > 0)
    ax.axhspan(-3.5, 0, xmin=0.0, xmax=0.45, color="#fef3c7", alpha=0.30, zorder=0)  # Q2 (bottom left quadrant if rain < 0)
    ax.axhspan(0, 1.5, xmin=0.45, xmax=1.0, color="#ecfdf5", alpha=0.35, zorder=0)   # Steady / Accretion (top right)
    ax.axhspan(0, 1.5, xmin=0.0, xmax=0.45, color="#f1f5f9", alpha=0.30, zorder=0)   # Buffering (top left)

    ax.axhline(0, color="#64748b", linestyle="--", lw=1.2, alpha=0.7)
    ax.axvline(0, color="#64748b", linestyle="--", lw=1.2, alpha=0.7)

    # Plot divisions
    for _, r in div_df.iterrows():
        ax.scatter(r["precip_slope_mm_yr"], r["tws_slope_cm_yr"],
                   color="#94a3b8", s=60, alpha=0.7, zorder=3)
        ax.annotate(r["entity"], (r["precip_slope_mm_yr"], r["tws_slope_cm_yr"]),
                    fontsize=8, color="#64748b", xytext=(4, 4), textcoords="offset points")

    # Plot regions
    reg_colors = {
        "NW": "#dc2626", "NE": "#8b5cf6", "Central": "#0284c7",
        "SW": "#059669", "SE": "#ea580c", "National": "#111827"
    }
    for _, r in reg_df.iterrows():
        c = reg_colors.get(r["entity"], "#000000")
        ax.scatter(r["precip_slope_mm_yr"], r["tws_slope_cm_yr"],
                   color=c, s=140, edgecolors="black", lw=1.5, zorder=4, label=f"Region: {r['entity']}")
        ax.annotate(r["entity"], (r["precip_slope_mm_yr"], r["tws_slope_cm_yr"]),
                    fontsize=10, fontweight="bold", color=c, xytext=(6, -6), textcoords="offset points")

    # Quadrant Labels
    ax.text(2.5, -2.8, "QUADRANT 1: Decoupled Depletion\n(Bengal Water Storage Paradox)\n• Significant Storage Depletion\n• Stable/Normal Rainfall Influx",
            fontsize=9, fontweight="bold", color="#991b1b",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#ffffff", edgecolor="#f87171", alpha=0.85))

    ax.text(-2.5, -2.8, "QUADRANT 2: Drought-Driven\n• Storage Depletion\n• Declining Rainfall",
            fontsize=9, color="#92400e",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#ffffff", edgecolor="#fcd34d", alpha=0.85))

    ax.text(0.8, 0.9, "QUADRANT 3: Steady State\n• Stable Storage & Stable Rain",
            fontsize=9, color="#065f46",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#ffffff", edgecolor="#6ee7b7", alpha=0.85))

    ax.set_xlim(-4.0, 5.0)
    ax.set_ylim(-3.2, 1.2)
    ax.set_xlabel("Primary Precipitation Slope (mm/yr) [GPM IMERG V07B]", fontsize=11, fontweight="bold")
    ax.set_ylabel("Total Water Storage Slope (cm/yr) [Calibrated GRACE / GRACE-FO]", fontsize=11, fontweight="bold")
    ax.set_title("Rainfall vs. Terrestrial Water Storage Dynamics Across Bangladesh (2002–2026)\n"
                 "PRELIMINARY — Primary Full-Record Analysis | Team Tenstral", fontsize=12, fontweight="bold")
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(loc="upper left", fontsize=8, framealpha=0.9)

    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=300)
    plt.close()
    print(f"Saved: {OUT_PNG}")


if __name__ == "__main__":
    run_2x2_analysis()
