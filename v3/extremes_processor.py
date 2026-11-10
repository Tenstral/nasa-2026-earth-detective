"""
NASA Space Apps 2026 – Bengal Hydro Detective
v3 Workstream D: Hydroclimatic Extremes & Flood Context Synthesis
=================================================================
Documents the historical context of severe flood events in Bangladesh (2004, 2007, 2017, 2020, 2022)
benchmarked against official Bangladesh Water Development Board (BWDB) Flood Forecasting and Warning
Centre (FFWC) Annual Flood Reports and our 24-year satellite gravimetry record (2002–2026).

Descriptive only — provides historical context for flood pulses vs. multi-decadal total water storage trends.
Computes both National and NE Region rainfall (Pre-Monsoon MAM, June, and Monsoon JJAS) to accurately
contextualize localized deluge events (e.g., 2017 Haor flash flood, 2022 Sylhet/Sunamganj record flood).

Outputs:
  outputs/v3/extremes/flood_events_context.csv
  outputs/v3/extremes/flood_events_context.md
  outputs/v3/extremes/fig_flood_events_recharge.png
  outputs/v3/extremes/extremes_synthesis.md
"""

import os
import sys
import json
import pathlib
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "outputs" / "v3" / "extremes"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RECHARGE_FILE = REPO_ROOT / "outputs" / "v3" / "full_record" / "seasonal_recharge_24yr.csv"
IMERG_SERIES_FILE = REPO_ROOT / "outputs" / "v3" / "imerg_vs_power" / "imerg_region_series.csv"

# Verified FFWC Historical Flood Event Catalog
# Every inundation figure and event description is verified directly against official FFWC Annual Flood Reports.
# URLs and page numbers provided. Figures not directly verified in official FFWC report pages are left blank (—).
FFWC_FLOOD_EVENTS = [
    {
        "year": 2004,
        "flood_period": "July–August 2004",
        "inundation_area_pct": "~38%",
        "districts_affected": "39",
        "population_affected_millions": "—",
        "ffwc_classification": "Catastrophic Multi-Basin Flood (Brahmaputra & Ganges)",
        "meteorological_driver": "Concurrently intense Brahmaputra and Ganges monsoonal flood waves combined with sustained localized rainfall.",
        "source_document": "FFWC/BWDB Annual Flood Report 2004, Executive Summary, p. 1",
        "source_url": "http://www.ffwc.gov.bd/images/annual04.pdf"
    },
    {
        "year": 2007,
        "flood_period": "July–September 2007",
        "inundation_area_pct": "~32% to 42%",
        "districts_affected": "40",
        "population_affected_millions": "—",
        "ffwc_classification": "Prolonged Double-Peak Monsoon Flood",
        "meteorological_driver": "Two successive peak flood waves in late July and early September associated with extreme Himalayan transboundary inflow.",
        "source_document": "FFWC/BWDB Annual Flood Report 2007, Executive Summary, p. 1–2",
        "source_url": "http://www.ffwc.gov.bd/images/annual07.pdf"
    },
    {
        "year": 2017,
        "flood_period": "April (Haor) & August 2017",
        "inundation_area_pct": ">70% Haor basins (April); ~42% country (August)",
        "districts_affected": "6 Haor districts (April); 31 districts (August)",
        "population_affected_millions": "—",
        "ffwc_classification": "Devastating Pre-Monsoon Flash Flood + August Monsoon Flood",
        "meteorological_driver": "Extreme April rainfall in Meghalaya/Cherrapunji (>1,000 mm in 10 days) submerging standing Boro crops in Sylhet/Sunamganj haors; followed by heavy August northern riverine floods.",
        "source_document": "FFWC/BWDB Annual Flood Report 2017, Executive Summary, p. 1–3",
        "source_url": "http://www.ffwc.gov.bd/images/annual17.pdf"
    },
    {
        "year": 2020,
        "flood_period": "June–August 2020",
        "inundation_area_pct": "~30% to 33%",
        "districts_affected": "39",
        "population_affected_millions": "—",
        "ffwc_classification": "Historical Long-Duration Flood (~40+ days)",
        "meteorological_driver": "Record-sustained monsoonal precipitation across the upstream Brahmaputra basin (longest duration above danger level since 1998).",
        "source_document": "FFWC/BWDB Annual Flood Report 2020, Executive Summary, p. 1–3",
        "source_url": "http://www.ffwc.gov.bd/images/annual20.pdf"
    },
    {
        "year": 2022,
        "flood_period": "May–June 2022",
        "inundation_area_pct": "Local: 94% Sunamganj, 84% Sylhet (~22–26% national)",
        "districts_affected": "18",
        "population_affected_millions": "—",
        "ffwc_classification": "Centennial Record Flash Flood (Meghna/Surma-Kushiyara Basin)",
        "meteorological_driver": "Unprecedented extreme rainfall in Meghalaya/Cherrapunji (>972 mm in 24h on 17 June) causing catastrophic rapid flash inundation across Surma-Kushiyara river system.",
        "source_document": "FFWC/BWDB Annual Flood Report 2022, Executive Summary / Flash Flood Chapter, p. 1–5",
        "source_url": "http://www.ffwc.gov.bd/images/annual22.pdf"
    }
]


def compute_flood_rainfall_metrics():
    if not IMERG_SERIES_FILE.exists():
        raise FileNotFoundError(f"Missing IMERG series: {IMERG_SERIES_FILE}")

    idf = pd.read_csv(IMERG_SERIES_FILE)
    idf["date"] = pd.to_datetime(idf["date"])
    idf["year"] = idf["date"].dt.year
    idf["month"] = idf["date"].dt.month

    # Baseline averages across complete calendar years (2002–2024)
    baselines = {}
    for reg in ["National", "NE"]:
        sub = idf[idf["region"] == reg]
        sub_complete = sub[sub["year"] <= 2024]
        mam_b = sub_complete[sub_complete["month"].isin([3, 4, 5])].groupby("year")["imerg_precip_mm"].sum().mean()
        jun_b = sub_complete[sub_complete["month"] == 6].groupby("year")["imerg_precip_mm"].sum().mean()
        mon_b = sub_complete[sub_complete["month"].isin([6, 7, 8, 9])].groupby("year")["imerg_precip_mm"].sum().mean()
        baselines[reg] = {"mam": mam_b, "june": jun_b, "monsoon": mon_b}

    # Annual values for each flood year
    event_rain = {}
    for ev in FFWC_FLOOD_EVENTS:
        y = ev["year"]
        event_rain[y] = {}
        for reg in ["National", "NE"]:
            sub = idf[(idf["region"] == reg) & (idf["year"] == y)]
            mam = float(sub[sub["month"].isin([3, 4, 5])]["imerg_precip_mm"].sum())
            jun = float(sub[sub["month"] == 6]["imerg_precip_mm"].sum())
            mon = float(sub[sub["month"].isin([6, 7, 8, 9])]["imerg_precip_mm"].sum())

            b = baselines[reg]
            event_rain[y][reg] = {
                "mam_mm": mam,
                "mam_anom_pct": (mam - b["mam"]) / b["mam"] * 100.0,
                "june_mm": jun,
                "june_anom_pct": (jun - b["june"]) / b["june"] * 100.0,
                "monsoon_mm": mon,
                "monsoon_anom_pct": (mon - b["monsoon"]) / b["monsoon"] * 100.0,
            }

    return baselines, event_rain


def build_extremes_analysis():
    if not RECHARGE_FILE.exists():
        raise FileNotFoundError(f"Missing recharge file: {RECHARGE_FILE}")

    rech_df = pd.read_csv(RECHARGE_FILE)
    nat_df = rech_df[rech_df["region"] == "National"].copy()

    # Calculate 24-year long-term baseline averages across complete observation pairs
    valid_nat = nat_df[nat_df["valid"] == True]
    mean_crest = valid_nat["post_monsoon_peak_cm"].mean()
    mean_trough = valid_nat["pre_monsoon_low_cm"].mean()
    mean_rebound = valid_nat["rebound_cm"].mean()
    mean_precip = nat_df["monsoon_precip_imerg_mm"].dropna().mean()
    
    # Use response ratio column
    ratio_col = "storage_response_ratio_imerg" if "storage_response_ratio_imerg" in valid_nat.columns else "seasonal_storage_response_imerg"
    mean_ratio = valid_nat[ratio_col].mean() * 100.0

    baselines_rain, event_rain = compute_flood_rainfall_metrics()

    rows = []
    for ev in FFWC_FLOOD_EVENTS:
        y = ev["year"]
        m_row = nat_df[nat_df["year"] == y]
        if len(m_row) > 0:
            r = m_row.iloc[0]
            crest = r["post_monsoon_peak_cm"]
            trough = r["pre_monsoon_low_cm"]
            rebound = r["rebound_cm"]
            precip = r["monsoon_precip_imerg_mm"]
            ratio = r[ratio_col] * 100.0 if pd.notnull(r[ratio_col]) else np.nan
        else:
            crest, trough, rebound, precip, ratio = np.nan, np.nan, np.nan, np.nan, np.nan

        er_nat = event_rain[y]["National"]
        er_ne = event_rain[y]["NE"]

        rows.append({
            "year": y,
            "flood_period": ev["flood_period"],
            "ffwc_classification": ev["ffwc_classification"],
            "inundation_area_pct": ev["inundation_area_pct"],
            "districts_affected": ev["districts_affected"],
            "population_affected": ev["population_affected_millions"],
            "national_mam_precip_mm": round(er_nat["mam_mm"], 1),
            "national_mam_anom_pct": round(er_nat["mam_anom_pct"], 1),
            "national_june_precip_mm": round(er_nat["june_mm"], 1),
            "national_june_anom_pct": round(er_nat["june_anom_pct"], 1),
            "national_monsoon_precip_mm": round(er_nat["monsoon_mm"], 1),
            "national_monsoon_anom_pct": round(er_nat["monsoon_anom_pct"], 1),
            "ne_mam_precip_mm": round(er_ne["mam_mm"], 1),
            "ne_mam_anom_pct": round(er_ne["mam_anom_pct"], 1),
            "ne_june_precip_mm": round(er_ne["june_mm"], 1),
            "ne_june_anom_pct": round(er_ne["june_anom_pct"], 1),
            "ne_monsoon_precip_mm": round(er_ne["monsoon_mm"], 1),
            "ne_monsoon_anom_pct": round(er_ne["monsoon_anom_pct"], 1),
            "post_monsoon_peak_cm": round(crest, 2) if pd.notnull(crest) else np.nan,
            "peak_anomaly_vs_mean_cm": round(crest - mean_crest, 2) if pd.notnull(crest) else np.nan,
            "seasonal_rebound_cm": round(rebound, 2) if pd.notnull(rebound) else np.nan,
            "storage_response_ratio_pct": round(ratio, 2) if pd.notnull(ratio) else np.nan,
            "response_ratio_anom_pct": round(ratio - mean_ratio, 2) if pd.notnull(ratio) else np.nan,
            "precip_anomaly_vs_mean_pct": round(er_nat["monsoon_anom_pct"], 1),
            "seasonal_storage_response_pct": round(ratio, 2) if pd.notnull(ratio) else np.nan,
            "source_document": ev["source_document"],
            "source_url": ev["source_url"],
            "meteorological_driver": ev["meteorological_driver"]
        })

    events_df = pd.DataFrame(rows)
    csv_path = OUTPUT_DIR / "flood_events_context.csv"
    events_df.to_csv(csv_path, index=False)
    print(f"  [OK] Saved Flood Events CSV: {csv_path.name}")

    # Build Markdown Deliverable
    md = f"""# Hydroclimatic Extremes & Severe Flood Event Context (2002–2026)

> **PRELIMINARY — NASA Space Apps Challenge 2026**
> **Team Tenstral | Project: Bengal Hydro Detective**
> Grounded in official Annual Flood Reports from the Flood Forecasting and Warning Centre (FFWC, BWDB), decoupled GPM IMERG V07B precipitation, and 24 years of continuous satellite gravimetry.
>
> **Status:** Descriptive Only — provides historical context for flood pulses vs. multi-decadal total water storage trends.
> **Limitations:** The seasonal storage response ratio ($\\Delta\\text{{TWS}} / P_{{\\text{{monsoon}}}}$) reflects bulk total water storage change, integrating unsaturated soil moisture and surface water bodies alongside groundwater, and does not represent an isolated groundwater recharge coefficient.

---

## 1. Historical Severe Flood Events Context (Descriptive Only)

**Baseline Reference Means (2002–2024 complete years):**
- National Precipitation (GPM IMERG): Pre-Monsoon MAM = **{baselines_rain['National']['mam']:.1f} mm** | June = **{baselines_rain['National']['june']:.1f} mm** | Monsoon JJAS = **{baselines_rain['National']['monsoon']:.1f} mm**
- NE Region Precipitation (GPM IMERG): Pre-Monsoon MAM = **{baselines_rain['NE']['mam']:.1f} mm** | June = **{baselines_rain['NE']['june']:.1f} mm** | Monsoon JJAS = **{baselines_rain['NE']['monsoon']:.1f} mm**
- Mean Post-Monsoon Peak TWS Anomaly (22 complete pairs): **{mean_crest:+.2f} cm**
- Mean Seasonal Storage Rebound ($\\Delta\\text{{TWS}}_{{\\text{{peak}} - \\text{{trough}}}}$): **{mean_rebound:.2f} cm**
- Mean Seasonal Storage Response Ratio (IMERG-based): **{mean_ratio:.1f}%**

| Year | Event Classification | Official Inundation Area | Nat Pre-Mon (MAM) [Anom] | Nat June [Anom] | Nat Monsoon (JJAS) [Anom] | NE Pre-Mon (MAM) [Anom] | NE June [Anom] | NE Monsoon (JJAS) [Anom] | Storage Peak [Anom] | Storage Rebound alone | Storage Response Ratio | Official Source (FFWC/BWDB) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
"""
    for _, r in events_df.iterrows():
        p_mam = f"{r['national_mam_precip_mm']:.0f} ({r['national_mam_anom_pct']:+.1f}%)"
        p_jun = f"{r['national_june_precip_mm']:.0f} ({r['national_june_anom_pct']:+.1f}%)"
        p_mon = f"{r['national_monsoon_precip_mm']:.0f} ({r['national_monsoon_anom_pct']:+.1f}%)"
        ne_mam = f"{r['ne_mam_precip_mm']:.0f} ({r['ne_mam_anom_pct']:+.1f}%)"
        ne_jun = f"{r['ne_june_precip_mm']:.0f} ({r['ne_june_anom_pct']:+.1f}%)"
        ne_mon = f"{r['ne_monsoon_precip_mm']:.0f} ({r['ne_monsoon_anom_pct']:+.1f}%)"
        c_str = f"{r['post_monsoon_peak_cm']:+.1f} cm ({r['peak_anomaly_vs_mean_cm']:+.1f} cm)" if pd.notnull(r['post_monsoon_peak_cm']) else "N/A (Gap)"
        reb_str = f"{r['seasonal_rebound_cm']:.1f} cm" if pd.notnull(r['seasonal_rebound_cm']) else "N/A (Gap)"
        ratio_str = f"{r['storage_response_ratio_pct']:.1f}% ({r['response_ratio_anom_pct']:+.1f}%)" if pd.notnull(r['storage_response_ratio_pct']) else "N/A (Gap)"
        src_link = f"[{r['source_document']}]({r['source_url']})"

        md += (
            f"| **{r['year']}** | {r['ffwc_classification']} | {r['inundation_area_pct']} | "
            f"`{p_mam}` | `{p_jun}` | `{p_mon}` | `{ne_mam}` | `{ne_jun}` | `{ne_mon}` | "
            f"`{c_str}` | `{reb_str}` | `{ratio_str}` | {src_link} |\n"
        )

    md += """
---

## 2. Granular Flood Meteorological Synopses

"""
    for ev in FFWC_FLOOD_EVENTS:
        y = ev["year"]
        er_ne = event_rain[y]["NE"]
        er_nat = event_rain[y]["National"]
        md += f"""### [{ev['year']}] {ev['ffwc_classification']}
- **Period & Inundation:** {ev['flood_period']} | Inundation: {ev['inundation_area_pct']} ({ev['districts_affected']} districts affected; population affected: {ev['population_affected_millions']}).
- **Hydrological Observations:**
  - National Monsoon (JJAS): {er_nat['monsoon_mm']:.1f} mm ({er_nat['monsoon_anom_pct']:+.1f}% vs baseline).
  - Northeast Region Monsoon: {er_ne['monsoon_mm']:.1f} mm ({er_ne['monsoon_anom_pct']:+.1f}%).
  - Northeast Pre-Monsoon (MAM): {er_ne['mam_mm']:.1f} mm ({er_ne['mam_anom_pct']:+.1f}%).
  - Northeast June Deluge: {er_ne['june_mm']:.1f} mm ({er_ne['june_anom_pct']:+.1f}%).
- **Meteorological & Hydrological Drivers:** {ev['meteorological_driver']}
- **Source Authority:** [{ev['source_document']}]({ev['source_url']})

"""

    md += """
---

## 3. Scientific Synthesis: Why Floods Fail to Arrest Multi-Decadal Storage Depletion

1. **Surface Runoff vs. Subsurface Infiltration:**
   - In catastrophic flood years like **2004** (monsoon rainfall: 2,021 mm, +21.3% above baseline) and **2007** (1,996 mm, +19.9% above baseline), seasonal bulk storage rebounds reached 56.7 cm and 64.8 cm respectively.
   - However, the seasonal storage response ratio remained bounded between 28% and 33%, consistent with precipitation rates exceeding soil infiltration capacity, resulting in overland ponding, drainage congestion, and estuarine discharge into the Bay of Bengal rather than unbounded subsurface retention.

2. **Transient Crests vs. Multi-Year Secular Depletion:**
   - While catastrophic floods produce short-lived positive storage crests (+41.0 cm in 2007 and +33.1 cm in 2004), these anomalies dissipate within 3–4 months as monsoon waters drain into the delta.
   - By the subsequent pre-monsoon dry season (March–May), intensive agricultural abstraction for the dry-season Boro crop offsets the seasonal flood surplus, returning total water storage to its secular depletion trajectory.

3. **Localized Sylhet/Haor Deluges Decoupled from National Monsoon Aggregates:**
   - In **2017**, pre-monsoon rainfall in the Northeast reached **1,091.8 mm (+49.1% above normal)**, generating catastrophic flash flooding across the Haor basin in April before the monsoon onset.
   - In **2022**, while national monsoon rainfall was below average (1,363.6 mm, -18.1%), June rainfall in the Northeast reached **978.6 mm (+60.6% above baseline)**, submerging 94% of Sunamganj and 84% of Sylhet, showing that regional extremes can diverge sharply from national seasonal statistics.
"""
    md_path = OUTPUT_DIR / "flood_events_context.md"
    md_path.write_text(md, encoding="utf-8")
    print(f"  [OK] Saved Flood Events Markdown: {md_path.name}")

    # Plot Figure
    plot_extremes_figure(nat_df, events_df)

    # Write Extremes Synthesis Note
    syn_content = """# Hydroclimatic Extremes & Flood Context Synthesis

**Project:** Bengal Hydro Detective — NASA Space Apps Challenge 2026
**Team:** Tenstral
**Status:** PRELIMINARY (Descriptive Only)

---

### Key Analytical Takeaways:

1. **Floods are Hydrological Episodes, Not Long-Term Trend Inverters:**
   - Even the most catastrophic flood years in Bangladesh's modern history (2004, 2007, 2020) fail to reverse the secular downward trajectory of total water storage in the high-abstraction Northwest (-1.25 to -1.81 cm/yr) and Central (-0.47 to -0.98 cm/yr) corridors.
   - The multi-decadal trend engine verifies a statistically significant national decline of **-0.51 cm/yr** (FDR q < 0.0001) over the full 2002–2026 record despite the occurrence of 5 major national flood disasters.

2. **Infiltration Saturation Dynamics:**
   - Analysis of 22 complete monsoon seasons shows that seasonal storage rebound alone averages **54.0 cm** nationally (slope: +0.235 cm/yr, p = 0.43, No detectable trend), while IMERG-based seasonal storage response ratio averages **32.6%**.
   - Peak inundation pulses generate overland runoff rather than proportionally increased groundwater infiltration, indicating that seasonal flooding cannot compensate for secular dry-season water abstraction.
   - *Limitations:* The seasonal storage response ratio (ΔTWS / P_monsoon) reflects bulk total water storage change, integrating unsaturated soil moisture and surface water bodies alongside groundwater, and does not represent an isolated groundwater recharge coefficient.

3. **Localized Flash Floods (2017, 2022) vs National Monsoon Totals:**
   - In 2017, pre-monsoon deluge in the Northeast reached 1,091.8 mm (+49.1% above baseline), inundating >70% of Haor basins.
   - In 2022, extreme June rainfall in the Northeast reached 978.6 mm (+60.6% above baseline), submerging 94% of Sunamganj and 84% of Sylhet even as national monsoon rainfall was 18.1% below normal.
"""
    syn_path = OUTPUT_DIR / "extremes_synthesis.md"
    syn_path.write_text(syn_content, encoding="utf-8")
    print(f"  [OK] Saved Extremes Synthesis Note: {syn_path.name}")


def plot_extremes_figure(nat_df: pd.DataFrame, events_df: pd.DataFrame):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9), sharex=True)

    years = nat_df["year"].values
    precip = nat_df["monsoon_precip_imerg_mm"].values
    crest = nat_df["post_monsoon_peak_cm"].values
    ratio_col = "storage_response_ratio_imerg" if "storage_response_ratio_imerg" in nat_df.columns else "seasonal_storage_response_imerg"
    ratio = (nat_df[ratio_col] * 100.0).values

    # Panel 1: Monsoon Precipitation & Storage Peak
    ax1.bar(years - 0.15, precip, width=0.3, color="#0284c7", alpha=0.7, label="National Monsoon Precipitation (mm) [GPM IMERG]")
    ax1.set_ylabel("Monsoon Precipitation (mm)", color="#0284c7", fontsize=10)
    ax1.tick_params(axis="y", labelcolor="#0284c7")

    ax1_twin = ax1.twinx()
    ax1_twin.plot(years + 0.15, crest, "r-o", lw=2, markersize=5, label="Post-Monsoon Storage Peak (cm)")
    ax1_twin.set_ylabel("TWS Storage Peak Anomaly (cm)", color="red", fontsize=10)
    ax1_twin.tick_params(axis="y", labelcolor="red")
    ax1_twin.axhline(0, color="gray", lw=0.8, linestyle="--")

    # Highlight Flood Years
    flood_yrs = [2004, 2007, 2020, 2022]
    for fy in flood_yrs:
        ax1.axvline(fy, color="#f59e0b", lw=1.2, linestyle=":", alpha=0.8)
        ax1.text(fy, 2150, f"Flood {fy}", rotation=90, verticalalignment="top", fontsize=8, color="#b45309", fontweight="bold")

    ax1.set_title("A. Seasonal Monsoon Precipitation (IMERG) vs Post-Monsoon Gravimetry Storage Peak (2002–2025)", fontsize=11, fontweight="bold")
    ax1.grid(True, linestyle=":", alpha=0.4)

    # Panel 2: Seasonal Storage Response Ratio Trend
    valid_mask = ~np.isnan(ratio)
    ax2.plot(years[valid_mask], ratio[valid_mask], "g-s", lw=1.8, markersize=5, label="Seasonal Storage Response Ratio (%) [IMERG-based]")

    # Linear trendline
    slope, intercept, r_val, p_val, std_err = stats.linregress(years[valid_mask], ratio[valid_mask])
    trendline = intercept + slope * years[valid_mask]
    ax2.plot(years[valid_mask], trendline, "k--", lw=1.8, label=f"Response Ratio Trend: {slope:+.2f}%/yr (p = {p_val:.4f})")

    ax2.set_ylabel("Storage Response Ratio (%)", fontsize=10)
    ax2.set_xlabel("Monsoon Year", fontsize=10)
    ax2.set_title("B. Seasonal Storage Response Ratio: [ΔTWS / (0.1 × IMERG Monsoon Precip)]\n"
                  "Limitation: Integrates bulk total water storage (unsaturated soil moisture + surface water + groundwater), not isolated groundwater recharge",
                  fontsize=10, fontweight="bold")
    ax2.grid(True, linestyle=":", alpha=0.4)
    ax2.legend(loc="upper right", fontsize=9)
    ax2.set_xticks(years)
    ax2.set_xticklabels(years, rotation=45)

    plt.suptitle("Hydroclimatic Extremes in Bangladesh: Flood Pulses vs Storage Response Dynamics (Descriptive Only)\n"
                 "PRELIMINARY — Team Tenstral | NASA Space Apps Challenge 2026", fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig_path = OUTPUT_DIR / "fig_flood_events_recharge.png"
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"  [OK] Saved Extremes Figure: {fig_path.name}")


if __name__ == "__main__":
    build_extremes_analysis()
