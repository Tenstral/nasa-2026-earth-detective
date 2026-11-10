# Exploratory Trend of Seasonal Storage Response Ratio (2002–2025)

**Status:** PRELIMINARY & EXPLORATORY ONLY
**Generated:** 2026-11-10 07:40:08
**Methodology:** Theil-Sen robust slope estimator with Calibrated Effective Sample Size Mann-Kendall (ESS-MK) test and duality-aligned 95% rank confidence intervals.

---

## 1. Metric Definition & Data Protocol
- **Seasonal Storage Response Ratio:** Defined as the ratio of seasonal storage rebound alone ($\Delta	ext{TWS}$, cm) to seasonal monsoon rainfall ($0.1 	imes P_{	ext{monsoon}}$, cm liquid water):
  $$\text{Seasonal Storage Response Ratio} = \frac{\Delta\text{TWS}\text{ (cm)}}{0.1 \times P_{\text{monsoon}}\text{ (mm)}} \times 100\%$$
- **Numerator:** $\Delta	ext{TWS}$ is the post-monsoon storage peak (maximum of August–November) minus the pre-monsoon dry season low (minimum of March–May) from CSR GRACE/GRACE-FO RL06.3.
- **Denominator:** $P_{	ext{monsoon}}$ is the decoupled June–September 4-month total rainfall from NASA GPM IMERG V07B Final Run.
- **Missing Observation Protocol:** Seasons with incomplete satellite observation windows are excluded directly rather than interpolated.
  - In 2017: GRACE was decommissioned in June 2017, so no post-monsoon peak was observed.
  - In 2018: GRACE-FO was launched in May 2018 (first operational data in June 2018), so no pre-monsoon low was observed.
  - Consequently, 2 seasons (2017, 2018) are dropped per region, leaving **22 complete seasons** (2002–2016 [15] and 2019–2025 [7]) in the main run.
- **Sensitivity Run:** Drops seasons within $\pm 6$ months of the GRACE/GRACE-FO transition (2016, 2017, 2018, 2019), leaving **20 complete seasons**.
- **Exploratory FDR Control:** Benjamini-Hochberg FDR control is calculated strictly across these 6 exploratory regional tests and is quarantined from headline 36-test FDR families.

---

## 2. Main Analysis Results (22 Complete Seasons, 2002–2025)

| Region | N | Mean Ratio | Theil-Sen Slope (%/yr) | 95% Confidence Interval | p-value (ESS-MK) | Exploratory FDR q | MDS (80% Power) | Verdict |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **NW** (Northwest (Rajshahi + Rangpur)) | 22 | 39.6% | +0.266%/yr | [-0.295, +0.836] | 0.3784 | 0.5158 | 0.700%/yr | No detectable trend |
| **NE** (Northeast (Sylhet + Mymensingh)) | 22 | 30.1% | +0.203%/yr | [-0.079, +0.500] | 0.2147 | 0.4294 | 0.400%/yr | No detectable trend |
| **Central** (Central (Dhaka)) | 22 | 42.2% | +0.387%/yr | [+0.046, +0.712] | 0.0369 | 0.1105 | 0.500%/yr | No detectable trend |
| **SW** (Southwest (Khulna + Barishal)) | 22 | 33.0% | +0.138%/yr | [-0.164, +0.481] | 0.4298 | 0.5158 | 0.500%/yr | No detectable trend |
| **SE** (Southeast (Chattogram)) | 22 | 26.0% | +0.063%/yr | [-0.147, +0.228] | 0.6118 | 0.6118 | 0.350%/yr | No detectable trend |
| **National** (National Composite (All 8 Divisions)) | 22 | 32.5% | +0.136%/yr | [+0.028, +0.355] | 0.0208 | 0.1105 | 0.300%/yr | No detectable trend |

---

## 3. Sensitivity Analysis (Transition-Buffer Excluded, N = 20 Seasons)

| Region | N | Mean Ratio | Theil-Sen Slope (%/yr) | 95% Confidence Interval | p-value (ESS-MK) | Exploratory FDR q | MDS (80% Power) | Verdict |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **NW** (Northwest (Rajshahi + Rangpur)) | 20 | 40.0% | +0.362%/yr | [-0.131, +0.932] | 0.1759 | 0.2638 | 0.650%/yr | No detectable trend |
| **NE** (Northeast (Sylhet + Mymensingh)) | 20 | 30.4% | +0.263%/yr | [-0.018, +0.548] | 0.0855 | 0.1710 | 0.400%/yr | No detectable trend |
| **Central** (Central (Dhaka)) | 20 | 42.6% | +0.476%/yr | [+0.151, +0.698] | 0.0048 | 0.0212 | 0.450%/yr | Exploratory: trend detected |
| **SW** (Southwest (Khulna + Barishal)) | 20 | 33.0% | +0.093%/yr | [-0.183, +0.528] | 0.6265 | 0.6732 | 0.550%/yr | No detectable trend |
| **SE** (Southeast (Chattogram)) | 20 | 26.1% | +0.052%/yr | [-0.175, +0.238] | 0.6732 | 0.6732 | 0.400%/yr | No detectable trend |
| **National** (National Composite (All 8 Divisions)) | 20 | 32.8% | +0.151%/yr | [+0.059, +0.367] | 0.0071 | 0.0212 | 0.300%/yr | Exploratory: trend detected |

---

## 4. Methodological Limits & Scientific Context
- **Bulk Storage Mass Limitation:** The seasonal storage response ratio reflects bulk total water storage change, integrating unsaturated soil moisture and surface water bodies alongside groundwater, and does not represent an isolated groundwater recharge coefficient.
- **Confidence Interval Breadth:** In regions such as the Northwest, the 95% confidence interval ([-0.295, +0.836] %/yr) is wide relative to the point slope (+0.266 %/yr) and spans zero, reflecting substantial interannual variability and confirming that the slope cannot be distinguished from multi-year climate variability.
- **Exploratory Framing:** Neither Central nor National slopes survive within-family Benjamini-Hochberg FDR control ($q \ge 0.05$); therefore, all regions are formally classified as `No detectable trend` under multiple-testing standards.
