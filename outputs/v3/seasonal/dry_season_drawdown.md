# Exploratory Dry-Season Drawdown Trends & Cropland Overlay (2002–2026)

**Status:** PRELIMINARY & EXPLORATORY ONLY
**Generated:** 2026-11-10 11:04:19
**Methodology:** Calibrated ESS-MK Theil-Sen regression with duality-aligned 95% CIs and descriptive overlay.

---

## 1. Metric Definition & Exact Observation Windows
- **Dry-Season Drawdown:** Defined as the total water storage difference between the annual monsoon peak and the subsequent pre-monsoon minimum:
  $$\text{Drawdown}_{y} = \text{TWS}_{\text{peak}, y} - \text{TWS}_{\text{min}, y+1}$$
- **Config Constants (from `config.json`):**
  - Monsoon Peak Months (`monsoon_peak_months`): `[8, 9, 10, 11]` (Aug/Sep/Oct/Nov of year $y$)
  - Following Pre-Monsoon Low Months (`following_pre_monsoon_min_months`): `[3, 4, 5]` (Mar/Apr/May of year $y+1$)
  - Transition Gap Years (`transition_gap_years`): `[2017, 2018]`
  - Transition Buffer (`transition_buffer_months`): `6` months
- **Missing Endpoint Protocol:** Any year missing either endpoint is dropped directly rather than interpolated.
  - Cycle 2017–2018 lacks the autumn 2017 peak and spring 2018 low due to the 11-month GRACE to GRACE-FO transition gap.
  - Consequently, exactly **1 year (2017)** drops out per region, leaving **23 valid observation cycles** (2002–2016 [15] and 2018–2025 [8]) in the main run.
- **Sensitivity Run:** Excludes cycles whose endpoints touch the $\pm 6$-month buffer around the gap (2016, 2017, 2018), leaving **21 valid cycles**.
- **Exploratory Multiple Testing:** Benjamini-Hochberg FDR correction is calculated within these 6 exploratory tests only.

---

## 2. Dry-Season Drawdown Trends (Main Run: N = 23 Cycles, 2002–2026)

| Region | N | Mean Drawdown (cm) | Theil-Sen Slope (cm/yr) | 95% Confidence Interval | p-value (ESS-MK) | Exploratory FDR q | MDS (80% Power) | Verdict |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **NW** (Northwest (Rajshahi + Rangpur)) | 23 | 55.23 cm | +0.011 cm/yr | [-0.895, +0.813] | 1.0000 | 1.0000 | 1.300 cm/yr | No detectable trend |
| **NE** (Northeast (Sylhet + Mymensingh)) | 23 | 58.48 cm | +0.086 cm/yr | [-0.784, +0.675] | 0.8168 | 1.0000 | 1.300 cm/yr | No detectable trend |
| **Central** (Central (Dhaka)) | 23 | 58.19 cm | -0.014 cm/yr | [-0.994, +0.745] | 0.9444 | 1.0000 | 1.300 cm/yr | No detectable trend |
| **SW** (Southwest (Khulna + Barishal)) | 23 | 48.70 cm | -0.095 cm/yr | [-0.472, +0.243] | 0.5006 | 1.0000 | 0.700 cm/yr | No detectable trend |
| **SE** (Southeast (Chattogram)) | 23 | 51.16 cm | -0.055 cm/yr | [-0.353, +0.241] | 0.6996 | 1.0000 | 0.550 cm/yr | No detectable trend |
| **National** (National Composite (All 8 Divisions)) | 23 | 53.24 cm | -0.013 cm/yr | [-0.593, +0.509] | 0.9703 | 1.0000 | 1.100 cm/yr | No detectable trend |

---

## 3. Sensitivity Analysis (Transition-Buffer Excluded: N = 21 Cycles)

| Region | N | Mean Drawdown (cm) | Theil-Sen Slope (cm/yr) | 95% Confidence Interval | p-value (ESS-MK) | Exploratory FDR q | MDS (80% Power) | Verdict |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **NW** (Northwest (Rajshahi + Rangpur)) | 21 | 57.29 cm | +0.102 cm/yr | [-0.381, +0.644] | 0.6946 | 0.8800 | 0.750 cm/yr | No detectable trend |
| **NE** (Northeast (Sylhet + Mymensingh)) | 21 | 60.55 cm | +0.174 cm/yr | [-0.315, +0.526] | 0.4149 | 0.8800 | 0.700 cm/yr | No detectable trend |
| **Central** (Central (Dhaka)) | 21 | 60.20 cm | +0.044 cm/yr | [-0.297, +0.461] | 0.7858 | 0.8800 | 0.550 cm/yr | No detectable trend |
| **SW** (Southwest (Khulna + Barishal)) | 21 | 49.65 cm | -0.064 cm/yr | [-0.253, +0.148] | 0.5260 | 0.8800 | 0.300 cm/yr | No detectable trend |
| **SE** (Southeast (Chattogram)) | 21 | 52.10 cm | -0.023 cm/yr | [-0.197, +0.173] | 0.8800 | 0.8800 | 0.300 cm/yr | No detectable trend |
| **National** (National Composite (All 8 Divisions)) | 21 | 54.81 cm | +0.052 cm/yr | [-0.234, +0.302] | 0.7398 | 0.8800 | 0.450 cm/yr | No detectable trend |

---

## 4. Descriptive Cropland & Total Water Storage Overlay

The table below overlays regional agricultural cropland fraction (MODIS MCD12Q1), human population (NASA SEDAC GPWv4), 24-year full-record secular total water storage slope (`results_all_windows.csv`), and annual dry-season drawdown trend. To prevent ecological fallacy and spurious inference from a sample of 5 spatial aggregations, no correlation or regression is computed across regions; data are presented strictly for descriptive comparison.

| Region | Cropland Fraction (%) | Population (2020) | Full-Record TWS Slope (cm/yr) | Full-Record TWS 95% CI | Mean Drawdown (cm) | Drawdown Trend (cm/yr) | Drawdown Verdict |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **NW** | 74.2% | 38.81M | -1.25 | [-1.50, -1.02] | 55.23 cm | +0.011 | No detectable trend |
| **NE** | 58.6% | 24.05M | -0.56 | [-0.70, -0.42] | 58.48 cm | +0.086 | No detectable trend |
| **Central** | 56.4% | 45.64M | -0.47 | [-0.62, -0.34] | 58.19 cm | -0.014 | No detectable trend |
| **SW** | 48.7% | 27.14M | -0.05 | [-0.20, +0.10] | 48.70 cm | -0.095 | No detectable trend |
| **SE** | 32.1% | 34.18M | -0.05 | [-0.17, +0.06] | 51.16 cm | -0.055 | No detectable trend |
| **National** | 57.8% | 169.83M | -0.51 | [-0.66, -0.38] | 53.24 cm | -0.013 | No detectable trend |

---

## 5. Methodological Limits & Scope

> Gravimetry measures total water storage (groundwater, soil moisture and surface water together). This analysis shows regional patterns that are consistent with dry-season agricultural water use but does not attribute them to irrigation pumping. Testing that would require metered pumping or electricity records (BMDA), BWDB well hydrographs, or irrigated-area mapping.
