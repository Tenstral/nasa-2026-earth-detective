"""
Script to update Section 9 of PROJECT_STATUS.md programmatically from exploratory CSVs.
"""

from pathlib import Path
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
STATUS_FILE = REPO_ROOT / "PROJECT_STATUS.md"
RATIO_CSV = REPO_ROOT / "outputs" / "v3" / "seasonal" / "ratio_trend.csv"
DRAWDOWN_CSV = REPO_ROOT / "outputs" / "v3" / "seasonal" / "dry_season_drawdown.csv"


def update_project_status():
    r_df = pd.read_csv(RATIO_CSV)
    dd_df = pd.read_csv(DRAWDOWN_CSV)

    r_main = r_df[r_df["analysis_type"] == "main_run"].set_index("region")
    dd_main = dd_df[dd_df["analysis_type"] == "main_run"].set_index("region")

    with open(STATUS_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    # Fix earlier occurrences of stationary
    text = text.replace(
        "- **Stationary Extreme Indices:** Daily precipitation extremes (Rx1day, Rx5day, days $\\ge 50\\text{ mm}$, and annual total for 2003–2024; monsoon total, monsoon Rx1day, monsoon Rx5day, and monsoon days $\\ge 50\\text{ mm}$ for 2002–2025) show no statistically significant trend across Bangladesh.",
        "- **No Detectable Trend in Extreme Indices:** Daily precipitation extremes (Rx1day, Rx5day, days $\\ge 50\\text{ mm}$, and annual total for 2003–2024; monsoon total, monsoon Rx1day, monsoon Rx5day, and monsoon days $\\ge 50\\text{ mm}$ for 2002–2025) show no detectable trend across Bangladesh."
    )
    text = text.replace(
        "- `outputs/v3/extremes/fig_imerg_extreme_indices_trends.png`: Multi-index time series showing stationary daily extreme precipitation.",
        "- `outputs/v3/extremes/fig_imerg_extreme_indices_trends.png`: Multi-index time series showing daily extreme precipitation with no detectable trend."
    )

    # Truncate before Section 9
    sec9_marker = "## 9. Exploratory Seasonal Storage Response & Dry-Season Drawdown (Preliminary)"
    idx = text.find(sec9_marker)
    if idx != -1:
        dash_idx = text.rfind("---", 0, idx)
        base_text = text[:dash_idx].rstrip() + "\n\n---\n\n"
    else:
        base_text = text.rstrip() + "\n\n---\n\n"

    # Build Section 9 dynamically
    lines = [
        "## 9. Exploratory Seasonal Storage Response & Dry-Season Drawdown (Preliminary)",
        "",
        "> **Status Label:** PRELIMINARY & EXPLORATORY ONLY.  ",
        "> These supplementary analyses test seasonal storage dynamics across multi-decadal observations. To maintain strict statistical governance, all exploratory results are documented separately in `outputs/v3/seasonal/` and quarantined from the headline 336-test master table (`results_all_windows.csv`).",
        "",
        "### A. Trend of Seasonal Storage Response Ratio (2002–2025)",
        "",
        "1. **Physical Metric & Data Sources:**",
        "   - Evaluates the multi-decadal stability of the seasonal storage response ratio, defined as:",
        r"     $$\text{Seasonal Storage Response Ratio} = \frac{\Delta\text{TWS}\text{ (cm)}}{0.1 \times P_{\text{monsoon}}\text{ (mm)}} \times 100\%$$",
        r"   - **Numerator ($\Delta\text{TWS}$):** Seasonal storage rebound alone, defined as the post-monsoon storage peak (maximum of August–November) minus the pre-monsoon dry season low (minimum of March–May) from CSR GRACE/GRACE-FO RL06.3 gravimetry (cm of total water storage).",
        r"   - **Denominator ($P_{\text{monsoon}}$):** June–September 4-month cumulative rainfall from NASA GPM IMERG V07B Final Run (converted to cm liquid water equivalent).",
        "2. **Satellite Gap Protocol:**",
        "   - Incomplete seasons are dropped directly rather than interpolated. The 2017 season (lacking post-monsoon peak due to GRACE decommissioning) and 2018 season (lacking pre-monsoon low prior to GRACE-FO operations) are excluded, leaving **22 complete seasons** (2002–2016 and 2019–2025) in the main run.",
        r"   - A sensitivity run further excludes seasons within $\pm 6$ months of the satellite mission transition (2016–2019), leaving **20 complete seasons**.",
        "3. **Statistical Findings (Main Run, N = 22 Seasons):**",
    ]

    for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
        row = r_main.loc[reg]
        reg_name = row["region_name"]
        mean_r = row["mean_ratio_pct"]
        slope = row["slope_pct_yr"]
        ci_low = row["slope_ci_low_pct_yr"]
        ci_high = row["slope_ci_high_pct_yr"]
        p_val = row["p_value"]
        q_val = row["exploratory_fdr_q"]
        mds = row["mds_80pct_power_pct_yr"]
        verdict = row["verdict"]
        ci_note = " (CI is wide relative to slope and spans zero)" if (ci_low < 0 < ci_high) else ""
        if verdict == "Suggestive":
            verdict_str = f"**Suggestive** (raw $p < 0.05$ does not survive exploratory Benjamini-Hochberg FDR control $q = {q_val:.4f} \\ge 0.05$)"
        elif verdict == "Exploratory: trend detected":
            verdict_str = f"**Exploratory: trend detected** ($p = {p_val:.4f}, q = {q_val:.4f}$)"
        else:
            verdict_str = f"**No detectable trend**{ci_note}"

        lines.append(
            f"   - **{reg}** ({reg_name}): Mean ratio = {mean_r:.1f}%, Theil-Sen slope = **{slope:+.3f} %/yr**, 95% CI: `[{ci_low:+.3f}, {ci_high:+.3f}] %/yr`, $p = {p_val:.4f}$, exploratory FDR $q = {q_val:.4f}$, MDS (80% power) = {mds:.3f} %/yr $\\rightarrow$ {verdict_str}."
        )

    lines += [
        "4. **Sensitivity Run (Transition-Buffer Excluded, N = 20 Seasons):**",
        "   - In the sensitivity run that drops seasons within ±6 months of the GRACE to GRACE-FO transition (20 seasons), Central and National pass exploratory FDR control (Central: slope +0.476 %/yr, $p = 0.0048$, $q = 0.0212$; National: slope +0.151 %/yr, $p = 0.0071$, $q = 0.0212$), while NW, NE, SW, and SE show no detectable trend. The result therefore depends on whether the 2016 and 2019 seasons are included and should be treated as fragile and exploratory.",
        "   - A positive ratio slope means the monsoon storage rebound per mm of rain has not weakened; it does not mean recharge is improving.",
        "",
        "---",
        "",
        "### B. Dry-Season Storage Drawdown & Cropland Overlay (2002–2026)",
        "",
        "1. **Physical Metric & Exact Config Windows:**",
        "   - Evaluates whether the annual dry-season storage drawdown has expanded or contracted over the 24-year satellite record:",
        r"     $$\text{Drawdown}_{y} = \text{TWS}_{\text{peak}, y} - \text{TWS}_{\text{min}, y+1}$$",
        "   - Exact observation windows specified in `config.json` constants:",
        "     - `monsoon_peak_months`: `[8, 9, 10, 11]` (August–November of year $y$)",
        "     - `following_pre_monsoon_min_months`: `[3, 4, 5]` (March–May of following year $y+1$)",
        "2. **Missing Satellite Endpoint Protocol:**",
        "   - Any annual cycle missing either endpoint is dropped rather than interpolated. The 2017–2018 cycle lacks both autumn 2017 peak and spring 2018 low due to the GRACE to GRACE-FO transition gap; exactly **1 year (2017)** drops out per region, leaving **23 valid observation cycles** (2002–2016 and 2018–2025) in the main run.",
        r"   - Sensitivity run excludes cycles touching the $\pm 6$-month buffer (2016–2018), leaving **21 valid cycles**.",
        "3. **Statistical Trends & Descriptive Cropland Overlay:**",
        "   - To prevent ecological fallacy and spurious regression across an aggregated sample of 5 regions ($N=5$), no cross-regional correlation or regression is performed. Regional metrics are reported descriptively alongside agricultural land cover (MODIS MCD12Q1) and population (NASA SEDAC GPWv4):",
        "",
        "| Region | Cropland (%) | Population (2020) | Full-Record TWS Slope (cm/yr) | Full-Record TWS 95% CI | Mean Drawdown (cm) | Drawdown Slope (cm/yr) | 95% Confidence Interval | p-value | Exploratory FDR q | MDS (80% Power) | Verdict |",
        "|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|",
    ]

    for reg in ["NW", "NE", "Central", "SW", "SE", "National"]:
        row = dd_main.loc[reg]
        crop = row["cropland_pct_mcd12q1"]
        pop = row["pop_millions_2020"]
        tws_s = row["secular_tws_slope_cm_yr"]
        tws_ci = row["secular_tws_ci_95"]
        mean_dd = row["mean_drawdown_cm"]
        dd_s = row["drawdown_slope_cm_yr"]
        ci_low = row["drawdown_ci_low_cm_yr"]
        ci_high = row["drawdown_ci_high_cm_yr"]
        p_val = row["p_value"]
        q_val = row["exploratory_fdr_q"]
        mds = row["mds_80pct_power_cm_yr"]
        verdict = row["verdict"]

        pop_str = f"{pop:.2f}M" if pd.notna(pop) else "—"
        lines.append(
            f"| **{reg}** | {crop:.1f}% | {pop_str} | {tws_s:.2f} | {tws_ci} | {mean_dd:.2f} cm | **{dd_s:+.3f}** | [{ci_low:+.3f}, {ci_high:+.3f}] | {p_val:.4f} | {q_val:.4f} | {mds:.3f} cm/yr | {verdict} |"
        )

    lines += [
        "",
        "4. **Physical Interpretation:**",
        "   - In all 5 regions and nationally, the annual dry-season drawdown trend shows **no detectable trend** (all $p \\ge 0.50$, all exploratory $q = 1.00$ in the main run).",
        "   - No detectable change in seasonal amplitude (drawdown slope CIs about ±0.9 cm/yr in NW); the baseline total water storage declines (-1.25 cm/yr in NW). A change smaller than the detection limit is not ruled out.",
        "",
        "5. **Methodological Limits & Scope:**",
        "   > Gravimetry measures total water storage (groundwater, soil moisture and surface water together). This analysis shows regional patterns that are consistent with dry-season agricultural water use but does not attribute them to irrigation pumping. Testing that would require metered pumping or electricity records (BMDA), BWDB well hydrographs, or irrigated-area mapping.",
        ""
    ]

    new_content = base_text + "\n".join(lines)

    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("Successfully updated PROJECT_STATUS.md from exploratory CSVs!")


if __name__ == "__main__":
    update_project_status()
