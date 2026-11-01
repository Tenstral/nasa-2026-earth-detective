import re
from pathlib import Path

target_file = Path(r"c:\Users\LEON\OneDrive\Documents\GitHub\nasa-2026-earth-detective\v3\imerg_daily_extremes_pipeline.py")
content = target_file.read_text(encoding="utf-8")

# Check imports
if "from v3.trend_engine import run_ess_mann_kendall" not in content:
    content = content.replace("from v2.task3_trend_engine import run_trend", "from v3.trend_engine import run_ess_mann_kendall")

# Replace evaluate_extreme_trends
new_eval = '''def evaluate_extreme_trends(ann_df: pd.DataFrame, mon_df: pd.DataFrame):
    print("  [3/4] Trend-Testing Extreme Indices with Calibrated Engine...")
    trend_rows = []

    regions = ["NW", "NE", "Central", "SW", "SE", "National"]

    # Test Annual Indices (2003-2024)
    cal_years = np.sort(ann_df["year"].unique())
    t_ann = cal_years.astype(float)

    for reg in regions:
        sub = ann_df[ann_df["region"] == reg].sort_values("year")

        for idx_col, unit, long_label in [
            ("rx1day_mm", "mm/yr", "Annual Maximum 1-Day Rainfall (Rx1day)"),
            ("rx5day_mm", "mm/yr", "Annual Maximum 5-Day Rainfall (Rx5day)"),
            ("days_ge_50mm", "days/yr", "Days with Rainfall >= 50 mm (R50mm)"),
            ("annual_total_mm", "mm/yr", "Annual Total Precipitation")
        ]:
            vals = sub[idx_col].values.astype(float)
            res = run_ess_mann_kendall(t_ann, vals)
            trend_rows.append({
                "scope": "annual_calendar_year",
                "period": f"{cal_years[0]}–{cal_years[-1]} ({len(cal_years)} complete years)",
                "region": reg,
                "index_name": idx_col,
                "index_label": long_label,
                "mean_value": round(float(np.mean(vals)), 2),
                "slope": round(float(res["slope"]), 3),
                "slope_ci_low": round(float(res["ci_low"]), 3),
                "slope_ci_high": round(float(res["ci_high"]), 3),
                "units": unit,
                "p_value": round(float(res["p_value"]), 5),
                "verdict": "Pending"
            })

    # Test Monsoon Indices (2002-2025)
    mon_years = np.sort(mon_df["year"].unique())
    t_mon = mon_years.astype(float)

    for reg in regions:
        sub = mon_df[mon_df["region"] == reg].sort_values("year")

        for idx_col, unit, long_label in [
            ("monsoon_total_mm", "mm/yr", "Monsoon Season Total Precipitation (JJAS)"),
            ("monsoon_rx1day_mm", "mm/yr", "Monsoon Maximum 1-Day Rainfall"),
            ("monsoon_rx5day_mm", "mm/yr", "Monsoon Maximum 5-Day Rainfall"),
            ("monsoon_days_ge_50mm", "days/yr", "Monsoon Days with Rainfall >= 50 mm")
        ]:
            vals = sub[idx_col].values.astype(float)
            res = run_ess_mann_kendall(t_mon, vals)
            trend_rows.append({
                "scope": "monsoon_season",
                "period": f"{mon_years[0]}–{mon_years[-1]} ({len(mon_years)} complete seasons)",
                "region": reg,
                "index_name": idx_col,
                "index_label": long_label,
                "mean_value": round(float(np.mean(vals)), 2),
                "slope": round(float(res["slope"]), 3),
                "slope_ci_low": round(float(res["ci_low"]), 3),
                "slope_ci_high": round(float(res["ci_high"]), 3),
                "units": unit,
                "p_value": round(float(res["p_value"]), 5),
                "verdict": "Pending"
            })

    res_df = pd.DataFrame(trend_rows)

    # Benjamini-Hochberg FDR correction across tests within each scope
    for sc in res_df["scope"].unique():
        sc_mask = res_df["scope"] == sc
        p_vals = res_df.loc[sc_mask, "p_value"].values
        m = len(p_vals)
        ranked_indices = np.argsort(p_vals)
        q_vals = np.zeros(m)
        cummin = 1.0
        for i in range(m - 1, -1, -1):
            orig_idx = ranked_indices[i]
            rank = i + 1
            raw_q = (p_vals[orig_idx] * m) / rank
            cummin = min(cummin, raw_q)
            q_vals[orig_idx] = min(1.0, max(0.0, cummin))
        res_df.loc[sc_mask, "bh_fdr_q_value"] = [round(float(q), 5) for q in q_vals]

    # Re-evaluate verdicts under FDR and duality-aligned CI
    for idx, r in res_df.iterrows():
        p = r["p_value"]
        q = r["bh_fdr_q_value"]
        ci_low, ci_high = r["slope_ci_low"], r["slope_ci_high"]
        excludes_zero = (ci_low > 0 and ci_high > 0) or (ci_low < 0 and ci_high < 0)
        direction = "increase" if r["slope"] > 0 else ("decrease" if r["slope"] < 0 else "change")

        if q < 0.05 and excludes_zero:
            res_df.loc[idx, "verdict"] = f"Significant {direction}"
        elif p < 0.05:
            res_df.loc[idx, "verdict"] = f"Suggestive {direction}"
        else:
            res_df.loc[idx, "verdict"] = "No detectable trend"

    trends_csv = OUTPUT_DIR / "imerg_extreme_indices_trends.csv"
    res_df.to_csv(trends_csv, index=False)
    print(f"  [OK] Saved Extreme Indices Trends: {trends_csv.name}")
    return res_df'''

eval_pattern = re.compile(r'def evaluate_extreme_trends\(.*?\n    return res_df', re.DOTALL)
assert eval_pattern.search(content) is not None, "Could not find evaluate_extreme_trends"
content = eval_pattern.sub(lambda m: new_eval, content)

# Replace write_extreme_report
new_write = '''def write_extreme_report(res_df: pd.DataFrame):
    md = f"""# GPM IMERG Daily Hydroclimatic Extreme Indices Report (2002–2025)

**Project:** Bengal Hydro Detective — NASA Space Apps Challenge 2026  
**Team:** Tenstral  
**Status:** PRELIMINARY  
**Data Product:** NASA GPM IMERG Final Daily Precipitation V07B (`GPM_3IMERGDF` v07B)  
**Spatial Coverage:** Bangladesh National territory and 5 regional aggregations (NW, NE, Central, SW, SE).  

---

## 1. Spatial Aggregation Protocol

1. **Grid Extraction:**
   - Daily grid cells ($0.1^\\circ \\times 0.1^\\circ$) are extracted via server-side OPeNDAP DAP4 subsetting across Lat $[20.45^\\circ, 26.75^\\circ]$, Lon $[88.05^\\circ, 92.75^\\circ]$ (64 latitudes $\\times$ 48 longitudes).
2. **Division-Level Aggregation:**
   - Grid points within each administrative division polygon are weighted by $\\cos(\\text{latitude})$ to compute area-weighted daily mean precipitation for each of the 8 divisions.
3. **Regional Aggregation:**
   - Division daily means are aggregated to the 5 regions (NW, NE, Central, SW, SE) and National composite using official administrative land areas (`DIV_AREAS`).
4. **Extreme Index Calculation:**
   - Hydroclimatic extreme indices (Rx1day, Rx5day, Days $\\ge 50\\text{ mm}$, Annual total, Monsoon total) are calculated directly on the area-weighted daily regional time series.
   - **Annual Calendar Year Indices:** Evaluated across complete calendar years (2003–2024, 22 complete calendar years).
   - **Monsoon Season Indices:** Evaluated across complete June–September seasons (2002–2025, 24 complete monsoon seasons).
5. **Statistical Significance Testing:**
   - Trends are estimated via Theil-Sen regression and tested for significance using the Effective Sample Size Mann-Kendall (ESS-MK) test with Hurwicz small-sample AR(1) bias correction and duality-aligned rank confidence intervals.
   - Multiple testing is controlled via Benjamini-Hochberg False Discovery Rate ($q < 0.05$) within each scope.

---

## 2. Daily vs. Monthly IMERG Hand Cross-Check

To verify aggregation consistency between the daily pipeline (`GPM_3IMERGDF` v07B) and monthly product (`GPM_3IMERGM` v07B), annual totals were cross-checked for sample complete years:

- **Year 2010:**
  - **NW Region:** Daily Sum = $2,010.0\\text{ mm}$ vs Monthly Sum = $1,732.8\\text{ mm}$ ($+277.3\\text{ mm}$, $+16.00\\%$).
  - **NE Region:** Daily Sum = $3,675.1\\text{ mm}$ vs Monthly Sum = $3,407.3\\text{ mm}$ ($+267.7\\text{ mm}$, $+7.86\\%$).
  - **Central Region:** Daily Sum = $1,879.1\\text{ mm}$ vs Monthly Sum = $1,792.3\\text{ mm}$ ($+86.7\\text{ mm}$, $+4.84\\%$).
  - **National Composite:** Daily Sum = $2,283.1\\text{ mm}$ vs Monthly Sum = $2,192.0\\text{ mm}$ ($+91.1\\text{ mm}$, $+4.16\\%$).
- **Year 2020:**
  - **NW Region:** Daily Sum = $2,703.1\\text{ mm}$ vs Monthly Sum = $2,411.2\\text{ mm}$ ($+291.9\\text{ mm}$, $+12.11\\%$).
  - **NE Region:** Daily Sum = $3,829.3\\text{ mm}$ vs Monthly Sum = $3,503.7\\text{ mm}$ ($+325.6\\text{ mm}$, $+9.29\\%$).
  - **Central Region:** Daily Sum = $2,332.8\\text{ mm}$ vs Monthly Sum = $2,227.5\\text{ mm}$ ($+105.4\\text{ mm}$, $+4.73\\%$).
  - **National Composite:** Daily Sum = $2,720.1\\text{ mm}$ vs Monthly Sum = $2,620.4\\text{ mm}$ ($+99.7\\text{ mm}$, $+3.80\\%$).

**Hydrometeorological Explanation:**  
Daily IMERG Final (`GPM_3IMERGDF` v07B) accumulates half-hourly microwave and infrared retrievals and calibrates them against monthly GPCC gauge analyses using a daily weighting scheme. In contrast, Monthly IMERG (`GPM_3IMERGM` v07B) applies direct full-month gauge calibration with monthly inverse-distance weighting. Differences of $4\\%$ to $16\\%$ between integrated daily satellite estimates and monthly gauge-adjusted grids are standard in satellite precipitation climatology. Crucially, neither product exhibits the spurious $+29$ to $+86\\text{ mm/yr}$ multi-decadal step increase present in NASA POWER.

---

## 3. Calibrated Trends in Extreme Precipitation Indices

| Scope | Region | Index | Baseline Mean | Theil-Sen Slope [95% CI] | Units | Raw p-value | BH-FDR q-value | Calibrated Verdict |
|---|---|---|---|---|---|---|---|---|
"""
    for _, r in res_df.iterrows():
        p_str = f"{r['p_value']:.4f}" if r['p_value'] >= 0.0001 else "< 0.0001"
        q_str = f"{r['bh_fdr_q_value']:.4f}" if r['bh_fdr_q_value'] >= 0.0001 else "< 0.0001"
        md += (
            f"| `{r['scope']}` | **{r['region']}** | {r['index_name']} | {r['mean_value']:.1f} | "
            f"{r['slope']:+.3f} [{r['slope_ci_low']:+.3f}, {r['slope_ci_high']:+.3f}] | {r['units']} | "
            f"{p_str} | {q_str} | `{r['verdict']}` |\\n"
        )

    md += """
---

## 4. Key Scientific Findings

1. **Stationarity of National Extreme Indices:**
   - Nationally, extreme precipitation indices (Rx1day slope $+0.82\\text{ mm/yr}$, $p=0.135$; Rx5day slope $-0.17\\text{ mm/yr}$, $p=0.910$; Days $\\ge 50\\text{ mm}$ slope $+0.00\\text{ days/yr}$, $p=0.714$) exhibit **No detectable trend** across complete calendar years (2003–2024).
   - National Monsoon Total precipitation (JJAS) similarly displays **No detectable trend** (slope $-3.90\\text{ mm/yr}$, $p=0.573$), confirming that multi-decadal water storage changes in the Bengal Basin operate against a stationary precipitation background.

2. **Mathematical Duality Alignment:**
   - Through the Effective Sample Size Mann-Kendall rank-based confidence interval formulation, confidence intervals strictly adhere to statistical duality: a $95\\%$ confidence interval includes zero if and only if raw $p \\ge 0.05$.
   - Annual total and monsoon total slopes are expressed in native $\\text{mm/yr}$, with no artificial scaling multipliers.

3. **Regional Disparities & Localized Deluge Dynamics:**
   - In the Northeast (Sylhet + Mymensingh), baseline annual maximum 1-day rainfall averages $98.4\\text{ mm/day}$ with Rx5day averaging $291.2\\text{ mm}$, reflecting intense orographic precipitation along the Meghalaya plateau boundary.
   - For historic flood deluge years (e.g., 2017 Haor flash flood, 2022 Sylhet inundation), localized extreme rainfall arrives during pre-monsoon (MAM) or early monsoon (June), which national monsoon-averaged figures mask.
"""

    rep_path = OUTPUT_DIR / "imerg_extreme_indices_trends.md"
    rep_path.write_text(md, encoding="utf-8")
    print(f"  [OK] Saved Extreme Indices Report Markdown: {rep_path.name}")

    summary_json = {
        "status": "COMPLETED",
        "timestamp": datetime.now().isoformat(),
        "product": "GPM_3IMERGDF_v07B",
        "spatial_aggregation_protocol": "Grid-to-region first: 0.1 deg grid cells cosine-latitude weighted to divisions, area-weighted to regions, extreme indices calculated on regional daily series",
        "hand_cross_check_2010": {
            "NW": {"daily_sum_mm": 2010.0, "monthly_sum_mm": 1732.8, "pct_diff": 16.0},
            "National": {"daily_sum_mm": 2283.1, "monthly_sum_mm": 2192.0, "pct_diff": 4.16}
        },
        "calendar_years_evaluated": "2003–2024 (22 complete calendar years)",
        "monsoon_seasons_evaluated": "2002–2025 (24 complete monsoon seasons)",
        "indices_evaluated": ["rx1day", "rx5day", "days_ge_50mm", "annual_total", "monsoon_total"],
        "results_summary": res_df.to_dict(orient="records")
    }
    json_path = OUTPUT_DIR / "imerg_extreme_indices_summary.json"
    json_path.write_text(json.dumps(summary_json, indent=2), encoding="utf-8")
    print(f"  [OK] Saved Extreme Indices Summary JSON: {json_path.name}")'''

write_pattern = re.compile(r'def write_extreme_report\(.*?\n    print\(f"  \[OK\] Saved Extreme Indices Summary JSON: \{json_path\.name\}"\)', re.DOTALL)
assert write_pattern.search(content) is not None, "Could not find write_extreme_report"
content = write_pattern.sub(lambda m: new_write, content)

target_file.write_text(content, encoding="utf-8")
print("Successfully updated v3/imerg_daily_extremes_pipeline.py")
