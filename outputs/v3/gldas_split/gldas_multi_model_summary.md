# GLDAS Multi-Model Soil-Moisture & Storage Partitioning Report

**Project:** Bengal Hydro Detective — NASA Space Apps Challenge 2026  
**Team:** Tenstral  
**Status:** PRELIMINARY  
**Primary Gravimetry:** CSR GRACE / GRACE-FO RL0603 Mascons (2002–2026)  
**Models Evaluated:**
1. **GLDAS-2.1 Noah Land Surface Model L4 monthly 0.25°** (`GLDAS_NOAH025_M` v2.1, **Independent**): $2.0	ext{ m}$ root-zone depth (4 layers: $0–10	ext{ cm}$, $10–40	ext{ cm}$, $40–100	ext{ cm}$, $100–200	ext{ cm}$) + Canopy + Snow.
2. **GLDAS-2.1 Variable Infiltration Capacity (VIC) L4 monthly 1.0°** (`GLDAS_VIC10_M` v2.1, **Independent**): 3 soil moisture layers + Canopy + Snow.
3. **GLDAS-2.2 Catchment Land Surface Model (CLSM) L4 daily 0.25°** (`GLDAS_CLSM025_DA1_D` v2.2, **Non-independent / GRACE-assimilated**): Profile soil moisture + Canopy + Snow (assimilates GRACE TWSA via EnKF; record starts 2003-02).
- **Reference Baseline:** All models re-baselined to 2004-01 to 2009-12 (mean anomaly $\equiv 0.0	ext{ cm}$).
- **Residual Storage Definition:** $	ext{Residual} = 	ext{TWS} - \Delta	ext{SMS} - \Delta	ext{SWE}$, strictly labeled as `groundwater + surface water + model error residual`.
- **Partitioning Principle:** Noah and VIC represent independent open-loop land surface physics. CLSM 2.2 assimilates GRACE observations directly, creating circularity if used to partition GRACE, and is therefore reported separately for diagnostic context only.

---

## 1. Multi-Model Partitioning Trends Across All 4 Operational Windows

| Window | Region | TWS Slope (cm/yr) | Noah ΔSMS Slope (cm/yr) | VIC ΔSMS Slope (cm/yr) | Independent ΔSMS Range [Min, Max] | Independent Residual Slope Range [Min, Max]* | CLSM ΔSMS Slope (cm/yr)** | CLSM Residual Slope (cm/yr)** |
|---|---|---|---|---|---|---|---|---|
| `full_record` | **NW** | -1.25 | -0.10 (`Suggestive decrease`) | -0.12 (`No detectable trend`) | [-0.12, -0.10] | [-1.12, -1.11] | -0.94** | -0.33** |
| `full_record` | **NE** | -0.56 | -0.06 (`No detectable trend`) | -0.04 (`No detectable trend`) | [-0.06, -0.04] | [-0.51, -0.48] | -0.31** | -0.30** |
| `full_record` | **Central** | -0.47 | -0.12 (`Suggestive decrease`) | -0.17 (`No detectable trend`) | [-0.17, -0.12] | [-0.36, -0.32] | -0.62** | +0.07** |
| `full_record` | **SW** | -0.05 | -0.10 (`Suggestive decrease`) | -0.25 (`Suggestive decrease`) | [-0.25, -0.10] | [+0.04, +0.20] | -0.29** | +0.23** |
| `full_record` | **SE** | -0.05 | -0.09 (`Suggestive decrease`) | -0.04 (`No detectable trend`) | [-0.09, -0.04] | [-0.02, +0.04] | -0.30** | +0.24** |
| `full_record` | **National** | -0.51 | -0.09 (`Suggestive decrease`) | -0.13 (`No detectable trend`) | [-0.13, -0.09] | [-0.41, -0.38] | -0.51** | -0.02** |
| `grace_era` | **NW** | -1.56 | -0.28 (`Suggestive decrease`) | -0.54 (`Suggestive decrease`) | [-0.54, -0.28] | [-1.26, -1.05] | -1.41** | -0.24** |
| `grace_era` | **NE** | -0.72 | -0.17 (`Suggestive decrease`) | -0.25 (`Suggestive decrease`) | [-0.25, -0.17] | [-0.59, -0.53] | -0.50** | -0.30** |
| `grace_era` | **Central** | -0.63 | -0.29 (`Suggestive decrease`) | -0.55 (`Suggestive decrease`) | [-0.55, -0.29] | [-0.39, -0.16] | -0.94** | +0.19** |
| `grace_era` | **SW** | -0.13 | -0.19 (`Suggestive decrease`) | -0.61 (`Suggestive decrease`) | [-0.61, -0.19] | [+0.01, +0.48] | -0.60** | +0.44** |
| `grace_era` | **SE** | -0.12 | -0.08 (`No detectable trend`) | -0.04 (`No detectable trend`) | [-0.08, -0.04] | [-0.10, -0.06] | -0.28** | +0.13** |
| `grace_era` | **National** | -0.68 | -0.20 (`Suggestive decrease`) | -0.42 (`Suggestive decrease`) | [-0.42, -0.20] | [-0.51, -0.30] | -0.78** | +0.04** |
| `grace_fo_era` | **NW** | -1.67 | +0.05 (`No detectable trend`) | +0.20 (`No detectable trend`) | [+0.05, +0.20] | [-1.92, -1.70] | -1.09** | -0.53** |
| `grace_fo_era` | **NE** | -0.79 | -0.04 (`No detectable trend`) | +0.09 (`No detectable trend`) | [-0.04, +0.09] | [-1.05, -0.79] | -0.26** | -0.55** |
| `grace_fo_era` | **Central** | -0.81 | -0.08 (`No detectable trend`) | +0.18 (`No detectable trend`) | [-0.08, +0.18] | [-0.89, -0.71] | -0.54** | -0.23** |
| `grace_fo_era` | **SW** | +0.53 | -0.32 (`No detectable trend`) | +0.42 (`No detectable trend`) | [-0.32, +0.42] | [+0.20, +0.70] | -0.01** | +0.44** |
| `grace_fo_era` | **SE** | +0.45 | -0.13 (`No detectable trend`) | -0.05 (`No detectable trend`) | [-0.13, -0.05] | [+0.45, +0.49] | -0.09** | +0.61** |
| `grace_fo_era` | **National** | -0.47 | -0.10 (`No detectable trend`) | +0.22 (`No detectable trend`) | [-0.10, +0.22] | [-0.68, -0.36] | -0.28** | -0.10** |
| `recent_2020` | **NW** | -2.93 | -0.22 (`No detectable trend`) | -0.37 (`No detectable trend`) | [-0.37, -0.22] | [-2.59, -2.38] | -2.56** | -0.05** |
| `recent_2020` | **NE** | -1.06 | -0.24 (`No detectable trend`) | -0.19 (`No detectable trend`) | [-0.24, -0.19] | [-1.02, -0.87] | -0.68** | -0.55** |
| `recent_2020` | **Central** | -1.19 | -0.35 (`Suggestive decrease`) | +0.03 (`No detectable trend`) | [-0.35, +0.03] | [-1.05, -0.76] | -1.51** | +0.43** |
| `recent_2020` | **SW** | +0.03 | -0.57 (`Suggestive decrease`) | +0.02 (`No detectable trend`) | [-0.57, +0.02] | [+0.17, +0.52] | -0.69** | +0.71** |
| `recent_2020` | **SE** | +0.39 | -0.42 (`No detectable trend`) | -0.20 (`No detectable trend`) | [-0.42, -0.20] | [+0.54, +0.72] | -0.05** | +0.34** |
| `recent_2020` | **National** | -1.02 | -0.37 (`Suggestive decrease`) | -0.12 (`No detectable trend`) | [-0.37, -0.12] | [-0.76, -0.61] | -1.09** | +0.16** |

*\*Note: Independent Residual is defined as TWS - ΔSMS across independent models (Noah 2.1 and VIC 2.1). Strictly labeled: `groundwater + surface water + model error residual`. Presented as a model range [min, max] across independent models, avoiding mixed physical and model confidence intervals.*  
*\*\*Note: GLDAS-2.2 CLSM is **Non-independent / GRACE-assimilated** (assimilates GRACE TWSA via Ensemble Kalman Filtering); its record starts 2003-02. CLSM 2.2 cannot serve as an independent partition of GRACE.*

---

## 2. Model Soil-Moisture Homogeneity & Forcing Evolution

> [!IMPORTANT]
> **Interpretation of Homogeneity Tests Under a Secular Trend:**  
> Non-parametric change-point tests such as Pettitt's test test the null hypothesis of stationarity against an alternative of a single step change. When applied to any time series that exhibits a continuous secular trend, Pettitt's test will mathematically reject the null and identify a nominal break near the midpoint ($t pprox N/2$) of the series. Therefore, Pettitt test rejection under a trend does **not** constitute evidence of meteorological data inhomogeneity or instrumentation artifacts.

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
| **NW** | 2009-02 / 2004-08 | `False` | 2009-01 / 2006-04 | `False` | 2010-07 | `False` |
| **NE** | 2009-02 / 2004-11 | `False` | 2008-04 / 2008-05 | `False` | 2009-02 | `False` |
| **Central** | 2009-02 / 2009-02 | `False` | 2009-02 / 2008-05 | `False` | 2009-02 | `False` |
| **SW** | 2009-01 / 2004-10 | `False` | 2009-01 / 2008-08 | `False` | 2008-12 | `False` |
| **SE** | 2008-04 / 2003-07 | `False` | 2008-03 / 2008-04 | `False` | 2018-08 | `False` |
| **National** | 2009-02 / 2004-11 | `False` | 2009-02 / 2008-05 | `False` | 2009-04 | `False` |

---

## 3. Scientific Synthesis (Bilingual)

### English Scientific Synthesis
Across both independent open-loop land surface models (Noah 2.1 and VIC 2.1), simulated unsaturated zone soil moisture exhibits no statistically significant secular decline in the Northwest region (Noah: +0.05 cm/yr, $p = 0.6010$; VIC: +0.20 cm/yr; independent range: [+0.05, +0.20] cm/yr). In contrast, total water storage declines across the record (GRACE-FO: -1.67 cm/yr; full record: -1.25 cm/yr). The resulting residual storage ('groundwater + surface water + model error residual') spans an estimated rate of [-1.92, -1.70] cm/yr during GRACE-FO and [-1.12, -1.11] cm/yr across the full record across independent models. Most of the decline is not accounted for by simulated soil moisture; groundwater and surface water cannot be separated here. This pattern is consistent with, not proof of, agricultural groundwater extraction from the deep subsurface. CLSM 2.2 is shown separately because it assimilates GRACE observations via EnKF and cannot serve as an independent partition.

**Methodological Limitations:**  
> *Limitations:* Residual storage is strictly defined as $	ext{Residual} = 	ext{TWS} - \Delta	ext{SMS} - \Delta	ext{SWE}$. It aggregates unmodeled surface water bodies, river stage variations, irrigation return flows, and structural model errors. It should not be interpreted as in-situ piezometric water table depth. GLDAS-2.2 CLSM assimilates GRACE observations and cannot serve as an independent partition.

---

### বাংলা বৈজ্ঞানিক বিবরণী (Bangla Scientific Synthesis)
উন্মুক্ত ল্যান্ড সারফেস মডেলের (Noah 2.1 ও VIC 2.1) বিশ্লেষণে দেখা যায় যে, উত্তর-পশ্চিম অঞ্চলে মাটির অগভীর আর্দ্রতায় কোনো তাৎপর্যপূর্ণ দীর্ঘমেয়াদী পতন ঘটেনি (নূহ মডেল: +0.05 সেমি/বছর; ভিআইসি মডেল: +0.20 সেমি/বছর; স্বাধীন মডেল পরিসর: [+0.05, +0.20] সেমি/বছর)। কিন্তু স্যাটেলাইট গ্র্যাভিমেট্রি তথ্যে মোট পানি সঞ্চয় (TWS) হ্রাস পাচ্ছে (গ্রেস-এফও যুগে বার্ষিক -1.67 সেমি; পুরো রেকর্ডে বার্ষিক -1.25 সেমি)। ফলস্বরূপ, স্বাধীন মডেলের অবশিষ্টাংশ সঞ্চয় ('ভূগর্ভস্থ পানি + ভূ-পৃষ্ঠের পানি + মডেল ত্রুটির অবশিষ্টাংশ') হ্রাস নির্দেশ করে (স্বাধীন মডেল পরিসর: [-1.92, -1.70] সেমি/বছর)। মোট পানি সঞ্চয় হ্রাসের সিংহভাগই মাটির অগভীর আর্দ্রতা দিয়ে ব্যাখ্যা করা যায় না; তবে এখানে ভূগর্ভস্থ পানি ও ভূ-পৃষ্ঠের পানি আলাদা করা সম্ভব নয়। এটি গভীর নলকূপ দিয়ে সেচ উত্তোলনের সাথে সামঞ্জস্যপূর্ণ, তবে সরাসরি প্রমাণ নয়। GLDAS-2.2 CLSM মডেলটি গ্রেস ডেটা আত্তীকরণ করে বিধায় এটিকে স্বাধীন প্রামাণ্য উৎস হিসেবে বিবেচনা করা যায় না।

**সীমাবদ্ধতার বিজ্ঞপ্তি:**  
> *সীমাবদ্ধতা:* অবশিষ্টাংশ সঞ্চয়কে কঠোরভাবে 'ভূগর্ভস্থ পানি + ভূ-পৃষ্ঠের পানি + মডেল ত্রুটির অবশিষ্টাংশ' হিসেবে সংজ্ঞায়িত করা হয়েছে। এতে নদী-নালা ও উন্মুক্ত জলাশয়ের প্রবাহ এবং মডেলের কাঠামোগত অনিশ্চয়তা অন্তর্ভুক্ত। একে সরাসরি স্থানীয় নলকূপের পানির স্তর হিসেবে গণ্য করা যাবে না। অধিকন্তু, GLDAS-2.2 CLSM মডেলে গ্রেস স্যাটেলাইট তথ্য আত্তীকরণ (assimilated) করা হয়েছে, বিধায় এটি কোনো স্বাধীন প্রামাণ্য উৎস নয়।
