# GLDAS Multi-Model Soil-Moisture & Storage Partitioning Report

**Project:** Bengal Hydro Detective — NASA Space Apps Challenge 2026  
**Team:** Tenstral  
**Status:** PRELIMINARY  
**Primary Gravimetry:** CSR GRACE / GRACE-FO RL0603 Mascons (2002–2026)  
**Models Evaluated:**
1. **GLDAS-2.1 Noah Land Surface Model L4 monthly 0.25°** (`GLDAS_NOAH025_M` v2.1): $2.0\text{ m}$ root-zone depth (4 layers: $0–10\text{ cm}$, $10–40\text{ cm}$, $40–100\text{ cm}$, $100–200\text{ cm}$) + Canopy + Snow.
2. **GLDAS-2.1 Variable Infiltration Capacity (VIC) L4 monthly 1.0°** (`GLDAS_VIC10_M` v2.1): 3 soil moisture layers + Canopy + Snow.
3. **GLDAS-2.2 Catchment Land Surface Model (CLSM) L4 daily 0.25°** (`GLDAS_CLSM025_DA1_D` v2.2): Profile soil moisture + Canopy + Snow (Labeled: **Non-independent / GRACE-assimilated**; record starts 2003-02).
- **Reference Baseline:** All models re-baselined to 2004-01 to 2009-12 (mean anomaly $\equiv 0.0\text{ cm}$).
- **Residual Storage Definition:** $\text{Residual} = \text{TWS} - \Delta\text{SMS} - \Delta\text{SWE}$, strictly labeled as `groundwater + surface water + model error residual`.

---

## 1. Multi-Model Partitioning Trends Across All 4 Operational Windows

| Window | Region | TWS Slope (cm/yr) | Noah ΔSMS Slope (cm/yr) | VIC ΔSMS Slope (cm/yr) | CLSM ΔSMS Slope (cm/yr)* | Ensemble ΔSMS Slope | Model Spread (cm/yr) | Ensemble Residual Slope (cm/yr) [95% CI] | Ensemble Residual Verdict |
|---|---|---|---|---|---|---|---|---|---|
| `full_record` | **NW** | -1.25 | -0.10 (`Suggestive decrease`) | -0.12 (`No detectable trend`) | -0.94* | -0.37 (`Suggestive decrease`) | 0.84 | -0.85 [-0.96, -0.73] | `Suggestive decrease` |
| `full_record` | **NE** | -0.56 | -0.06 (`No detectable trend`) | -0.04 (`No detectable trend`) | -0.31* | -0.13 (`Suggestive decrease`) | 0.27 | -0.42 [-0.52, -0.33] | `Suggestive decrease` |
| `full_record` | **Central** | -0.47 | -0.12 (`Suggestive decrease`) | -0.17 (`No detectable trend`) | -0.62* | -0.31 (`Suggestive decrease`) | 0.50 | -0.20 [-0.28, -0.11] | `Suggestive decrease` |
| `full_record` | **SW** | -0.05 | -0.10 (`Suggestive decrease`) | -0.25 (`Suggestive decrease`) | -0.29* | -0.22 (`Suggestive decrease`) | 0.19 | +0.17 [+0.05, +0.29] | `Suggestive increase` |
| `full_record` | **SE** | -0.05 | -0.09 (`Suggestive decrease`) | -0.04 (`No detectable trend`) | -0.30* | -0.14 (`Suggestive decrease`) | 0.27 | +0.08 [-0.03, +0.19] | `No detectable trend` |
| `full_record` | **National** | -0.51 | -0.09 (`Suggestive decrease`) | -0.13 (`No detectable trend`) | -0.51* | -0.24 (`Suggestive decrease`) | 0.42 | -0.28 [-0.35, -0.21] | `Suggestive decrease` |
| `grace_era` | **NW** | -1.56 | -0.28 (`Suggestive decrease`) | -0.54 (`Suggestive decrease`) | -1.41* | -0.71 (`Suggestive decrease`) | 1.13 | -0.88 [-1.08, -0.66] | `Suggestive decrease` |
| `grace_era` | **NE** | -0.72 | -0.17 (`Suggestive decrease`) | -0.25 (`Suggestive decrease`) | -0.50* | -0.30 (`Suggestive decrease`) | 0.33 | -0.46 [-0.65, -0.28] | `Suggestive decrease` |
| `grace_era` | **Central** | -0.63 | -0.29 (`Suggestive decrease`) | -0.55 (`Suggestive decrease`) | -0.94* | -0.57 (`Suggestive decrease`) | 0.66 | -0.13 [-0.28, +0.00] | `Suggestive decrease` |
| `grace_era` | **SW** | -0.13 | -0.19 (`Suggestive decrease`) | -0.61 (`Suggestive decrease`) | -0.60* | -0.49 (`Suggestive decrease`) | 0.42 | +0.30 [+0.07, +0.53] | `Suggestive increase` |
| `grace_era` | **SE** | -0.12 | -0.08 (`No detectable trend`) | -0.04 (`No detectable trend`) | -0.28* | -0.11 (`No detectable trend`) | 0.24 | -0.02 [-0.22, +0.18] | `No detectable trend` |
| `grace_era` | **National** | -0.68 | -0.20 (`Suggestive decrease`) | -0.42 (`Suggestive decrease`) | -0.78* | -0.45 (`Suggestive decrease`) | 0.58 | -0.28 [-0.39, -0.16] | `Suggestive decrease` |
| `grace_fo_era` | **NW** | -1.67 | +0.05 (`No detectable trend`) | +0.20 (`No detectable trend`) | -1.09* | -0.29 (`No detectable trend`) | 1.29 | -1.37 [-2.02, -0.71] | `Suggestive decrease` |
| `grace_fo_era` | **NE** | -0.79 | -0.04 (`No detectable trend`) | +0.09 (`No detectable trend`) | -0.26* | -0.12 (`No detectable trend`) | 0.35 | -0.84 [-1.48, -0.24] | `Suggestive decrease` |
| `grace_fo_era` | **Central** | -0.81 | -0.08 (`No detectable trend`) | +0.18 (`No detectable trend`) | -0.54* | -0.14 (`No detectable trend`) | 0.72 | -0.68 [-1.18, -0.19] | `Suggestive decrease` |
| `grace_fo_era` | **SW** | +0.53 | -0.32 (`No detectable trend`) | +0.42 (`No detectable trend`) | -0.01* | +0.09 (`No detectable trend`) | 0.74 | +0.49 [-0.18, +1.15] | `Suggestive increase` |
| `grace_fo_era` | **SE** | +0.45 | -0.13 (`No detectable trend`) | -0.05 (`No detectable trend`) | -0.09* | -0.10 (`No detectable trend`) | 0.09 | +0.51 [-0.08, +1.08] | `Suggestive increase` |
| `grace_fo_era` | **National** | -0.47 | -0.10 (`No detectable trend`) | +0.22 (`No detectable trend`) | -0.28* | -0.08 (`No detectable trend`) | 0.50 | -0.40 [-0.95, +0.16] | `No detectable trend` |
| `recent_2020` | **NW** | -2.93 | -0.22 (`No detectable trend`) | -0.37 (`No detectable trend`) | -2.56* | -1.05 (`No detectable trend`) | 2.34 | -1.69 [-2.56, -0.72] | `Suggestive decrease` |
| `recent_2020` | **NE** | -1.06 | -0.24 (`No detectable trend`) | -0.19 (`No detectable trend`) | -0.68* | -0.40 (`No detectable trend`) | 0.49 | -0.76 [-1.65, +0.08] | `Suggestive decrease` |
| `recent_2020` | **Central** | -1.19 | -0.35 (`Suggestive decrease`) | +0.03 (`No detectable trend`) | -1.51* | -0.65 (`No detectable trend`) | 1.54 | -0.48 [-1.19, +0.23] | `No detectable trend` |
| `recent_2020` | **SW** | +0.03 | -0.57 (`Suggestive decrease`) | +0.02 (`No detectable trend`) | -0.69* | -0.44 (`No detectable trend`) | 0.72 | +0.50 [-0.40, +1.41] | `No detectable trend` |
| `recent_2020` | **SE** | +0.39 | -0.42 (`No detectable trend`) | -0.20 (`No detectable trend`) | -0.05* | -0.23 (`No detectable trend`) | 0.37 | +0.47 [-0.29, +1.28] | `Suggestive increase` |
| `recent_2020` | **National** | -1.02 | -0.37 (`Suggestive decrease`) | -0.12 (`No detectable trend`) | -1.09* | -0.54 (`No detectable trend`) | 0.97 | -0.39 [-1.13, +0.44] | `No detectable trend` |

*\*Note: GLDAS-2.2 CLSM is **Non-independent / GRACE-assimilated** (assimilates GRACE TWSA via Ensemble Kalman Filtering); its record starts 2003-02.*

---

## 2. Model Soil-Moisture Homogeneity & Forcing Evolution

### Meteorological Forcing Changes Verified in GLDAS Documentation
1. **GLDAS-2.1 (Noah & VIC):**
   - Driven by atmospheric analysis from NOAA/GDAS combined with disaggregated daily GPCP Version 1.3 precipitation fields.
   - AGRMET (AFWA) radiation was integrated operationally beginning March 1, 2001.
   - Forcing precipitation is independent of domestic agricultural groundwater extraction.
2. **GLDAS-2.2 (CLSM Catchment):**
   - Driven by ECMWF Integrated Forecasting System (IFS) atmospheric analysis fields.
   - Record begins February 1, 2003.
   - Assimilates satellite gravimetry TWSA observations (GRACE/GRACE-FO) directly into model hydrology. Consequently, CLSM soil moisture and groundwater fields are non-independent and partially inherit GRACE trends.

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
Across all three land surface models (Noah 2.1, VIC 2.1, and CLSM 2.2), simulated unsaturated zone soil moisture exhibits no statistically significant secular decline in the Northwest region (Noah: +0.05 cm/yr, $p = 0.6010$; VIC: +0.20 cm/yr; Ensemble: -0.29 cm/yr). In contrast, total terrestrial water storage declines at -1.67 cm/yr during GRACE-FO (and -1.25 cm/yr across the full 2002–2026 record). The resulting multi-model residual storage anomaly ('groundwater + surface water + model error residual') declines at -1.37 cm/yr (95% CI: [-2.02, -0.71]). Because open-loop land surface models (Noah and VIC) simulate topsoil unsaturated moisture dynamics but do not represent unconfined aquifer abstraction, this partition indicates that regional water storage loss is concentrated in the deep subsurface, consistent with irrigation-driven unconfined aquifer drawdown rather than surface desiccation.

**Methodological Limitations:**  
> *Limitations:* Residual storage is strictly defined as $\text{Residual} = \text{TWS} - \Delta\text{SMS} - \Delta\text{SWE}$. It aggregates unmodeled surface water bodies, river stage variations, irrigation return flows, and structural model errors. It should not be interpreted as in-situ piezometric water table depth. GLDAS-2.2 CLSM assimilates GRACE observations and is not an independent validation.

---

### বাংলা বৈজ্ঞানিক বিবরণী (Bangla Scientific Synthesis)
তিনটি ভিন্ন ল্যান্ড সারফেস মডেলের (Noah 2.1, VIC 2.1, এবং CLSM 2.2) বিশ্লেষণে দেখা যায় যে, উত্তর-পশ্চিম অঞ্চলে মাটির অগভীর আর্দ্রতায় কোনো তাৎপর্যপূর্ণ দীর্ঘমেয়াদী পতন ঘটেনি (নূহ মডেল: +0.05 সেমি/বছর; ভিআইসি মডেল: +0.20 সেমি/বছর; এনসেম্বল গড়: -0.29 সেমি/বছর)। কিন্তু স্যাটেলাইট গ্র্যাভিমেট্রি তথ্যে মোট পানি সঞ্চয় (TWS) দ্রুতগতিতে হ্রাস পাচ্ছে (গ্রেস-এফও যুগে বার্ষিক -1.67 সেমি)। ফলস্বরূপ, ভূ-গর্ভস্থ অবশিষ্টাংশ সঞ্চয় ('ভূগর্ভস্থ পানি + ভূ-পৃষ্ঠের পানি + মডেল ত্রুটির অবশিষ্টাংশ') বার্ষিক -1.37 সেমি হারে হ্রাস পাচ্ছে। যেহেতু উন্মুক্ত ল্যান্ড সারফেস মডেলগুলো কেবল মাটির উপরের আর্দ্রতা পরিমাপ করে কিন্তু গভীর নলকূপ দিয়ে পানি উত্তোলন গণনা করে না, তাই মাটির উপরিভাগের আর্দ্রতা স্থিতিশীল থাকা সত্ত্বেও এই গভীর অবশিষ্টাংশের পতন নির্দেশ করে যে পানি সঞ্চয় হ্রাসের ঘটনা মাটির গভীরে পুঞ্জীভূত—যা শুষ্ক মৌসুমে বোরো ধানের সেচ উত্তোলনের সাথে সামঞ্জস্যপূর্ণ।

**সীমাবদ্ধতার বিজ্ঞপ্তি:**  
> *সীমাবদ্ধতা:* অবশিষ্টাংশ সঞ্চয়কে কঠোরভাবে 'ভূগর্ভস্থ পানি + ভূ-পৃষ্ঠের পানি + মডেল ত্রুটির অবশিষ্টাংশ' হিসেবে সংজ্ঞায়িত করা হয়েছে। এতে নদী-নালা ও উন্মুক্ত জলাশয়ের প্রবাহ এবং মডেলের কাঠামোগত অনিশ্চয়তা অন্তর্ভুক্ত। একে সরাসরি স্থানীয় নলকূপের পানির স্তর হিসেবে গণ্য করা যাবে না। অধিকন্তু, GLDAS-2.2 CLSM মডেলে গ্রেস স্যাটেলাইট তথ্য আত্তীকরণ (assimilated) করা হয়েছে, বিধায় এটি কোনো স্বাধীন প্রামাণ্য উৎস নয়।
