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
1. **NASA/CSR GRACE and GRACE Follow-On satellite gravimetry:** Twin satellite missions measuring vertically integrated regional mass changes, capturing total water storage (TWS)—including surface water bodies, unsaturated topsoil moisture, and deep aquifers.
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
   - The southern delta is buffered by estuarine river networks, coastal mangrove wetlands (the Sundarbans), and lower agricultural dry-season groundwater abstraction relative to the north.

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

### B. Satellite Precipitation with GPM IMERG (Stationary Rainfall)
Replacing atmospheric reanalysis with NASA's radar and microwave satellite precipitation constellation (**GPM IMERG V07B Final Run**) eliminated the artificial jump:
- Nationally, annual IMERG rainfall trend is **+2.04 mm/year** (95% CI: **[-7.70, +12.45] mm/yr**, $p = 0.64$, FDR $q = 0.9342$), showing **no detectable trend** within natural multi-year variability.
- In the Northwest, annual rainfall trend is **-1.91 mm/year** (95% CI: **[-11.04, +4.48] mm/yr**, $p = 0.54$, FDR $q = 0.8968$), also showing **no detectable trend**.
- Over the 24-year satellite observational period (2000–2025), national IMERG precipitation averages **2,366 mm/year**.
- *Data Latency Notice:* GPM IMERG Final data currently extends through September 2025 due to standard NASA production latency, truncating the final 10 months of the 2002–2026 gravimetry analysis window.

### C. Extreme Rainfall and Flood Dynamics
- **Stationary Extreme Indices:** Daily precipitation extremes (Rx1day, Rx5day, R95p, R99p, CDD, CWD, SDII) show no statistically significant trend across Bangladesh between 2003 and 2024.
- **Flood Response and Storage Recovery (Untested Hypothesis):** Historical flood events (2004, 2007, 2017, 2020, 2022 Sylhet) correspond to large transient storage surges (e.g., storage anomalies spiked by +41 cm in 2007 and +33 cm in 2004):
  - An untested hypothesis frequently cited in regional hydrogeology suggests that topsoil saturation and floodplain drainage limit the proportion of floodwaters that recharge deeper aquifers, allowing subsequent dry-season abstraction to outpace seasonal recharge.
  - However, this mechanism remains an unverified hypothesis in this study; satellite gravimetry captures vertically integrated bulk mass and cannot measure aquifer infiltration rates directly without in-situ piezometer hydrographs.

---

## 5. Storage Partitioning: Multi-Model Soil Moisture Findings

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
4. **Recent Window (2020–2026):**
   - Total Water Storage slope: **-2.93 cm/year** (`method-dependent`)
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
| **5. Surrogate Placebo Sensitivity** | On a real-residual surrogate placebo (phase-randomized surrogates preserving autocorrelation and the real gap pattern), NW previously showed an elevated False Positive Rate of **17.6%** (82.5% CI coverage) under ESS-MK, whereas under an independent parametric AR(1) Monte Carlo null test, Calibrated ESS-MK passes nominal standards (NW FPR: 4.60%, coverage: 95.40%). | Both tests are reported to document sensitivity to empirical noise structure; longer continuous observational records will narrow this uncertainty. |
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
- `outputs/v3/exposure/exposure_table.csv` & `.md`: Regional breakdown of 69.4 million residents and cropland exposure.
- `outputs/v3/extremes/imerg_extreme_indices_trends.csv` & `.md`: Exact trend values and duality-aligned CIs for all ETCCDI extreme rainfall metrics.
- `outputs/v3/gldas_split/gldas_multi_model_summary.csv` & `.md`: Multi-model GLDAS soil moisture and residual storage partitioning.

### C. Deep-Dive Audit Documentation (For Technical Inquiries)
- `NOTES.md`: Developer decision log detailing parameters, calibration validation, and audit trail.
- `outputs/v3/full_record/gap_calibration_report.json`: Monte Carlo simulation results verifying false-positive rate calibration.
- `outputs/v3/imerg_vs_power/imerg_vs_power_summary.md`: Statistical evaluation detailing the NASA POWER step artifact and GPM IMERG validation.
