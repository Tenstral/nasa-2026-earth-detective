# Bengal Hydro Detective — Plain-Language Project Status & Findings Guide

**NASA Space Apps Challenge 2026 — Be an Earth System Trend Detective!**  
**Team:** Tenstral  
**Status:** PRELIMINARY — Subject to Peer Review and In-Situ Hydrometric Validation  
**Audience:** Non-statistician teammates, presenters, and reviewers  

---

## 1. What Is This Project and What Question Does It Answer?

Every summer, Bangladesh receives substantial monsoon rainfall, nourishing river networks and occasionally causing major seasonal flooding. Yet farmers and local water managers in the northern agricultural heartland report that tubewells run dry during the pre-monsoon dry season and water tables have declined over recent decades.

**This project answers a fundamental Earth System question:**  
> *Is Bangladesh losing total water storage over the long term, how do regional storage trajectories compare to satellite precipitation trends, and does unsaturated soil moisture account for observed storage changes?*

To evaluate these dynamics empirically, we developed a reproducible scientific detection pipeline that audits **24 continuous years of NASA satellite observations** (April 2002 to July 2026). The analysis synthesizes:
1. **NASA/CSR GRACE and GRACE Follow-On satellite gravimetry:** Twin satellite missions measuring vertically integrated regional mass changes, capturing total water storage (TWS)—including surface water bodies, unsaturated topsoil moisture, and deep groundwater.
2. **Satellite precipitation records:** GPM IMERG Final Run V07B (radar and passive microwave calibrated satellite precipitation) and NASA POWER (atmospheric reanalysis).
3. **NASA Land Surface Models (GLDAS Noah 2.1 and VIC 2.1):** Open-loop physical land surface models simulating moisture in the top 2 meters of soil.
4. **NASA Socioeconomic and Land Cover grids:** Gridded population (SEDAC GPWv4) and cropland coverage (MODIS MCD12Q1).

### Spatial Scale & Test Hierarchy
- **Regional vs. Divisional Analysis:** Satellite gravimetry operates at an effective spatial resolution of approximately 300 km. Consequently, individual administrative divisions cannot be treated as statistically independent hydrological catchments. We aggregate data into **5 hydrologically cohesive macro-regions** (Northwest, Northeast, Central, Southwest, Southeast) and a **National** composite. Administrative division series are provided strictly for **descriptive and local administrative context** (`Descriptive (not independent)`).
- **The 336 Statistical Tests:** The master results file (`results_all_windows.csv`) audits exactly 336 individual tests: 4 analytical windows $\times$ 14 spatial units (6 macro-regions + 8 administrative divisions) $\times$ 2 variables (TWS, IMERG precipitation) $\times$ 3 seasonal slices (annual/all-months, dry season, monsoon season) = $4 \times 14 \times 2 \times 3 = 336$ tests. All formal hypothesis testing and False Discovery Rate (FDR) screening are evaluated at the 5-region and National scale.

---

## 2. Headline Findings by Region and Window

### A. The Geography of Total Water Storage (Where Is Storage Changing?)
*Note on Confidence Intervals and Significance:* All reported 95% confidence intervals and p-values originate directly from `results_all_windows.csv` and are computed via **Calibrated ESS-Mann-Kendall** (duality-aligned rank-based Theil-Sen 95% CIs with Hurwicz AR(1) bias-corrected effective sample size).

Total water storage trajectories across Bangladesh exhibit marked regional divergence:

1. **The Northwest Depletion Corridor (Rajshahi and Rangpur):**
   - The Northwest is the nation's primary storage loss hotspot across all multi-decadal evaluations.
   - **Full 24-Year Record (2002–2026):** Total water storage has declined at **-1.25 cm/year** (95% CI: **[-1.50, -1.02] cm/yr**, $p < 0.0001$, within-window FDR $q < 0.0001$). This corresponds to a volumetric loss of **-0.39 billion cubic meters (km³) of water per year**. Over the 24.2-year record, cumulative storage loss totals approximately **-9.5 km³** in this region alone.
   - **Historical Baseline (GRACE-1 era, 2002–2017):** Clean transition-free storage declined at **-1.56 cm/year** (95% CI: **[-1.96, -1.17] cm/yr**, $p < 0.0001$, FDR $q < 0.0001$), or **-0.49 km³/year**.

2. **The Northeast and Central Regions (Dhaka, Sylhet, Mymensingh):**
   - **Central (Dhaka):** Declining at **-0.47 cm/year** (95% CI: **[-0.62, -0.34] cm/yr**, $p < 0.0001$, FDR $q < 0.0001$, -0.08 km³/yr) over the full record.
   - **Northeast (Sylhet and Mymensingh):** Declining at **-0.56 cm/year** (95% CI: **[-0.70, -0.42] cm/yr**, $p < 0.0001$, FDR $q < 0.0001$, -0.12 km³/yr) over the full record.

3. **The Southern Delta (Khulna, Barishal, Chattogram):**
   - **Southwest:** **-0.05 cm/year** (95% CI: **[-0.20, +0.10] cm/yr**, $p = 0.55$, FDR $q = 0.8968$). Minimum detectable slope (MDS, 80% power) for `full_record` in SW is **0.22 cm/year** (window range 0.22 to 0.32 cm/yr). Verdict: **no detectable change/trend**.
   - **Southeast:** **-0.05 cm/year** (95% CI: **[-0.17, +0.06] cm/yr**, $p = 0.38$, FDR $q = 0.8968$). Minimum detectable slope (MDS, 80% power) for `full_record` in SE is **0.22 cm/year** (window range 0.22 to 0.32 cm/yr). Verdict: **no detectable change/trend**.
   - As an untested hypothesis, the southern delta may be buffered by estuarine river networks, coastal mangrove wetlands (the Sundarbans), and lower agricultural dry-season groundwater abstraction relative to the north.

4. **National Total (All Bangladesh Combined):**
   - Nationally, total water storage has declined at **-0.51 cm/year** (95% CI: **[-0.66, -0.38] cm/yr**, $p < 0.0001$, FDR $q < 0.0001$) over the full 24-year record, equal to a volumetric loss of **-0.63 km³ of water per year** across the country.

---

### B. The 3-Way Northwest Slope Transparency
Between the original GRACE mission (decommissioned June 2017) and GRACE Follow-On (operational June 2018), an 11-month observation gap occurred. An upward step offset (+9.15 cm in NW, $p = 0.028$) of unknown origin is detected across the gap in raw gravimetric anomaly series. Because multi-satellite trends across unbridged gaps can be sensitive to step offsets, we report the Northwest trend across three transparent model specifications (sourced from `outputs/v3/full_record/three_way_slopes_and_transition.md`):

| Method / Model Specification | Northwest TWS Slope | 95% Confidence Interval | Methodological Description |
|---|:---:|:---:|---|
| **1. Lead Evidence: GRACE-1 Era (2002–2017)** | **-1.56 cm/yr** | [-1.96, -1.17] cm/yr | Transition-free baseline under a single continuous satellite instrument. |
| **2. Single Continuous Line (2002–2026)** | **-1.25 cm/yr** | [-1.50, -1.02] cm/yr | Standard linear trend fit across the full 24-year record under Calibrated ESS-MK. |
| **3. Step-Adjusted Fit (2002–2026)** | **-1.81 cm/yr** | — | Controls for a +9.15 cm upward step offset ($p = 0.028$) across the 2017–2018 transition. |
| **4. Transition-Excluded ($\pm 6$-Month Buffer)** | **-1.29 cm/yr** | — | Excludes 2017-01 to 2018-11; the transition step (+7.83 cm, $p = 0.171$) is not significant. |

*Takeaway:* Across continuous, step-adjusted, and transition-excluded specifications, Northwest multi-satellite total water storage depletion spans an estimated range of **-1.81 to -1.25 cm/year** (with the single-satellite lead benchmark at **-1.56 cm/year**). Pure step simulations show that an unadjusted +9.15 cm step is falsely flagged as a trend in 93.8% to 100% of red-noise simulations under standard linear models, showing why step-adjusted and buffer-excluded bounds are necessary.

---

## 3. Evidence Certainty Tiers: Significant, Suggestive, and Below Detection Limit

To prevent false alarms in autocorrelated satellite data, we apply a dual-threshold criterion: a finding is categorized as **Significant** only if it passes within-window False Discovery Rate screening ($q < 0.05$) AND its duality-aligned 95% confidence interval excludes zero.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        EVIDENCE CERTAINTY TIERS                        │
├────────────────────────────────────────────────────────────────────────┤
│ 1. STATISTICALLY SIGNIFICANT TRENDS (FDR q < 0.05 & CI Excludes Zero)  │
│    • Northwest Total Water Storage: Full record (-1.25 cm/yr, q<0.0001)│
│    • Northwest Total Water Storage: Historical era (-1.56 cm/yr)       │
│    • Northeast Total Water Storage: Full record (-0.56 cm/yr, q<0.0001)│
│    • Central Total Water Storage: Full record (-0.47 cm/yr, q<0.0001)  │
│    • National Total Water Storage: Full record (-0.51 cm/yr, q<0.0001) │
│    • National Total Water Storage: Historical era (-0.68 cm/yr)        │
├────────────────────────────────────────────────────────────────────────┤
│ 2. METHOD-DEPENDENT / SENSITIVITY FINDINGS                             │
│    • Northwest in recent_2020 (2020–2026): Point slope is -2.93 cm/yr  │
│      (95% CI: [-4.97, -0.78] cm/yr). Raw p = 0.0107, but within-window │
│      FDR q = 0.0772 > 0.05 (fails significance standard). Different    │
│      statistical tests yield diverging verdicts; labeled               │
│      METHOD-DEPENDENT rather than Significant.                         │
├────────────────────────────────────────────────────────────────────────┤
│ 3. BELOW DETECTION LIMIT / NO DETECTABLE TREND                         │
│    • Southwest and Southeast Total Water Storage across all windows.   │
│    • Northwest in grace_fo_era (2018–2026): slope is -1.67 cm/yr       │
│      (95% CI: [-3.32, +0.06] cm/yr, p = 0.0549, FDR q = 0.4626). The   │
│      CI spans zero; this rate falls below the 80% detection limit      │
│      (MDS = 1.74 cm/yr) for an 8.1-year window.                        │
│    • ALL regional precipitation trends (GPM IMERG): rainfall displays  │
│      no detectable multi-decadal upward or downward trend anywhere.    │
│    • Extreme precipitation indices (Rx1day, Rx5day, heavy rain days).  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. The Rainfall Record: Data Artifact vs. Satellite Observation

### A. The NASA POWER Reanalysis Artifact
Earlier exploratory evaluations reported that Bangladesh rainfall was increasing rapidly (+29 to +86 mm/year). Systematic data audit identified this as a **reanalysis data artifact**:
- Between 2014-12 and 2015-12, NASA POWER's underlying assimilation system (MERRA-2) underwent an abrupt upward step change of **+45% to +84%** across Bangladesh (Pettitt $p < 0.0001$, SNHT $T = 31.94$).
- In the Northwest, annual totals jumped from ~1,580 mm/year prior to 2015 to ~2,330 mm/year after 2018.
- This non-climatic step shift induced spurious positive linear trends. The exact cause in the reanalysis model assimilation stream remains unverified.

### B. Satellite Precipitation with GPM IMERG: No Detectable Rainfall Trend (Wide CI: NW about ±8 mm/yr)
Replacing atmospheric reanalysis with NASA's radar and microwave satellite precipitation constellation (**GPM IMERG V07B Final Run**) eliminated the artificial jump:
- Nationally, annual IMERG rainfall trend is **+2.04 mm/year** (95% CI: **[-7.70, +12.45] mm/yr**, $p = 0.64$, FDR $q = 0.9342$), showing **no detectable trend** within natural multi-year variability.
- In the Northwest, annual rainfall trend is **-1.91 mm/year** (95% CI: **[-11.04, +4.48] mm/yr**, $p = 0.54$, FDR $q = 0.8968$), also showing **no detectable trend**.
- Over the satellite observational period (2002-01 to 2025-09), national IMERG precipitation averages **2,366 mm/year**.
- *Data Latency Notice:* GPM IMERG Final data currently extends through September 2025 due to standard NASA production latency, truncating the final 10 months of the 2002–2026 gravimetry analysis window.

### C. Extreme Rainfall and Flood Dynamics
- **Stationary Extreme Indices:** Daily precipitation extremes (Rx1day, Rx5day, days $\ge 50\text{ mm}$, and annual total for 2003–2024; monsoon total, monsoon Rx1day, monsoon Rx5day, and monsoon days $\ge 50\text{ mm}$ for 2002–2025) show no statistically significant trend across Bangladesh.
- **Flood Response and Storage Recovery (Untested Hypothesis):** Historical flood events (2004, 2007, 2017, 2020, 2022 Sylhet) correspond to large transient storage surges (e.g., storage anomalies spiked by +41 cm in 2007 and +33 cm in 2004):
  - An untested hypothesis frequently cited in regional hydrogeology suggests that topsoil saturation and floodplain drainage limit the proportion of floodwaters that recharge deeper subsurface storage, allowing subsequent dry-season abstraction to outpace seasonal recharge.
  - However, this mechanism remains an unverified hypothesis in this study; satellite gravimetry captures vertically integrated bulk mass and cannot measure subsurface infiltration rates directly without in-situ piezometer hydrographs.

---

## 5. Storage Partitioning: Soil moisture explains a minor part of the NW decline; the remainder is an unpartitioned residual

Satellite gravimetry measures total column water mass, integrating surface water, soil moisture, and deep groundwater. To determine whether total water storage depletion is accounted for by unsaturated soil drying, we evaluated NASA's **GLDAS Land Surface Models** across all four analytical windows (sourced from `outputs/v3/gldas_split/gldas_multi_model_summary.csv`):

### Northwest Soil Moisture & Residual Partitioning Across Windows
1. **Full Record (2002–2026):**
   - Total Water Storage slope: **-1.25 cm/year**
   - Independent Soil Moisture ($\Delta\text{SMS}$) range: **[-0.12, -0.10] cm/year** (Noah 2.1: -0.10 cm/yr, $p = 0.0036$; VIC 2.1: -0.12 cm/yr, $p = 0.22$, `No detectable trend`).
   - Partitioned Residual (`groundwater + surface water + model error residual`): **[-1.12, -1.11] cm/year**.
2. **GRACE-1 Era (2002–2017):**
   - Total Water Storage slope: **-1.56 cm/year**
   - Independent Soil Moisture range: **[-0.54, -0.28] cm/year** (Noah: -0.28 cm/yr; VIC: -0.54 cm/yr).
   - Partitioned Residual range: **[-1.26, -1.05] cm/year**.
3. **GRACE Follow-On Era (2018–2026):**
   - Total Water Storage slope: **-1.67 cm/year** (below detection limit)
   - Independent Soil Moisture range: **[+0.05, +0.20] cm/year** (Noah: +0.05 cm/yr; VIC: +0.20 cm/yr; neither statistically significant).
   - Partitioned Residual range: **[-1.92, -1.70] cm/year**.
4. **Recent Window (2020–2026, Sensitivity Analysis Only):**
   - Total Water Storage slope: **-2.93 cm/year** (95% CI: **[-4.97, -0.78] cm/yr**, $p = 0.0107$, FDR $q = 0.0772$, `method-dependent`).
   - Independent Soil Moisture range: **[-0.37, -0.22] cm/year** (Noah: -0.22 cm/yr; VIC: -0.37 cm/yr).
   - Partitioned Residual range: **[-2.59, -2.38] cm/year**.

### Physical Interpretation & Methodological Quarantine
- **Physical Interpretation:** Across all windows, unsaturated root-zone soil moisture decline accounts for only a minor fraction of observed total water storage loss. Most of the decline is not accounted for by simulated soil moisture; groundwater and surface water cannot be separated here. This pattern is **consistent with, not proof of**, dry-season groundwater abstraction for intensive irrigated agriculture.
- **CLSM 2.2 Quarantine:** Catchment Land Surface Model (CLSM 2.2) directly assimilates GRACE TWS observations via an Ensemble Kalman Filter (EnKF). In CLSM, simulated soil moisture declines rapidly (-0.94 cm/yr in full_record), artificially compressing the residual to -0.33 cm/yr. Because assimilating GRACE into CLSM to evaluate GRACE involves circular logic, CLSM is reported separately for context and quarantined from the independent physical budget.

---

## 6. Honest Limitations & Resolution Pathways

To preserve scientific integrity, observed patterns are subject to the following limitations:

| Observational Pattern | What It Cannot Prove | What Would Be Needed to Resolve It |
|---|---|---|
| **1. Regional Water Depletion** | Coarse gravimetric resolution (~300 km) cannot resolve district, upazila, or municipal drawdown. | Satellite radar interferometry (InSAR) ground deformation and sub-basin subsidence modeling. |
| **2. Residual Subsurface Loss** | Satellites measure total column mass; we cannot separate deep groundwater from surface water bodies and wetlands. | Direct integration of Bangladesh Water Development Board (BWDB) nationwide in-situ piezometer well hydrographs. |
| **3. Agricultural Extraction Link** | We do not possess direct metered pumping logs across the Barind Tract. | Sub-district agricultural power consumption records and deep tubewell discharge registries from the Barind Multipurpose Development Authority (BMDA). |
| **4. Inter-Satellite Gap & Offset** | The 11-month transition (2017–2018) between GRACE and GRACE-FO introduces an upward offset (+9.15 cm, $p=0.028$) of unknown origin. | Continuous multi-satellite airborne gravimetry bridging or hydrodynamic data assimilation across the transition. |
| **5. Surrogate Placebo Sensitivity** | On a real-residual surrogate placebo (phase-randomized surrogates preserving autocorrelation and the real gap pattern), NW previously showed an elevated False Positive Rate of **17.6%** (82.5% CI coverage) under ESS-MK, whereas under an independent parametric AR(1) Monte Carlo null test, Calibrated ESS-MK passes nominal standards (NW FPR: 4.10%, coverage: 95.90%). | Both tests are reported to document sensitivity to empirical noise structure; longer continuous observational records will narrow this uncertainty. |
| **6. Precipitation Record Latency** | GPM IMERG Final Run V07B currently extends through September 2025. | Updating the processing stream when NASA GES DISC releases late-2025 and 2026 Final Run granules. |

---

## 7. Deliverables & File Directory Guide

For presentations, slide decks, and technical verification, refer to the following repository assets:

### A. Recommended for Presentations & Slide Decks
- `PROJECT_STATUS.md` *(this document)*: Plain-language executive guide and verified master numbers.
- `README.md`: Project specification, architectural summary, and command-line execution instructions.
- `outputs/v3/full_record/fig1_full_record_tws_trends.png`: 6-panel regional water storage trends across 2002–2026 with 95% confidence bands.
- `outputs/v3/exposure/fig_exposure_choropleth.png`: Choropleth map illustrating regional population and cropland exposure across the Northwest corridor.
- `outputs/v3/extremes/fig_imerg_extreme_indices_trends.png`: Multi-index time series showing stationary daily extreme precipitation.
- `outputs/v3/gldas_split/fig_storage_partition_multi_model.png`: Multi-model comparison illustrating independent soil moisture vs. deep residual deficit.

### B. Master Results Tables (For Spreadsheets & Citations)
- `outputs/v3/full_record/results_all_windows.csv`: Master results table containing all 336 statistical tests across all 4 windows, 6 regions, and 8 divisions with duality-aligned CIs and FDR q-values.
- `outputs/v3/full_record/three_way_slopes_and_transition.csv` & `.md`: Detailed 3-way Northwest slope sensitivity and satellite transition metrics.
- `outputs/v3/benchmark/benchmark_table.csv` & `.md`: Synthesis of regional rates against 6 published peer-reviewed studies.
- `outputs/v3/exposure/exposure_table.csv` & `.md`: Regional breakdown of 108.5 million residents (63.9%) and cropland exposure.
- `outputs/v3/extremes/imerg_extreme_indices_trends.csv` & `.md`: Exact trend values and duality-aligned CIs for all ETCCDI extreme rainfall metrics.
- `outputs/v3/gldas_split/gldas_multi_model_summary.csv` & `.md`: Multi-model GLDAS soil moisture and residual storage partitioning.

### C. Deep-Dive Audit Documentation (For Technical Inquiries)
- `NOTES.md`: Developer decision log detailing parameters, calibration validation, and audit trail.
- `outputs/v3/full_record/gap_calibration_report.json`: Monte Carlo simulation results verifying false-positive rate calibration.
- `outputs/v3/imerg_vs_power/imerg_vs_power_summary.md`: Statistical evaluation detailing the NASA POWER step artifact and GPM IMERG validation.

---

## 8. Consistency Fixes & Statistical Reconciliation (Audit Trail)

All reported figures have been audited against the primary single sources of truth (`outputs/v3/full_record/results_all_windows.csv` and `outputs/v3/full_record/gap_calibration_report.json`). No numbers have been manually approximated or typed without programmatic verification.

| Metric / Parameter | Location / Context | Old Value | New Value | Source of Truth / Methodological Justification |
|---|---|:---:|:---:|---|
| **NW full_record TWS 95% CI** | `exposure_table.csv`, `.md`, `NOTES.md` | `[-1.54, -0.96]` | **`[-1.50, -1.02]`** | Primary duality-aligned rank CI from `results_all_windows.csv` (`slope_ci_low`, `slope_ci_high`), replacing surrogate CI columns. |
| **SW full_record TWS 95% CI** | `exposure_table.csv`, `.md`, `NOTES.md` | `[-0.17, +0.08]` | **`[-0.20, +0.10]`** | Primary duality-aligned rank CI from `results_all_windows.csv` (`slope_ci_low`, `slope_ci_high`), replacing surrogate CI columns. |
| **NW full_record TWS FDR q-value** | `exposure_table.csv`, `.md` | `< 0.0001` or `0.0015` | **`< 0.0001`** | Direct within-window Benjamini-Hochberg FDR $q$-value from `results_all_windows.csv` ($q = 0.000078$). |
| **NW recent_2020 TWS 95% CI** | `README.md`, `NOTES.md` | `[-4.90, -0.57]` | **`[-4.97, -0.78]`** | Exact duality-aligned CI from `results_all_windows.csv` for 2020–2026 sensitivity window. |
| **National recent_2020 TWS 95% CI** | `README.md`, `NOTES.md` | `[-3.05, +0.94]` | **`[-2.53, +0.51]`** | Exact duality-aligned CI from `results_all_windows.csv` for 2020–2026 sensitivity window. |
| **National full_record TWS 95% CI** | `README.md` | `[-0.67, -0.35]` | **`[-0.66, -0.38]`** | Primary duality-aligned CI from `results_all_windows.csv` for full 24-year record. |
| **Depletion Corridor Exposed Population** | `PROJECT_STATUS.md`, `FIXES_REVIEW_REPORT.md`, `index.html`, `exposure_table.md` | `69.4 million` (40.9%) | **`108.5 million` (63.9%)** | Programmatic sum of NW (38.81M) + NE (24.05M) + Central (45.64M) from NASA SEDAC GPWv4 in `exposure_table.csv`. Old 69.4M unverified artifact deleted. |
| **Calibrated ESS-MK NW FPR** | `PROJECT_STATUS.md`, `FIXES_REVIEW_REPORT.md`, `index.html` | `4.60%` | **`4.10%`** | `gap_calibration_report.json` (`calibration_simulation.regional_ar1_null.NW.fpr_ess_mk` = 0.041). |
| **Calibrated ESS-MK NW CI Coverage** | `PROJECT_STATUS.md`, `FIXES_REVIEW_REPORT.md`, `index.html` | `95.40%` | **`95.90%`** | `gap_calibration_report.json` (`calibration_simulation.regional_ar1_null.NW.coverage_ess_mk` = 0.959). |
| **IMERG Satellite Observation Period** | `PROJECT_STATUS.md` | `2000–2025` | **`2002-01 to 2025-09`** | Verified GPM IMERG V07B Final Run data latency coverage. |
| **Daily Extreme Indices Catalog** | `PROJECT_STATUS.md` | `Rx1day, Rx5day, R95p, R99p, CDD, CWD, SDII (2003–2024)` | **Rx1day, Rx5day, days $\ge 50\text{ mm}$, annual total (2003–2024); monsoon total, monsoon Rx1day, monsoon Rx5day, monsoon days $\ge 50\text{ mm}$ (2002–2025)** | Matched exactly to indices computed in `v3/imerg_daily_extremes_pipeline.py` and `outputs/v3/extremes/imerg_extreme_indices_trends.csv`. |


---

## 9. Exploratory Seasonal Storage Response & Dry-Season Drawdown (Preliminary)

> **Status Label:** PRELIMINARY & EXPLORATORY ONLY.  
> These supplementary analyses test seasonal storage dynamics across multi-decadal observations. To maintain strict statistical governance, all exploratory results are documented separately in outputs/v3/seasonal/ and quarantined from the headline 336-test master table (
esults_all_windows.csv).

### A. Trend of Seasonal Storage Response Ratio (2002–2025)

1. **Physical Metric & Data Sources:**
   - Evaluates the multi-decadal stability of the seasonal storage response ratio, defined as:
     \text{Seasonal Storage Response Ratio} = \frac{\Delta\text{TWS}\text{ (cm)}}{0.1 \times P_{\text{monsoon}}\text{ (mm)}} \times 100\%
   - **Numerator ($\Delta\text{TWS}$):** Seasonal storage rebound alone, defined as the post-monsoon storage peak (maximum of August–November) minus the pre-monsoon dry season low (minimum of March–May) from CSR GRACE/GRACE-FO RL06.3 gravimetry (cm of total water storage).
   - **Denominator ({\text{monsoon}}$):** June–September 4-month cumulative rainfall from NASA GPM IMERG V07B Final Run (converted to cm liquid water equivalent).
2. **Satellite Gap Protocol:**
   - Incomplete seasons are dropped directly rather than interpolated. The 2017 season (lacking post-monsoon peak due to GRACE decommissioning) and 2018 season (lacking pre-monsoon low prior to GRACE-FO operations) are excluded, leaving **22 complete seasons** (2002–2016 and 2019–2025) in the main run.
   - A sensitivity run further excludes seasons within $\pm 6$ months of the satellite mission transition (2016–2019), leaving **20 complete seasons**.
3. **Statistical Findings (Main Run, N = 22 Seasons):**
   - **Northwest (NW):** Mean ratio = 39.6%, Theil-Sen slope = **+0.266 %/yr**, 95% CI: [-0.295, +0.836] %/yr,  = 0.3784$, exploratory FDR  = 0.5158$, MDS (80% power) = 0.700 %/yr $\rightarrow$ **No detectable trend**. The 95% CI is wide relative to the slope and spans zero.
   - **Northeast (NE):** Mean ratio = 30.1%, slope = **+0.203 %/yr**, 95% CI: [-0.079, +0.500] %/yr,  = 0.2147$, exploratory FDR  = 0.4294$, MDS = 0.400 %/yr $\rightarrow$ **No detectable trend**.
   - **Central:** Mean ratio = 42.2%, slope = **+0.387 %/yr**, 95% CI: [+0.046, +0.712] %/yr,  = 0.0369$, exploratory FDR  = 0.1105$, MDS = 0.500 %/yr $\rightarrow$ **No detectable trend** (raw  < 0.05$ does not survive exploratory Benjamini-Hochberg FDR control  < 0.05$).
   - **Southwest (SW):** Mean ratio = 33.0%, slope = **+0.138 %/yr**, 95% CI: [-0.164, +0.481] %/yr,  = 0.4298$, exploratory FDR  = 0.5158$, MDS = 0.500 %/yr $\rightarrow$ **No detectable trend**.
   - **Southeast (SE):** Mean ratio = 26.0%, slope = **+0.063 %/yr**, 95% CI: [-0.147, +0.228] %/yr,  = 0.6118$, exploratory FDR  = 0.6118$, MDS = 0.350 %/yr $\rightarrow$ **No detectable trend**.
   - **National Composite:** Mean ratio = 32.5%, slope = **+0.136 %/yr**, 95% CI: [+0.028, +0.355] %/yr,  = 0.0208$, exploratory FDR  = 0.1105$, MDS = 0.300 %/yr $\rightarrow$ **No detectable trend** (does not survive exploratory FDR control).
4. **Sensitivity Run (N = 20 Seasons):**
   - Central shows slope +0.476 %/yr ( = 0.0048$,  = 0.0212$) and National shows slope +0.151 %/yr ( = 0.0071$,  = 0.0212$), while NW, NE, SW, and SE show no detectable trend.

---

### B. Dry-Season Storage Drawdown & Cropland Overlay (2002–2026)

1. **Physical Metric & Exact Config Windows:**
   - Evaluates whether the annual dry-season storage drawdown has expanded or contracted over the 24-year satellite record:
     \text{Drawdown}_{y} = \text{TWS}_{\text{peak}, y} - \text{TWS}_{\text{min}, y+1}
   - Exact observation windows specified in config.json constants:
     - monsoon_peak_months: [8, 9, 10, 11] (August–November of year $)
     - ollowing_pre_monsoon_min_months: [3, 4, 5] (March–May of following year +1$)
2. **Missing Satellite Endpoint Protocol:**
   - Any annual cycle missing either endpoint is dropped rather than interpolated. The 2017–2018 cycle lacks both autumn 2017 peak and spring 2018 low due to the GRACE to GRACE-FO transition gap; exactly **1 year (2017)** drops out per region, leaving **23 valid observation cycles** (2002–2016 and 2018–2025) in the main run.
   - Sensitivity run excludes cycles touching the $\pm 6$-month buffer (2016–2018), leaving **21 valid cycles**.
3. **Statistical Trends & Descriptive Cropland Overlay:**
   - To prevent ecological fallacy and spurious regression across an aggregated sample of 5 regions (=5$), no cross-regional correlation or regression is performed. Regional metrics are reported descriptively alongside agricultural land cover (MODIS MCD12Q1) and population (NASA SEDAC GPWv4):

| Region | Cropland (%) | Population (2020) | Full-Record TWS Slope (cm/yr) | Full-Record TWS 95% CI | Mean Drawdown (cm) | Drawdown Slope (cm/yr) | 95% Confidence Interval | p-value | Exploratory FDR q | MDS (80% Power) | Verdict |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **NW** | 74.2% | 38.81M | -1.25 | [-1.50, -1.02] | 55.23 cm | **+0.011** | [-0.895, +0.813] | 1.0000 | 1.0000 | 1.300 cm/yr | No detectable trend |
| **NE** | 58.6% | 24.05M | -0.56 | [-0.70, -0.42] | 58.48 cm | **+0.086** | [-0.784, +0.675] | 0.8168 | 1.0000 | 1.300 cm/yr | No detectable trend |
| **Central** | 56.4% | 45.64M | -0.47 | [-0.62, -0.34] | 58.19 cm | **-0.014** | [-0.994, +0.745] | 0.9444 | 1.0000 | 1.300 cm/yr | No detectable trend |
| **SW** | 48.7% | 27.14M | -0.05 | [-0.20, +0.10] | 48.70 cm | **-0.095** | [-0.472, +0.243] | 0.5006 | 1.0000 | 0.700 cm/yr | No detectable trend |
| **SE** | 32.1% | 34.18M | -0.05 | [-0.17, +0.06] | 51.16 cm | **-0.055** | [-0.353, +0.241] | 0.6996 | 1.0000 | 0.550 cm/yr | No detectable trend |
| **National** | 57.8% | 169.83M | -0.51 | [-0.66, -0.38] | 53.24 cm | **-0.013** | [-0.593, +0.509] | 0.9703 | 1.0000 | 1.100 cm/yr | No detectable trend |

4. **Physical Interpretation:**
   - In all 5 regions and nationally, the annual dry-season drawdown trend shows **no detectable trend** ( \ge 0.50$,  = 1.0000$).
   - The seasonal cyclic amplitude of water storage (~48 to 58 cm) has remained stationary across 24 years, while the secular baseline total water storage has declined (-1.25 cm/yr in NW).

5. **Methodological Limits & Scope:**
   > Gravimetry measures total water storage (groundwater, soil moisture and surface water together). This analysis shows regional patterns that are consistent with dry-season agricultural water use but does not attribute them to irrigation pumping. Testing that would require metered pumping or electricity records (BMDA), BWDB well hydrographs, or irrigated-area mapping.
