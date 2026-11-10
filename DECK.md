# Bengal Hydro Detective: 24-Year Earth System Presentation Deck

**Project:** Bengal Hydro Detective  
**Challenge:** NASA Space Apps Challenge 2026 — *Be An Earth System Trend Detective!*  
**Team:** Tenstral (East West University, Bangladesh)  
**Live Hub:** [tenstral-nasa26.pages.dev](https://tenstral-nasa26.pages.dev)  
**Target Duration:** 240 Seconds (Local Presentation) | 30 Seconds (Global Pitch)  
**Status:** All findings PRELIMINARY

---

## Slide 1: Title & The Research Question (0:00 – 0:30)

### Visual Content
- **Headline:** Bengal Hydro Detective: Where Is Bangladesh's Stored Water Going?
- **Subtitle:** Resolving contradictory regional water observations under the same South Asian monsoon system (2002–2026).
- **Contrasting Regional Observations:**
  - *Northwest Corridor (Rajshahi & Rangpur):* Farmers and local reports describe dropping water tables, dry suction tubewells, and severe dry-season Boro rice water stress.
  - *Northeast Haor Basin (Sylhet & Mymensingh):* Communities face intense seasonal inundation, flash floods, and early pre-monsoon submergence.
- **The Core Scientific Question:**
  *Under the same monsoon, does total water storage decline across Bangladesh, and do regional trends differ statistically from rainfall?*

---

## Slide 2: Dual Satellite Earth Observations & Land Surface Partitioning (0:30 – 1:00)

### Visual Content
- **Gravity-Based Total Water Storage (TWS):**
  - *Mission:* NASA/German Aerospace Center (DLR/GFZ) CSR GRACE and GRACE-FO RL0603 Mascons.
  - *Period:* 2002-04 to 2026-07 (257 monthly solutions across 24 years).
  - *Physical Measurement:* Vertically integrated total water storage anomaly (groundwater, soil moisture, surface water, biomass) at ~300 km resolution.
- **Satellite Precipitation Ground Truth:**
  - *Mission:* NASA Global Precipitation Measurement (GPM) IMERG V07B (Final Run).
  - *Period:* 2002-01 to 2025-09 (fine 0.1° resolution, calibrated multi-satellite product).
- **Independent Soil Moisture Modeling:**
  - *Platform:* NASA GLDAS Land Surface Models (Noah 2.1 & VIC 4.1.2, 0–2 m unsaturated soil zone).
  - *Role:* Quarantines non-independent data (CLSM 2.2 assimilates GRACE) to isolate the independent topsoil component.

---

## Slide 3: Calibrated Statistical Trend Engine (1:00 – 1:30)

### Visual Content
- **Three-Tier Statistical Protocol:**
  1. *De-seasonalization:* Removes cyclical annual monsoon swings (32–42% seasonal amplitude) to reveal secular multi-decadal signals.
  2. *Robust Rate Estimation:* Theil-Sen slope estimator across continuous and epoch-partitioned series.
  3. *Autocorrelation-Corrected Significance:* Calibrated Effective Sample Size Mann-Kendall (ESS-MK) test with AR(1) pre-whitening and surrogate red-noise null validation.
- **Multiple Testing & Multi-Window Framework:**
  - *FDR Control:* Benjamini-Hochberg False Discovery Rate control applied strictly within families (m = 36 tests per window).
  - *Four Analytical Windows:* Full 24-year record (2002–2026), GRACE era (2002–2017), GRACE-FO era (2018–2026), and recent sensitivity window (2020–2026).

---

## Slide 4: Key Empirical Findings — Macro-Regional Storage & Rainfall (1:30 – 2:00)

### Visual Content
- **Regional Total Water Storage (Full Record 2002–2026):**
  - *Northwest (Rajshahi + Rangpur):* **-1.25 cm/yr** (95% CI: `[-1.50, -1.02]`; -0.39 km³/yr; FDR q < 0.0001; Verdict: Significant depletion).
  - *Northeast (Sylhet + Mymensingh):* **-0.56 cm/yr** (95% CI: `[-0.70, -0.42]`; -0.12 km³/yr; FDR q < 0.0001; Verdict: Significant depletion).
  - *Central (Dhaka Division):* **-0.47 cm/yr** (95% CI: `[-0.62, -0.34]`; -0.08 km³/yr; FDR q < 0.0001; Verdict: Significant depletion).
  - *Southwest (Khulna + Barishal):* **-0.05 cm/yr** (95% CI: `[-0.20, +0.10]`; Verdict: No detectable trend).
  - *Southeast (Chattogram + CHT):* **-0.05 cm/yr** (95% CI: `[-0.17, +0.06]`; Verdict: No detectable trend).
  - *National Composite:* **-0.51 cm/yr** (95% CI: `[-0.66, -0.38]`; -0.63 km³/yr; Verdict: Significant depletion).
- **Precipitation Findings (GPM IMERG):**
  - *All 5 Macro-Regions:* **No detectable trend** in precipitation (NW: -1.9 mm/yr, 95% CI `[-11.0, +4.5]`). Wide confidence intervals indicate high natural variability rather than absence of variation.
- **Northwest Transition Modeling Range:**
  - Accounting for the inter-satellite step (+9.15 cm between GRACE and GRACE-FO), the Northwest depletion slope spans **-1.81 to -1.25 cm/yr**.

---

## Slide 5: Storage Partitioning, Exposure & Seasonal Baseline (2:00 – 2:30)

### Visual Content
- **GLDAS Physical Partitioning:**
  - *Soil Moisture Share:* Unsaturated topsoil moisture (0–2 m, Noah and VIC) trends explain only a minor part (**-0.12 to -0.10 cm/yr**, ~8% to 10% of total storage loss).
  - *Subsurface Residual:* Total storage minus GLDAS topsoil leaves an unpartitioned residual of **-1.12 to -1.11 cm/yr** (labeled: *groundwater + surface water + model error residual*).
- **Socioeconomic Exposure:**
  - **108.5 million people** (63.9% of Bangladesh's 2020 population) reside in regions experiencing significant total water storage decline (NW: 38.8M; Central: 45.6M; NE: 24.1M).
  - Northwest cropland exposure: 74.2% of surface land area is classified as cropland (MODIS MCD12Q1).
- **Seasonal Baseline Dynamics:**
  - Mean seasonal storage swing (peak minus pre-monsoon low) spans **49 to 58 cm** across all regions with no detectable change.
  - The storage decline reflects a persistent multi-decadal shift in the baseline, not an expanding seasonal drawdown swing.

---

## Slide 6: Calibrated Between-Region Comparisons (2:30 – 3:00)

### Visual Content
- **Paired Difference Analysis (Effect Sizes Only):**
  - Evaluated on regional difference series using Calibrated ESS-MK. Exact p-values are withheld due to circular-shift placebo overconfidence.
  - *NW vs. SW & SE:* Northwest declines about **1.2 cm/yr faster** than Southwest and Southeast (deltas: -1.20 and -1.19 cm/yr; non-overlapping CIs).
  - *NE & Central vs. SW & SE:* Northeast and Central decline about **0.5 cm/yr faster** than Southwest and Southeast (deltas: -0.54 to -0.45 cm/yr).
  - *SW vs. SE:* Southwest and Southeast are **indistinguishable** (delta: +0.01 cm/yr; 95% CI: `[-0.03, +0.04]`).
  - *Rainfall Pairs:* No rainfall pair differs across the country.
  - *Descriptive Precaution:* Northeast vs. Central difference is descriptive only (individual regional CIs overlap).

---

## Slide 7: Methodological Limitations & Epistemic Humility (3:00 – 3:30) [REQUIRED SLIDE]

### Visual Content
- **1. Coarse Spatial Footprint:**
  - GRACE mascons resolve total mass changes at ~300 km. It is a regional satellite-derived series, not a measurement of local water tables or individual village tubewell lift.
- **2. Spatial Signal Leakage & Adjacency:**
  - Macro-regions are contiguous; shared signal smoothing can partially attenuate localized boundaries.
- **3. Intersatellite Gap & Step Offset:**
  - A +9.15 cm step between GRACE (ending 2017) and GRACE-FO (starting 2018) influences single-line regression; reporting the -1.81 to -1.25 cm/yr range ensures transparency.
- **4. Lack of Direct Well Validation:**
  - Satellite gravimetry has not yet been reconciled against Bangladesh Water Development Board (BWDB) in-situ piezometric well networks.
- **5. Causal Boundary:**
  - Observations are consistent with dry-season agricultural water use, but not attributable with satellite data alone. Pumping attribution requires local metering and extraction records.

---

## Slide 8: Detection Limits — Why "No Detectable Trend" Is Not "No Change" (3:30 – 4:00) [REQUIRED SLIDE]

### Visual Content
- **Understanding Statistical Detection Limits:**
  - "No detectable trend" does NOT mean "no change" or that rainfall/storage has zero physical variation.
  - High natural interannual variability in monsoon cloudbursts widens confidence intervals, making modest shifts undetectable over short windows.
- **Empirical Minimum Detectable Slope (MDS at 80% Power):**
  - *Full 24-Year Record:* NW TWS MDS is **0.32 cm/yr**. With 257 monthly observations, statistical power is sufficient to detect the -1.25 cm/yr depletion.
  - *Recent 2020–2026 Window:* NW TWS MDS degrades to **2.34 cm/yr**. With only 79 months, the statistical threshold expands dramatically; recent windows are below the detection limit.
- **Interactive Decision Support Hub:**
  - Live at **[tenstral-nasa26.pages.dev](https://tenstral-nasa26.pages.dev)**: 24-year timeline scrubber, multi-sensor studio, bilingual summaries, and complete 336-test audit registry.
- **Next Research Steps:**
  - Ingesting BWDB in-situ groundwater monitoring hydrographs, agricultural electricity pumping indices, and transboundary upstream river discharge gauges.
