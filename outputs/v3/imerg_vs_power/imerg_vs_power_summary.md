# GPM IMERG V07B vs NASA POWER Precipitation Homogeneity & Cross-Validation Audit

**Project:** Bengal Hydro Detective — NASA Space Apps Challenge 2026  
**Team:** Tenstral  
**Status:** PRELIMINARY  
**Primary Evaluated Overlap Period:** 2002-01 to 2025-09 (285 months continuous overlap)  
**Products Evaluated:**
- **Primary Source (Selected):** GPM IMERG Final Run V07B monthly accumulation (`GPM_3IMERGM`, 0.1° grid, unit-converted from mm/hr using calendar-exact days per month)
- **Secondary Sensitivity Source:** NASA POWER MERRA-2 corrected precipitation (`PRECTOTCORR`, 0.5° grid)

---

## 1. Executive Summary, Data Span & Decision Rule

### Data Span & Window Truncation Notice
- GPM IMERG Final Run V07B currently extends through **2025-09** (due to GES DISC ~3-4 month release latency for Final Run granules).
- **Window Coverage:**
  - `full_record`: GRACE extends to 2026-07 (292 months); IMERG is available for 282 of those months (**truncated by 10 months**, 2025-10 to 2026-07).
  - `grace_era`: 2002-04 to 2017-06 (183 months; **fully covered by IMERG**, 0 months truncated).
  - `grace_fo_era`: GRACE-FO extends 2018-06 to 2026-07 (98 months); IMERG covers 88 months (**truncated by 10 months**).
  - `recent_2020`: extends 2020-01 to 2026-07 (79 months); IMERG covers 69 months (**truncated by 10 months**).

### Primary Decision Rule
A precipitation dataset qualifies as the primary rainfall source for water storage trend analysis if:
1. **Statistical Homogeneity:** Non-parametric change-point testing (Pettitt test $p > 0.05$) on deseasonalized monthly anomalies shows no statistically significant step change across the analysis period.
2. **Climatological Consistency:** Multi-year mean annual totals are broadly consistent with ground-observed climatology across geographic divisions.
3. **Difference Series Attribution:** In the paired difference series ($\Delta P_t = \text{POWER}_t - \text{IMERG}_t$), any detected break must be attributed to non-climatic model/assimilation shifts rather than physical precipitation changes.

### Decision Verdict: GPM IMERG V07B Selected as PRIMARY Rainfall Series
- **NASA POWER Non-Homogeneity:** NASA POWER exhibits a statistically significant upward step change with data-driven break dates between **2014-12 and 2015-12** across all regions (Pettitt $p < 0.0001$, SNHT $p < 0.001$). Following this shift, POWER annual totals surge by **+45% to +84%** (+65.0% nationally; NW: 1,579 to 2,328 mm/yr; SE: 2,389 to 4,397 mm/yr). The underlying physical cause of this step change in MERRA-2 assimilation remains **unverified**. This step shift created artificial, non-climatic positive rainfall trends (+28 to +108 mm/yr) in earlier analyses.
- **GPM IMERG Calibration Status:**
  - Under Pettitt's non-parametric rank test, GPM IMERG shows **no statistically significant step change in any region** ($p = 0.152$ to $1.000$; National $p = 0.876$).
  - Under Alexandersson's SNHT, IMERG is non-significant across 5 regions ($p = 0.396$ to $0.843$), but detects a potential mean shift in the Northwest ($T_0 = 14.6, p = 0.013$ at `2005-10`).
  - IMERG multi-year means (NW: 1,954 mm/yr; NE: 3,010 mm/yr) fall outside single-station point ranges reported in literature (such as Rajshahi town at ~1,400–1,600 mm or Sylhet town at ~3,800–4,300 mm; Shahid 2010), reflecting regional polygon integration that incorporates surrounding higher-elevation margins.
  - Nationally, IMERG's 24-year mean is **2,366 mm/yr**, close to the official Bangladesh Meteorological Department (BMD) 30-year national station normal of **2,428 mm/yr** (BMD 1981–2010; Shahid 2010).
- **Decision:** GPM IMERG V07B Final Run is designated as the **PRIMARY** precipitation record. NASA POWER is classified as a non-homogeneous secondary series and retained solely for sensitivity comparison.

---

## 2. Statistical Homogeneity & Break-Point Scan

| Region | Overlap Months | POWER Pettitt $p$ | POWER Break Date | IMERG Pettitt $p$ | IMERG SNHT $p$ | Difference Pettitt $p$ | Difference Break Date | POWER Pre-Break (2004–10) | POWER Post-Break (2019–25) | POWER Jump (%) | IMERG Full Record Mean | Published Benchmark Normals | Source |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **NW** | 285 | < 0.0001 | `2015-11` | 0.1522 | 0.0130 | < 0.0001 | `2015-12` | 1578.9 mm | 2328.3 mm | **+47.5%** | 1953.7 mm | 1400–1600 mm | Shahid (2010); Islam et al. (2021) |
| **NE** | 285 | < 0.0001 | `2015-12` | 0.8374 | 0.8430 | < 0.0001 | `2015-10` | 2477.0 mm | 3926.6 mm | **+58.5%** | 3010.3 mm | 3800–4300 mm | Shahid (2010); BMD Normals |
| **Central** | 285 | < 0.0001 | `2015-12` | 0.5960 | 0.3960 | < 0.0001 | `2015-12` | 1796.2 mm | 2611.9 mm | **+45.4%** | 2078.3 mm | 1900–2200 mm | Shahid (2010); BMD Normals |
| **SW** | 285 | < 0.0001 | `2014-12` | 1.0000 | 0.4470 | < 0.0001 | `2014-12` | 1672.7 mm | 2993.2 mm | **+78.9%** | 2107.2 mm | 1800–2100 mm | Shahid (2010); Islam et al. (2021) |
| **SE** | 285 | < 0.0001 | `2014-12` | 0.8742 | 0.7510 | < 0.0001 | `2014-11` | 2389.3 mm | 4397.0 mm | **+84.0%** | 2821.7 mm | 2800–3500 mm | Shahid (2010); Islam et al. (2021) |
| **National** | 285 | < 0.0001 | `2014-12` | 0.8758 | 0.5180 | < 0.0001 | `2015-12` | 1951.3 mm | 3218.7 mm | **+65.0%** | 2366.1 mm | 2300–2500 mm | BMD 30-Year Normal (1981-2010); Shahid (2010) |

---

## 3. Bias Before and After the Step Break (2002–2014 vs 2015–2025)

| Region | Pre-Break Bias (2002–2014) | Pre-Break Bias (%) | Post-Break Bias (2015–2025) | Post-Break Bias (%) | Net Upward Shift in POWER |
|---|---|---|---|---|---|
| **NW** | -35.8 mm/mo | -21.8% | +25.3 mm/mo | +15.5% | **+61.1 mm/mo** |
| **NE** | -48.1 mm/mo | -19.5% | +76.9 mm/mo | +29.8% | **+125.0 mm/mo** |
| **Central** | -30.0 mm/mo | -17.5% | +51.4 mm/mo | +28.8% | **+81.4 mm/mo** |
| **SW** | -35.8 mm/mo | -20.6% | +86.8 mm/mo | +47.9% | **+122.7 mm/mo** |
| **SE** | -32.1 mm/mo | -13.8% | +160.5 mm/mo | +65.9% | **+192.6 mm/mo** |
| **National** | -36.4 mm/mo | -18.6% | +79.5 mm/mo | +39.3% | **+115.9 mm/mo** |

---

## 4. Cross-Validation Metrics (2002-01 to 2025-09, 285 Months Overlap)

| Region | Overlap Months | Raw Monthly Pearson $r$ | Raw Spearman $\rho$ | Deseasonalized Anomaly $r_{anom}$ | Deseasonalized $\rho_{anom}$ | Mean IMERG (mm/mo) | Mean POWER (mm/mo) | Overall Bias (POWER - IMERG) | Percent Bias (%) | RMSE (mm/mo) |
|---|---|---|---|---|---|---|---|---|---|---|
| **NW** | 285 | 0.937 | 0.963 | **0.734** | **0.726** | 163.9 | 155.7 | -8.2 mm | -5.0% | 58.1 |
| **NE** | 285 | 0.908 | 0.950 | **0.676** | **0.688** | 252.2 | 260.7 | +8.5 mm | +3.4% | 109.9 |
| **Central** | 285 | 0.917 | 0.953 | **0.729** | **0.698** | 174.7 | 181.5 | +6.9 mm | +3.9% | 72.2 |
| **SW** | 285 | 0.875 | 0.944 | **0.622** | **0.644** | 177.2 | 196.9 | +19.7 mm | +11.1% | 110.1 |
| **SE** | 285 | 0.858 | 0.941 | **0.603** | **0.624** | 237.1 | 292.2 | +55.1 mm | +23.2% | 202.6 |
| **National** | 285 | 0.899 | 0.952 | **0.605** | **0.623** | 198.7 | 214.8 | +16.1 mm | +8.1% | 99.6 |

---

## 5. Seasonal Bias Breakdown (POWER minus IMERG)

| Region | Pre-monsoon (MAM) Bias | Monsoon (JJAS) Bias | Post-monsoon (ON) Bias | Dry Season (DJF) Bias |
|---|---|---|---|---|
| **NW** | -2.5 mm/mo (-2.0%) | -25.8 mm/mo (-7.4%) | +6.1 mm/mo (+7.8%) | +0.7 mm/mo (+7.6%) |
| **NE** | +25.6 mm/mo (+10.4%) | -1.4 mm/mo (-0.3%) | +6.9 mm/mo (+5.8%) | +5.4 mm/mo (+41.7%) |
| **Central** | +14.7 mm/mo (+10.3%) | -0.6 mm/mo (-0.2%) | +12.9 mm/mo (+12.3%) | +5.2 mm/mo (+43.3%) |
| **SW** | +16.4 mm/mo (+15.7%) | +32.7 mm/mo (+8.6%) | +19.0 mm/mo (+15.9%) | +5.8 mm/mo (+45.6%) |
| **SE** | +26.7 mm/mo (+16.8%) | +124.0 mm/mo (+24.2%) | +36.1 mm/mo (+27.0%) | +3.0 mm/mo (+25.1%) |
| **National** | +15.1 mm/mo (+10.0%) | +25.9 mm/mo (+6.2%) | +16.3 mm/mo (+14.9%) | +3.8 mm/mo (+32.6%) |

---

## 6. Trend Engine Comparison Across Windows (Calibrated ESS-MK Engine)

| Window | Region | IMERG Slope (mm/yr) [95% CI] | IMERG $p$ | IMERG Verdict (PRIMARY) | POWER Slope (mm/yr) [95% CI] | POWER $p$ | POWER Verdict (SENSITIVITY) | Slope Diff (POWER - IMERG) |
|---|---|---|---|---|---|---|---|---|
| `full_record` | **NW** | -2.6 [-12.3, +3.5] | 0.3819 | `No detectable trend` | +27.7 [+14.7, +42.0] | < 0.0001 | `Suggestive increase` | +30.2 |
| `full_record` | **NE** | -1.6 [-16.4, +13.0] | 0.7406 | `No detectable trend` | +61.1 [+33.8, +95.1] | < 0.0001 | `Suggestive increase` | +62.7 |
| `full_record` | **Central** | -0.7 [-12.4, +10.3] | 0.8670 | `No detectable trend` | +47.0 [+24.2, +72.7] | < 0.0001 | `Suggestive increase` | +47.7 |
| `full_record` | **SW** | +0.1 [-10.6, +10.7] | 0.9689 | `No detectable trend` | +64.9 [+35.9, +98.9] | < 0.0001 | `Suggestive increase` | +64.8 |
| `full_record` | **SE** | +1.2 [-11.0, +12.6] | 0.8269 | `No detectable trend` | +108.0 [+61.5, +162.1] | < 0.0001 | `Suggestive increase` | +106.8 |
| `full_record` | **National** | -0.2 [-10.0, +9.0] | 0.9597 | `No detectable trend` | +68.3 [+39.7, +99.1] | < 0.0001 | `Suggestive increase` | +68.5 |
| `grace_era` | **NW** | -14.6 [-35.4, +1.1] | 0.0725 | `No detectable trend` | +5.5 [-7.3, +23.9] | 0.3692 | `No detectable trend` | +20.0 |
| `grace_era` | **NE** | -4.1 [-41.3, +26.6] | 0.7191 | `No detectable trend` | +23.6 [-7.2, +61.9] | 0.1442 | `No detectable trend` | +27.6 |
| `grace_era` | **Central** | -15.9 [-41.3, +3.5] | 0.1235 | `No detectable trend` | +15.9 [-7.5, +46.1] | 0.1895 | `No detectable trend` | +31.7 |
| `grace_era` | **SW** | -6.8 [-32.3, +11.9] | 0.4794 | `No detectable trend` | +47.5 [+13.0, +93.0] | 0.0033 | `Suggestive increase` | +54.3 |
| `grace_era` | **SE** | +4.0 [-19.0, +27.5] | 0.6224 | `No detectable trend` | +126.4 [+63.9, +203.1] | < 0.0001 | `Suggestive increase` | +122.3 |
| `grace_era` | **National** | -8.7 [-36.3, +8.1] | 0.2959 | `No detectable trend` | +46.9 [+13.5, +84.0] | 0.0025 | `Suggestive increase` | +55.6 |
| `grace_fo_era` | **NW** | +15.2 [-33.6, +87.9] | 0.5764 | `No detectable trend` | +15.9 [-53.9, +92.2] | 0.6480 | `No detectable trend` | +0.6 |
| `grace_fo_era` | **NE** | +46.9 [-31.4, +138.5] | 0.2532 | `No detectable trend` | +15.3 [-84.9, +141.0] | 0.7703 | `No detectable trend` | -31.6 |
| `grace_fo_era` | **Central** | +40.2 [-23.5, +123.8] | 0.2506 | `No detectable trend` | -5.2 [-107.2, +98.6] | 0.8613 | `No detectable trend` | -45.4 |
| `grace_fo_era` | **SW** | +27.5 [-63.8, +121.7] | 0.5206 | `No detectable trend` | -65.6 [-272.1, +96.0] | 0.4704 | `No detectable trend` | -93.0 |
| `grace_fo_era` | **SE** | +24.4 [-40.0, +107.2] | 0.4969 | `No detectable trend` | -105.4 [-272.2, +43.0] | 0.1670 | `No detectable trend` | -129.8 |
| `grace_fo_era` | **National** | +23.9 [-32.5, +98.0] | 0.4370 | `No detectable trend` | -36.4 [-153.6, +69.0] | 0.4763 | `No detectable trend` | -60.3 |
| `recent_2020` | **NW** | -26.6 [-119.3, +43.6] | 0.4014 | `No detectable trend` | -36.7 [-156.7, +65.7] | 0.4870 | `No detectable trend` | -10.1 |
| `recent_2020` | **NE** | -1.4 [-84.1, +105.7] | 0.9628 | `No detectable trend` | +1.8 [-151.9, +144.2] | 0.9628 | `No detectable trend` | +3.1 |
| `recent_2020` | **Central** | -7.7 [-95.3, +72.7] | 0.8144 | `No detectable trend` | -11.5 [-148.3, +141.6] | 0.8081 | `No detectable trend` | -3.8 |
| `recent_2020` | **SW** | -8.7 [-112.5, +95.4] | 0.8227 | `No detectable trend` | -29.4 [-264.2, +165.4] | 0.7308 | `No detectable trend` | -20.7 |
| `recent_2020` | **SE** | +24.1 [-84.0, +144.8] | 0.6846 | `No detectable trend` | -8.6 [-265.3, +227.8] | 0.9232 | `No detectable trend` | -32.6 |
| `recent_2020` | **National** | -28.6 [-115.3, +52.3] | 0.4612 | `No detectable trend` | -48.4 [-216.0, +123.1] | 0.5118 | `No detectable trend` | -19.8 |

---

## 7. Physical Synthesis & Evidence Assessment

1. **Resolution of the Artificial Rainfall Increase:**
   - Previous versions reported significant positive rainfall trends (+28 to +108 mm/yr) driven by NASA POWER. This audit shows that these trends are non-climatic artifacts caused by an abrupt upward step change in NASA POWER between 2014-12 and 2015-12 (potential MERRA-2 assimilation shift, unverified).
   - Under the calibrated GPM IMERG V07B record, **no statistically significant long-term rainfall trend exists across Bangladesh** during the 2002–2025 period (all regions exhibit `No detectable trend` under the calibrated ESS-MK engine, with slopes between -2.6 and +1.2 mm/yr).

2. **Correction of Prior Hypotheses:**
   - Earlier draft text conjectured that IMERG showed higher values due to "capturing heavier convective cells with dual-frequency radar". That conjecture was incorrect and is deleted: **IMERG is systematically lower than NASA POWER nationally post-2015**, where POWER exhibits an upward surge of +79.5 mm/month relative to IMERG.

3. **Status of the Bengal Water Storage Paradox:**
   - Because GPM IMERG confirms that rainfall in the Northwest and Central regions has remained stable without long-term decline or surge, the persistent depletion of Total Water Storage (TWS) in the Northwest (-1.25 to -1.81 cm/yr) and Central divisions occurs without a corresponding decline in rainfall influx.
   - This pattern is **consistent with, not proof of**, human water extraction (such as intensive Boro dry-season groundwater abstraction).
