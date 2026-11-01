import re
from pathlib import Path

target_file = Path("v3/gldas_multi_model_processor.py")
content = target_file.read_text(encoding="utf-8")

# 1. Update build_multi_model_regional_series
old_ens = '''        # Ensemble mean & spread across models
        sub["multi_model_sms_mean_cm"] = sub[["noah_sms_anom_cm", "vic_sms_anom_cm", "clsm_sms_anom_cm"]].mean(axis=1)
        sub["multi_model_sms_std_cm"] = sub[["noah_sms_anom_cm", "vic_sms_anom_cm", "clsm_sms_anom_cm"]].std(axis=1)
        sub["multi_model_sms_min_cm"] = sub[["noah_sms_anom_cm", "vic_sms_anom_cm", "clsm_sms_anom_cm"]].min(axis=1)
        sub["multi_model_sms_max_cm"] = sub[["noah_sms_anom_cm", "vic_sms_anom_cm", "clsm_sms_anom_cm"]].max(axis=1)'''

new_ens = '''        # Independent models (Noah 2.1 + VIC 2.1)
        sub["independent_sms_mean_cm"] = sub[["noah_sms_anom_cm", "vic_sms_anom_cm"]].mean(axis=1)
        sub["independent_sms_min_cm"] = sub[["noah_sms_anom_cm", "vic_sms_anom_cm"]].min(axis=1)
        sub["independent_sms_max_cm"] = sub[["noah_sms_anom_cm", "vic_sms_anom_cm"]].max(axis=1)

        # Multi-model ensemble (including CLSM for legacy comparison)
        sub["multi_model_sms_mean_cm"] = sub[["noah_sms_anom_cm", "vic_sms_anom_cm", "clsm_sms_anom_cm"]].mean(axis=1)
        sub["multi_model_sms_std_cm"] = sub[["noah_sms_anom_cm", "vic_sms_anom_cm", "clsm_sms_anom_cm"]].std(axis=1)
        sub["multi_model_sms_min_cm"] = sub[["noah_sms_anom_cm", "vic_sms_anom_cm", "clsm_sms_anom_cm"]].min(axis=1)
        sub["multi_model_sms_max_cm"] = sub[["noah_sms_anom_cm", "vic_sms_anom_cm", "clsm_sms_anom_cm"]].max(axis=1)'''

assert old_ens in content, "Could not find old_ens"
content = content.replace(old_ens, new_ens)

old_res = '''        # Compute Residuals: Residual = TWS - Delta SMS
        m_tws["noah_residual_cm"] = m_tws["grace_tws_cm"] - m_tws["noah_sms_anom_cm"]
        m_tws["vic_residual_cm"] = m_tws["grace_tws_cm"] - m_tws["vic_sms_anom_cm"]
        m_tws["clsm_residual_cm"] = m_tws["grace_tws_cm"] - m_tws["clsm_sms_anom_cm"]
        m_tws["multi_model_residual_cm"] = m_tws["grace_tws_cm"] - m_tws["multi_model_sms_mean_cm"]

        m_tws["residual_label"] = "groundwater + surface water + model error residual"
        m_tws["clsm_note"] = "Non-independent / GRACE-assimilated"'''

new_res = '''        # Compute Residuals: Residual = TWS - Delta SMS
        m_tws["noah_residual_cm"] = m_tws["grace_tws_cm"] - m_tws["noah_sms_anom_cm"]
        m_tws["vic_residual_cm"] = m_tws["grace_tws_cm"] - m_tws["vic_sms_anom_cm"]
        m_tws["clsm_residual_cm"] = m_tws["grace_tws_cm"] - m_tws["clsm_sms_anom_cm"]
        m_tws["independent_residual_min_cm"] = m_tws[["noah_residual_cm", "vic_residual_cm"]].min(axis=1)
        m_tws["independent_residual_max_cm"] = m_tws[["noah_residual_cm", "vic_residual_cm"]].max(axis=1)
        m_tws["multi_model_residual_cm"] = m_tws["grace_tws_cm"] - m_tws["multi_model_sms_mean_cm"]

        m_tws["residual_label"] = "groundwater + surface water + model error residual"
        m_tws["clsm_note"] = "Non-independent / GRACE-assimilated (cannot serve as independent partition)"'''

assert old_res in content, "Could not find old_res"
content = content.replace(old_res, new_res)

# 2. Update evaluate_multi_model_trends
old_trend_block = '''            results.append({
                "window": win_name,
                "region": reg,
                "n_obs_tws": len(sub),
                "tws_slope_cm_yr": round(float(res_tws["slope"]), 2),
                "tws_ci_low": round(float(res_tws["slope_ci_low"]), 2),
                "tws_ci_high": round(float(res_tws["slope_ci_high"]), 2),
                "tws_verdict": res_tws["verdict"],

                # Noah 2.1
                "noah_sms_slope": round(float(res_noah_sms["slope"]), 2),
                "noah_sms_p": round(float(res_noah_sms["p_value"]), 4),
                "noah_sms_verdict": res_noah_sms["verdict"],
                "noah_residual_slope": round(float(res_noah_res["slope"]), 2),
                "noah_residual_ci": f"[{round(float(res_noah_res['slope_ci_low']), 2):+.2f}, {round(float(res_noah_res['slope_ci_high']), 2):+.2f}]",
                "noah_residual_verdict": res_noah_res["verdict"],

                # VIC 2.1
                "vic_sms_slope": round(float(res_vic_sms["slope"]), 2),
                "vic_sms_p": round(float(res_vic_sms["p_value"]), 4),
                "vic_sms_verdict": res_vic_sms["verdict"],
                "vic_residual_slope": round(float(res_vic_res["slope"]), 2),
                "vic_residual_ci": f"[{round(float(res_vic_res['slope_ci_low']), 2):+.2f}, {round(float(res_vic_res['slope_ci_high']), 2):+.2f}]",
                "vic_residual_verdict": res_vic_res["verdict"],

                # CLSM 2.2 (Non-independent / GRACE-assimilated)
                "clsm_sms_slope": round(float(res_clsm_sms["slope"]), 2) if not np.isnan(float(res_clsm_sms["slope"])) else np.nan,
                "clsm_sms_p": round(float(res_clsm_sms["p_value"]), 4) if not np.isnan(float(res_clsm_sms["p_value"])) else np.nan,
                "clsm_sms_verdict": res_clsm_sms["verdict"],
                "clsm_residual_slope": round(float(res_clsm_res["slope"]), 2) if not np.isnan(float(res_clsm_res["slope"])) else np.nan,
                "clsm_residual_ci": f"[{round(float(res_clsm_res['slope_ci_low']), 2):+.2f}, {round(float(res_clsm_res['slope_ci_high']), 2):+.2f}]" if not np.isnan(float(res_clsm_res["slope"])) else "—",
                "clsm_residual_verdict": res_clsm_res["verdict"],
                "clsm_label": "Non-independent / GRACE-assimilated",

                # Multi-Model Ensemble
                "ensemble_sms_slope": round(float(res_ens_sms["slope"]), 2),
                "ensemble_sms_p": round(float(res_ens_sms["p_value"]), 4),
                "ensemble_sms_verdict": res_ens_sms["verdict"],
                "ensemble_residual_slope": round(float(res_ens_res["slope"]), 2),
                "ensemble_residual_ci": f"[{round(float(res_ens_res['slope_ci_low']), 2):+.2f}, {round(float(res_ens_res['slope_ci_high']), 2):+.2f}]",
                "ensemble_residual_verdict": res_ens_res["verdict"],
                "sms_slope_spread_cm_yr": round(sms_slope_spread, 2),
                "residual_label": "groundwater + surface water + model error residual"
            })'''

new_trend_block = '''            sms_min_slope = min(float(res_noah_sms["slope"]), float(res_vic_sms["slope"]))
            sms_max_slope = max(float(res_noah_sms["slope"]), float(res_vic_sms["slope"]))
            res_min_slope = min(float(res_noah_res["slope"]), float(res_vic_res["slope"]))
            res_max_slope = max(float(res_noah_res["slope"]), float(res_vic_res["slope"]))

            results.append({
                "window": win_name,
                "region": reg,
                "n_obs_tws": len(sub),
                "tws_slope_cm_yr": round(float(res_tws["slope"]), 2),
                "tws_ci_low": round(float(res_tws["slope_ci_low"]), 2),
                "tws_ci_high": round(float(res_tws["slope_ci_high"]), 2),
                "tws_verdict": res_tws["verdict"],

                # Noah 2.1 (Independent)
                "noah_sms_slope": round(float(res_noah_sms["slope"]), 2),
                "noah_sms_p": round(float(res_noah_sms["p_value"]), 4),
                "noah_sms_verdict": res_noah_sms["verdict"],
                "noah_residual_slope": round(float(res_noah_res["slope"]), 2),
                "noah_residual_ci": f"[{round(float(res_noah_res['slope_ci_low']), 2):+.2f}, {round(float(res_noah_res['slope_ci_high']), 2):+.2f}]",
                "noah_residual_verdict": res_noah_res["verdict"],

                # VIC 2.1 (Independent)
                "vic_sms_slope": round(float(res_vic_sms["slope"]), 2),
                "vic_sms_p": round(float(res_vic_sms["p_value"]), 4),
                "vic_sms_verdict": res_vic_sms["verdict"],
                "vic_residual_slope": round(float(res_vic_res["slope"]), 2),
                "vic_residual_ci": f"[{round(float(res_vic_res['slope_ci_low']), 2):+.2f}, {round(float(res_vic_res['slope_ci_high']), 2):+.2f}]",
                "vic_residual_verdict": res_vic_res["verdict"],

                # Independent Synthesis (Noah 2.1 + VIC 2.1)
                "independent_sms_slope_min": round(sms_min_slope, 2),
                "independent_sms_slope_max": round(sms_max_slope, 2),
                "independent_sms_range": f"[{sms_min_slope:+.2f}, {sms_max_slope:+.2f}]",
                "independent_residual_slope_min": round(res_min_slope, 2),
                "independent_residual_slope_max": round(res_max_slope, 2),
                "independent_residual_range": f"[{res_min_slope:+.2f}, {res_max_slope:+.2f}]",

                # CLSM 2.2 (Non-independent / GRACE-assimilated)
                "clsm_sms_slope": round(float(res_clsm_sms["slope"]), 2) if not np.isnan(float(res_clsm_sms["slope"])) else np.nan,
                "clsm_sms_p": round(float(res_clsm_sms["p_value"]), 4) if not np.isnan(float(res_clsm_sms["p_value"])) else np.nan,
                "clsm_sms_verdict": res_clsm_sms["verdict"],
                "clsm_residual_slope": round(float(res_clsm_res["slope"]), 2) if not np.isnan(float(res_clsm_res["slope"])) else np.nan,
                "clsm_residual_ci": f"[{round(float(res_clsm_res['slope_ci_low']), 2):+.2f}, {round(float(res_clsm_res['slope_ci_high']), 2):+.2f}]" if not np.isnan(float(res_clsm_res["slope"])) else "—",
                "clsm_residual_verdict": res_clsm_res["verdict"],
                "clsm_label": "Non-independent / GRACE-assimilated",
                "clsm_independence_note": "CLSM 2.2 assimilates GRACE observations via EnKF and cannot serve as an independent partition",

                # Multi-Model Ensemble
                "ensemble_sms_slope": round(float(res_ens_sms["slope"]), 2),
                "ensemble_sms_p": round(float(res_ens_sms["p_value"]), 4),
                "ensemble_sms_verdict": res_ens_sms["verdict"],
                "ensemble_residual_slope": round(float(res_ens_res["slope"]), 2),
                "ensemble_residual_ci": f"[{round(float(res_ens_res['slope_ci_low']), 2):+.2f}, {round(float(res_ens_res['slope_ci_high']), 2):+.2f}]",
                "ensemble_residual_verdict": res_ens_res["verdict"],
                "sms_slope_spread_cm_yr": round(sms_slope_spread, 2),
                "residual_label": "groundwater + surface water + model error residual"
            })'''

assert old_trend_block in content, "Could not find old_trend_block"
content = content.replace(old_trend_block, new_trend_block)

# 3. Update write_multi_model_report
old_report_func = re.compile(r'def write_multi_model_report\(res_df: pd\.DataFrame, hom_res: dict\):.*?\n    print\(f"  \[OK\] Saved Multi-Model Summary JSON: \{json_path\.name\}"\)', re.DOTALL)
assert old_report_func.search(content) is not None, "Could not find write_multi_model_report"

new_report_code = '''def write_multi_model_report(res_df: pd.DataFrame, hom_res: dict):
    # Extract Northwest statistics for grace_fo_era and full_record
    nw_fo = res_df[(res_df["region"] == "NW") & (res_df["window"] == "grace_fo_era")].iloc[0]
    nw_full = res_df[(res_df["region"] == "NW") & (res_df["window"] == "full_record")].iloc[0]

    md = f"""# GLDAS Multi-Model Soil-Moisture & Storage Partitioning Report

**Project:** Bengal Hydro Detective — NASA Space Apps Challenge 2026  
**Team:** Tenstral  
**Status:** PRELIMINARY  
**Primary Gravimetry:** CSR GRACE / GRACE-FO RL0603 Mascons (2002–2026)  
**Models Evaluated:**
1. **GLDAS-2.1 Noah Land Surface Model L4 monthly 0.25°** (`GLDAS_NOAH025_M` v2.1, **Independent**): $2.0\\text{{ m}}$ root-zone depth (4 layers: $0–10\\text{{ cm}}$, $10–40\\text{{ cm}}$, $40–100\\text{{ cm}}$, $100–200\\text{{ cm}}$) + Canopy + Snow.
2. **GLDAS-2.1 Variable Infiltration Capacity (VIC) L4 monthly 1.0°** (`GLDAS_VIC10_M` v2.1, **Independent**): 3 soil moisture layers + Canopy + Snow.
3. **GLDAS-2.2 Catchment Land Surface Model (CLSM) L4 daily 0.25°** (`GLDAS_CLSM025_DA1_D` v2.2, **Non-independent / GRACE-assimilated**): Profile soil moisture + Canopy + Snow (assimilates GRACE TWSA via EnKF; record starts 2003-02).
- **Reference Baseline:** All models re-baselined to 2004-01 to 2009-12 (mean anomaly $\\equiv 0.0\\text{{ cm}}$).
- **Residual Storage Definition:** $\\text{{Residual}} = \\text{{TWS}} - \\Delta\\text{{SMS}} - \\Delta\\text{{SWE}}$, strictly labeled as `groundwater + surface water + model error residual`.
- **Partitioning Principle:** Noah and VIC represent independent open-loop land surface physics. CLSM 2.2 assimilates GRACE observations directly, creating circularity if used to partition GRACE, and is therefore reported separately for diagnostic context only.

---

## 1. Multi-Model Partitioning Trends Across All 4 Operational Windows

| Window | Region | TWS Slope (cm/yr) | Noah ΔSMS Slope (cm/yr) | VIC ΔSMS Slope (cm/yr) | Independent ΔSMS Range [Min, Max] | Independent Residual Slope Range [Min, Max]* | CLSM ΔSMS Slope (cm/yr)** | CLSM Residual Slope (cm/yr)** |
|---|---|---|---|---|---|---|---|---|
"""
    for _, r in res_df.iterrows():
        clsm_sms_str = f"{r['clsm_sms_slope']:+.2f}" if pd.notna(r['clsm_sms_slope']) else "—"
        clsm_res_str = f"{r['clsm_residual_slope']:+.2f}" if pd.notna(r['clsm_residual_slope']) else "—"
        md += (
            f"| `{r['window']}` | **{r['region']}** | {r['tws_slope_cm_yr']:+.2f} | "
            f"{r['noah_sms_slope']:+.2f} (`{r['noah_sms_verdict']}`) | "
            f"{r['vic_sms_slope']:+.2f} (`{r['vic_sms_verdict']}`) | "
            f"{r['independent_sms_range']} | "
            f"{r['independent_residual_range']} | "
            f"{clsm_sms_str}** | "
            f"{clsm_res_str}** |\\n"
        )

    md += """
*\\*Note: Independent Residual is defined as TWS - ΔSMS across independent models (Noah 2.1 and VIC 2.1). Strictly labeled: `groundwater + surface water + model error residual`. Presented as a model range [min, max] across independent models, avoiding mixed physical and model confidence intervals.*  
*\\*\\*Note: GLDAS-2.2 CLSM is **Non-independent / GRACE-assimilated** (assimilates GRACE TWSA via Ensemble Kalman Filtering); its record starts 2003-02. CLSM 2.2 cannot serve as an independent partition of GRACE.*

---

## 2. Model Soil-Moisture Homogeneity & Forcing Evolution

> [!IMPORTANT]
> **Interpretation of Homogeneity Tests Under a Secular Trend:**  
> Non-parametric change-point tests such as Pettitt's test test the null hypothesis of stationarity against an alternative of a single step change. When applied to any time series that exhibits a continuous secular trend, Pettitt's test will mathematically reject the null and identify a nominal break near the midpoint ($t \\approx N/2$) of the series. Therefore, Pettitt test rejection under a trend does **not** constitute evidence of meteorological data inhomogeneity or instrumentation artifacts.

### Meteorological Forcing Changes Verified in GLDAS Documentation
1. **GLDAS-2.1 (Noah & VIC, Independent):**
   - Driven by atmospheric analysis from NOAA/GDAS combined with disaggregated daily GPCP Version 1.3 precipitation fields.
   - AGRMET (AFWA) radiation was integrated operationally beginning March 1, 2001.
   - Forcing precipitation is independent of domestic agricultural groundwater extraction.
2. **GLDAS-2.2 (CLSM Catchment, GRACE-Assimilated):**
   - Driven by ECMWF Integrated Forecasting System (IFS) atmospheric analysis fields.
   - Record begins February 1, 2003.
   - Assimilates satellite gravimetry TWSA observations (GRACE/GRACE-FO) directly into model hydrology. Consequently, CLSM soil moisture and groundwater fields are non-independent and inherit GRACE trends.

### Empirical Break-Point Testing (Pettitt & SNHT) on Deseasonalized Soil Moisture
| Region | Noah Break Date (Pettitt / SNHT) | Noah Homogeneous? | VIC Break Date (Pettitt / SNHT) | VIC Homogeneous? | CLSM Break Date (Pettitt / SNHT) | CLSM Homogeneous? |
|---|---|---|---|---|---|---|
"""
    for reg, h in hom_res.items():
        md += (
            f"| **{reg}** | {h['noah_pettitt_break_date']} / {h['noah_snht_break_date']} | `{h['noah_homogeneous']}` | "
            f"{h['vic_pettitt_break_date']} / {h['vic_snht_break_date']} | `{h['vic_homogeneous']}` | "
            f"{h['clsm_pettitt_break_date']} | `{h['clsm_homogeneous']}` |\\n"
        )

    md += f"""
---

## 3. Scientific Synthesis (Bilingual)

### English Scientific Synthesis
Across both independent open-loop land surface models (Noah 2.1 and VIC 2.1), simulated unsaturated zone soil moisture exhibits no statistically significant secular decline in the Northwest region (Noah: {nw_fo['noah_sms_slope']:+.2f} cm/yr, $p = {nw_fo['noah_sms_p']:.4f}$; VIC: {nw_fo['vic_sms_slope']:+.2f} cm/yr; independent range: {nw_fo['independent_sms_range']} cm/yr). In contrast, total water storage declines across the record (GRACE-FO: {nw_fo['tws_slope_cm_yr']:+.2f} cm/yr; full record: {nw_full['tws_slope_cm_yr']:+.2f} cm/yr). The resulting residual storage ('groundwater + surface water + model error residual') spans an estimated rate of {nw_fo['independent_residual_range']} cm/yr during GRACE-FO and {nw_full['independent_residual_range']} cm/yr across the full record across independent models. Most of the decline is not accounted for by simulated soil moisture; groundwater and surface water cannot be separated here. This pattern is consistent with, not proof of, agricultural groundwater extraction from the deep subsurface. CLSM 2.2 is shown separately because it assimilates GRACE observations via EnKF and cannot serve as an independent partition.

**Methodological Limitations:**  
> *Limitations:* Residual storage is strictly defined as $\\text{{Residual}} = \\text{{TWS}} - \\Delta\\text{{SMS}} - \\Delta\\text{{SWE}}$. It aggregates unmodeled surface water bodies, river stage variations, irrigation return flows, and structural model errors. It should not be interpreted as in-situ piezometric water table depth. GLDAS-2.2 CLSM assimilates GRACE observations and cannot serve as an independent partition.

---

### বাংলা বৈজ্ঞানিক বিবরণী (Bangla Scientific Synthesis)
উন্মুক্ত ল্যান্ড সারফেস মডেলের (Noah 2.1 ও VIC 2.1) বিশ্লেষণে দেখা যায় যে, উত্তর-পশ্চিম অঞ্চলে মাটির অগভীর আর্দ্রতায় কোনো তাৎপর্যপূর্ণ দীর্ঘমেয়াদী পতন ঘটেনি (নূহ মডেল: {nw_fo['noah_sms_slope']:+.2f} সেমি/বছর; ভিআইসি মডেল: {nw_fo['vic_sms_slope']:+.2f} সেমি/বছর; স্বাধীন মডেল পরিসর: {nw_fo['independent_sms_range']} সেমি/বছর)। কিন্তু স্যাটেলাইট গ্র্যাভিমেট্রি তথ্যে মোট পানি সঞ্চয় (TWS) হ্রাস পাচ্ছে (গ্রেস-এফও যুগে বার্ষিক {nw_fo['tws_slope_cm_yr']:+.2f} সেমি; পুরো রেকর্ডে বার্ষিক {nw_full['tws_slope_cm_yr']:+.2f} সেমি)। ফলস্বরূপ, স্বাধীন মডেলের অবশিষ্টাংশ সঞ্চয় ('ভূগর্ভস্থ পানি + ভূ-পৃষ্ঠের পানি + মডেল ত্রুটির অবশিষ্টাংশ') হ্রাস নির্দেশ করে (স্বাধীন মডেল পরিসর: {nw_fo['independent_residual_range']} সেমি/বছর)। মোট পানি সঞ্চয় হ্রাসের সিংহভাগই মাটির অগভীর আর্দ্রতা দিয়ে ব্যাখ্যা করা যায় না; তবে এখানে ভূগর্ভস্থ পানি ও ভূ-পৃষ্ঠের পানি আলাদা করা সম্ভব নয়। এটি গভীর নলকূপ দিয়ে সেচ উত্তোলনের সাথে সামঞ্জস্যপূর্ণ, তবে সরাসরি প্রমাণ নয়। GLDAS-2.2 CLSM মডেলটি গ্রেস ডেটা আত্তীকরণ করে বিধায় এটিকে স্বাধীন প্রামাণ্য উৎস হিসেবে বিবেচনা করা যায় না।

**সীমাবদ্ধতার বিজ্ঞপ্তি:**  
> *সীমাবদ্ধতা:* অবশিষ্টাংশ সঞ্চয়কে কঠোরভাবে 'ভূগর্ভস্থ পানি + ভূ-পৃষ্ঠের পানি + মডেল ত্রুটির অবশিষ্টাংশ' হিসেবে সংজ্ঞায়িত করা হয়েছে। এতে নদী-নালা ও উন্মুক্ত জলাশয়ের প্রবাহ এবং মডেলের কাঠামোগত অনিশ্চয়তা অন্তর্ভুক্ত। একে সরাসরি স্থানীয় নলকূপের পানির স্তর হিসেবে গণ্য করা যাবে না। অধিকন্তু, GLDAS-2.2 CLSM মডেলে গ্রেস স্যাটেলাইট তথ্য আত্তীকরণ (assimilated) করা হয়েছে, বিধায় এটি কোনো স্বাধীন প্রামাণ্য উৎস নয়।
"""

    rep_path = OUTPUT_DIR / "gldas_multi_model_summary.md"
    rep_path.write_text(md, encoding="utf-8")
    print(f"  [OK] Saved Multi-Model Summary Markdown: {rep_path.name}")

    summary_json = {
        "status": "COMPLETED",
        "timestamp": datetime.now().isoformat(),
        "models": {
            "noah_21": {"short_name": "GLDAS_NOAH025_M", "resolution": "0.25 deg", "depth_m": 2.0, "role": "independent"},
            "vic_21": {"short_name": "GLDAS_VIC10_M", "resolution": "1.0 deg", "layers": 3, "role": "independent"},
            "clsm_22": {"short_name": "GLDAS_CLSM025_DA1_D", "resolution": "0.25 deg", "role": "non-independent", "note": "Assimilates GRACE TWSA via EnKF; cannot serve as independent partition", "start": "2003-02"}
        },
        "windows_evaluated": ["full_record", "grace_era", "grace_fo_era", "recent_2020"],
        "residual_label": "groundwater + surface water + model error residual",
        "northwest_grace_fo": {
            "tws_slope_cm_yr": nw_fo["tws_slope_cm_yr"],
            "noah_sms_slope_cm_yr": nw_fo["noah_sms_slope"],
            "vic_sms_slope_cm_yr": nw_fo["vic_sms_slope"],
            "independent_sms_range_cm_yr": nw_fo["independent_sms_range"],
            "independent_residual_range_cm_yr": nw_fo["independent_residual_range"],
            "clsm_sms_slope_cm_yr": nw_fo["clsm_sms_slope"] if pd.notna(nw_fo["clsm_sms_slope"]) else None,
            "clsm_note": "Non-independent / GRACE-assimilated"
        },
        "homogeneity_summary": hom_res,
        "homogeneity_interpretation_note": "Pettitt test detects step changes under a trend and does not constitute evidence of data inhomogeneity."
    }
    json_path = OUTPUT_DIR / "gldas_multi_model_summary.json"
    json_path.write_text(json.dumps(summary_json, indent=2), encoding="utf-8")
    print(f"  [OK] Saved Multi-Model Summary JSON: {json_path.name}")'''

content = old_report_func.sub(lambda m: new_report_code, content)

# 4. Update plot_multi_model_figures
old_plot_func = re.compile(r'def plot_multi_model_figures\(part_df: pd\.DataFrame\):.*?\n    print\(f"  \[OK\] Saved Multi-Model Storage Partition Figure: \{fig_path\.name\}"\)', re.DOTALL)
assert old_plot_func.search(content) is not None, "Could not find plot_multi_model_figures"

new_plot_code = '''def plot_multi_model_figures(part_df: pd.DataFrame):
    fig, axes = plt.subplots(4, 1, figsize=(15, 16), sharex=True)

    colors = {"NW": "#d97706", "NE": "#0284c7", "Central": "#7c3aed", "National": "#111827"}

    for reg, col in colors.items():
        sub = part_df[part_df["region"] == reg].sort_values("date")
        dates = pd.to_datetime(sub["date"])
        lw = 2.0 if reg == "National" else 1.3

        # Panel 1: Satellite TWS Anomaly
        axes[0].plot(dates, sub["grace_tws_cm"], label=f"{reg} ({REGIONS[reg]['name_long']})", lw=lw, color=col)

        # Panel 2: GLDAS Noah 2.1 Soil Moisture (Independent)
        axes[1].plot(dates, sub["noah_sms_anom_cm"], label=f"{reg}", lw=lw, color=col)

        # Panel 3: Independent Land Surface Models Soil Moisture (Noah 2.1 & VIC 2.1 range shaded)
        axes[2].plot(dates, sub["independent_sms_mean_cm"], label=f"{reg} Independent Mean (Noah+VIC)", lw=lw, color=col)
        if reg in ["NW", "National"]:
            axes[2].fill_between(dates, sub["independent_sms_min_cm"], sub["independent_sms_max_cm"],
                                 color=col, alpha=0.15, label=f"{reg} Independent Spread [Min, Max]")
            # CLSM shown dashed
            if "clsm_sms_anom_cm" in sub.columns and sub["clsm_sms_anom_cm"].notna().any():
                axes[2].plot(dates, sub["clsm_sms_anom_cm"], color=col, linestyle="--", lw=0.9, alpha=0.7,
                             label=f"{reg} CLSM 2.2 (GRACE-DA, non-independent)" if reg == "NW" else None)

        # Panel 4: Partitioned Residual Storage Anomaly (Groundwater + Surface Water + Model Error Residual)
        axes[3].plot(dates, sub["noah_residual_cm"], label=f"{reg} Noah Residual", lw=lw, color=col)
        if reg in ["NW", "National"]:
            axes[3].fill_between(dates, sub["independent_residual_min_cm"], sub["independent_residual_max_cm"],
                                 color=col, alpha=0.15, label=f"{reg} Independent Residual Range")

    axes[0].set_title("A. Terrestrial Water Storage Anomaly (GRACE/GRACE-FO CSR Mascons RL0603)", fontsize=11, fontweight="bold")
    axes[0].set_ylabel("TWS Anomaly (cm)", fontsize=10)
    axes[0].grid(True, linestyle=":", alpha=0.5)
    axes[0].axhline(0, color="gray", lw=0.8, linestyle="--")
    axes[0].legend(loc="lower left", ncol=4, fontsize=9)

    axes[1].set_title("B. Independent Soil Moisture Anomaly (NASA GLDAS Noah 2.1, 0–2 m depth, re-baselined to 2004–2009)", fontsize=11, fontweight="bold")
    axes[1].set_ylabel("Noah ΔSMS (cm)", fontsize=10)
    axes[1].grid(True, linestyle=":", alpha=0.5)
    axes[1].axhline(0, color="gray", lw=0.8, linestyle="--")

    axes[2].set_title("C. Independent Soil Moisture Anomaly & Spread (Noah 2.1 vs VIC 2.1; CLSM 2.2 [GRACE-DA] shown dashed)", fontsize=11, fontweight="bold")
    axes[2].set_ylabel("ΔSMS (cm)", fontsize=10)
    axes[2].grid(True, linestyle=":", alpha=0.5)
    axes[2].axhline(0, color="gray", lw=0.8, linestyle="--")
    axes[2].legend(loc="lower left", ncol=3, fontsize=8)

    axes[3].set_title("D. Independent Partitioned Residual Storage Anomaly (Groundwater + Surface Water + Model Error Residual)", fontsize=11, fontweight="bold")
    axes[3].set_ylabel("Residual (cm)", fontsize=10)
    axes[3].set_xlabel("Year", fontsize=10)
    axes[3].grid(True, linestyle=":", alpha=0.5)
    axes[3].axhline(0, color="gray", lw=0.8, linestyle="--")

    plt.suptitle("Bengal Basin Multi-Model Storage Partitioning: GRACE vs GLDAS (Noah 2.1, VIC 2.1, CLSM 2.2)\n"
                 "PRELIMINARY — Team Tenstral | NASA Space Apps Challenge 2026", fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig_path = OUTPUT_DIR / "fig_storage_partition_multi_model.png"
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"  [OK] Saved Multi-Model Storage Partition Figure: {fig_path.name}")'''

content = old_plot_func.sub(lambda m: new_plot_code, content)

target_file.write_text(content, encoding="utf-8")
print("Successfully updated v3/gldas_multi_model_processor.py")
