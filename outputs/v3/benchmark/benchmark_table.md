# Audit-Grade Literature Benchmark: Bangladesh Water Storage Trends

> **PRELIMINARY — NASA Space Apps Challenge 2026**
> **Team Tenstral | Project: Bengal Hydro Detective**
> Generated programmatically from verified peer-reviewed publications and `outputs/v3/full_record/results_all_windows.csv`.

---

## 1. Synthesis Table of Published Studies vs. Bengal Hydro Detective v3 Rates

| ID | Author & Year | Study Period | Spatial Scope | Variable | Published Rate (Original) | Converted Rate (cm/yr) | Comparable? | Our v3 Rate (cm/yr) [95% CI] | Trajectory Assessment |
|---|---|---|---|---|---|---|---|---|---|
| **PUB-01** | Shamsudduha, M., Taylor, R. G., & Longuevergne, L. (2012) | 2003–2007 (satellite) / 1985–2007 (in situ) | Bengal Basin (Bangladesh territory, ~144,000 km2) | Groundwater storage (GWS) | `-0.44 to -2.04 km3/yr (GRACE ΔGWS); -0.52 ± 0.30 km3/yr (in situ)` | -0.31 to -1.42 cm/yr (using 144,000 km2) | **Yes** | `-0.68 [-0.91, -0.45]` | Similar: our grace_era national TWS rate (-0.83 km3/yr; -0.68 cm/yr) falls directly within their multi-model GRACE ΔGWS range (-0.44 to -2.04 km3/yr). |
| **PUB-02** | Purdy, A. J., David, C. H., Sikder, M. S., Reager, J. T., Chandanpurkar, H. A., Jones, N. L., & Matin, M. A. (2019) | 2002–2016 | Bangladesh National & Northwest region | Total Water Storage (TWS) and Groundwater Storage (GWS) | `-0.85 cm/yr (-1.16 km3/yr) National TWS; -1.99 cm/yr (-0.60 km3/yr) NW TWS; -0.88 cm/yr NW GWS` | -0.85 cm/yr (National), -1.99 cm/yr (NW) | **Yes** | `Nat: -0.68 [-0.91, -0.45]; NW: -1.56 [-1.96, -1.17]` | Similar: our grace_era rates (-0.68 cm/yr Nat, -1.56 cm/yr NW) closely corroborate Purdy et al.'s findings (-0.85 cm/yr Nat, -1.99 cm/yr NW), confirming the NW as the primary depletion hotspot. |
| **PUB-03** | Ouyang, L., Zhao, Z., Zhou, D., Cao, J., Qin, J., Cao, Y., & He, Y. (2024) | 2015–2022 | Bangladesh territory (national & divisions: Rangpur, Rajshahi, Mymensingh) | Groundwater storage (GWS) and InSAR Land Subsidence | `-5.55 mm/yr (-0.555 cm/yr) National GWS` | -0.56 cm/yr | **Yes** | `Full: -0.51 [-0.65, -0.38]; GFO: -0.47 [-1.37, 0.43]` | Remarkably consistent: Ouyang et al.'s -0.555 cm/yr GWS depletion falls squarely inside our full_record 95% CI (-0.65 to -0.38 cm/yr) and matches our point estimate of -0.51 cm/yr. |
| **PUB-04** | Shamsudduha, M., & Taylor, R. G. (2020) | 2002–2016 | Aquifer No. 24: Ganges–Brahmaputra Basin (~1.2 million km2) | Groundwater storage (GWS) | `Non-linear; linear trends unrepresentative due to episodic monsoonal recharge pulses` | N/A (Non-linear episodic) | **Partly** | `-0.51 [-0.65, -0.38]` | Physically corroborating: explains our finding of declining recharge efficiency (-1.05%/yr, p=0.0007); secular linear decline is punctuated by episodic extreme monsoonal flood years. |
| **PUB-05** | Ahmed, S. S., Zzaman, R. U., Jony, S. R., Himel, F. R., Sharmin, A., Rahman, A. H. M. K., Rahman, M. S., & Nowreen, S. (2025) | 2003–2024 | Bangladesh (focus on Barind Tract, NW) | GLDAS GWS Downscaled Storage & Recharge | `Localized discharge rates up to 25 cm/yr in intensive Boro irrigation zones` | Up to -25 cm/yr (localized Barind hotspots) | **Partly** | `NW: -1.25 [-1.49, -1.01]` | Physically consistent: provides the localized mechanism (intense Boro rice abstraction in the Barind tract) explaining why our regional NW trend (-1.25 cm/yr; -0.39 km3/yr) is the steepest in Bangladesh. |
| **PUB-06** | Rodell, M., Famiglietti, J. S., Wiese, D. N., Reager, J. T., Beaudoing, H. K., Landerer, F. W., & Lo, M. H. (2018) | 2002–2016 | Region 13: Eastern India, Bangladesh, and Myanmar (>1,000,000 km2) | Terrestrial Water Storage (TWS) | `-23.3 ± 1.9 Gt/yr (-23.3 ± 1.9 km3/yr) across Region 13` | N/A (Transboundary mega-region; area not delineated specifically for Bangladesh) | **Partly (Global Context)** | `-0.68 [-0.91, -0.45]` | Contextually corroborating: confirms regional freshwater deficit in the 2002–2016 era; our national Bangladesh slope (-0.83 km3/yr) represents ~3.6% of this transboundary depletion. |

---

## 2. Granular Extraction and Verification Audit

### [PUB-01] Shamsudduha, M., Taylor, R. G., & Longuevergne, L. (2012). Monitoring groundwater storage changes in the highly seasonal humid tropics: Validation of GRACE measurements in the Bengal Basin. Water Resources Research, 48(2), W02508.
- **DOI / Link:** [`10.1029/2011WR010993`](https://doi.org/10.1029/2011WR010993)
- **Product & Processing:** GRACE RL04 Spherical Harmonics (CSR, GFZ, JPL) + GLDAS (CLM, Noah, VIC) & in situ 236 boreholes
- **Methodology:** Residual water budget (ΔGWS = ΔTWS - ΔSMS) & in situ kriging
- **Reported Metric & Uncertainty:** `-0.44 to -2.04 km3/yr (GRACE ΔGWS); -0.52 ± 0.30 km3/yr (in situ)` (Uncertainty: ±0.30 km3/yr (in situ))
- **Location in Text:** Abstract, p. 1-2, Table 3
- **Direct Verified Excerpt (<=25 words):**
  > *"Recent groundwater depletion estimated from borehole hydrographs (2003–2007) averaged -0.52 ± 0.30 km3/yr... satellite-derived ΔGWS ranged between -0.44 to -2.04 km3/yr."*
- **Comparability Note:** Direct overlap with early GRACE era across Bangladesh Bengal Basin.
- **Trajectory Comparison:** Similar: our grace_era national TWS rate (-0.83 km3/yr; -0.68 cm/yr) falls directly within their multi-model GRACE ΔGWS range (-0.44 to -2.04 km3/yr).

### [PUB-02] Purdy, A. J., David, C. H., Sikder, M. S., Reager, J. T., Chandanpurkar, H. A., Jones, N. L., & Matin, M. A. (2019). An Open-Source Tool to Facilitate the Processing of GRACE Observations and GLDAS Outputs: An Evaluation in Bangladesh. Frontiers in Environmental Science, 7, 155.
- **DOI / Link:** [`10.3389/fenvs.2019.00155`](https://doi.org/10.3389/fenvs.2019.00155)
- **Product & Processing:** GRACE JPL/CSR Mascons (RL05/RL06) + GLDAS Noah/VIC/CLM
- **Methodology:** Linear Theil-Sen trend on monthly mascon solutions and GLDAS soil moisture residual
- **Reported Metric & Uncertainty:** `-0.85 cm/yr (-1.16 km3/yr) National TWS; -1.99 cm/yr (-0.60 km3/yr) NW TWS; -0.88 cm/yr NW GWS` (Uncertainty: Standard error reported in text)
- **Location in Text:** Section 3.2, Figures 4 & 5
- **Direct Verified Excerpt (<=25 words):**
  > *"Groundwater storage in the study region decreased at a rate of 0.88 cm yr-1... TWSa revealed rates of -0.85 cm yr-1."*
- **Comparability Note:** Directly comparable spatial units and identical GRACE-1 satellite mission window.
- **Trajectory Comparison:** Similar: our grace_era rates (-0.68 cm/yr Nat, -1.56 cm/yr NW) closely corroborate Purdy et al.'s findings (-0.85 cm/yr Nat, -1.99 cm/yr NW), confirming the NW as the primary depletion hotspot.

### [PUB-03] Ouyang, L., Zhao, Z., Zhou, D., Cao, J., Qin, J., Cao, Y., & He, Y. (2024). Study on the Relationship between Groundwater and Land Subsidence in Bangladesh Combining GRACE and InSAR. Remote Sensing, 16(19), 3715.
- **DOI / Link:** [`10.3390/rs16193715`](https://doi.org/10.3390/rs16193715)
- **Product & Processing:** GRACE/GRACE-FO CSR Mascons + GLDAS NOAH025_M + Sentinel-1 SBAS-InSAR
- **Methodology:** GRACE mascon decomposition (ΔGWS = ΔTWS - ΔSMS) & SBAS-InSAR deformation rate
- **Reported Metric & Uncertainty:** `-5.55 mm/yr (-0.555 cm/yr) National GWS` (Uncertainty: Not explicitly stated for linear slope)
- **Location in Text:** Abstract, Section 3.3, p. 8-10
- **Direct Verified Excerpt (<=25 words):**
  > *"Groundwater storage (GWS) in Bangladesh experienced a declining trend at an average rate of −5.55 mm/year, with the most prominent drops occurring in Rangpur, Mymensingh, and Rajshahi."*
- **Comparability Note:** Covers recent operational period bridging GRACE and GRACE-FO with independent InSAR cross-validation.
- **Trajectory Comparison:** Remarkably consistent: Ouyang et al.'s -0.555 cm/yr GWS depletion falls squarely inside our full_record 95% CI (-0.65 to -0.38 cm/yr) and matches our point estimate of -0.51 cm/yr.

### [PUB-04] Shamsudduha, M., & Taylor, R. G. (2020). Groundwater storage dynamics in the world's large aquifer systems from GRACE: uncertainty and role of extreme precipitation. Earth System Dynamics, 11(3), 755–774.
- **DOI / Link:** [`10.5194/esd-11-755-2020`](https://doi.org/10.5194/esd-11-755-2020)
- **Product & Processing:** Ensemble of 3 GRACE processing centres (CSR, GFZ, JPL) + 4 LSMs (CLM, Mosaic, Noah, VIC)
- **Methodology:** Multi-model ensemble anomaly decomposition, non-linear trend characterization
- **Reported Metric & Uncertainty:** `Non-linear; linear trends unrepresentative due to episodic monsoonal recharge pulses` (Uncertainty: Inter-model ensemble standard deviation)
- **Location in Text:** Table 1, Section 3.2, p. 760-764
- **Direct Verified Excerpt (<=25 words):**
  > *"Trends in GRACE-derived ΔGWS are overwhelmingly non-linear... simple linear declining trends adequately explaining variability in only two of the large aquifer systems."*
- **Comparability Note:** Evaluates full transboundary basin rather than Bangladesh boundaries, highlighting non-linear precipitation buffering.
- **Trajectory Comparison:** Physically corroborating: explains our finding of declining recharge efficiency (-1.05%/yr, p=0.0007); secular linear decline is punctuated by episodic extreme monsoonal flood years.

### [PUB-05] Ahmed, S. S., Zzaman, R. U., Jony, S. R., Himel, F. R., Sharmin, A., Rahman, A. H. M. K., Rahman, M. S., & Nowreen, S. (2025). GroundHog: Revolutionizing GLDAS Groundwater Storage Downscaling for Enhanced Recharge Estimation in Bangladesh. arXiv preprint arXiv:2503.22771.
- **DOI / Link:** [`arXiv:2503.22771`](https://doi.org/https://arxiv.org/abs/2503.22771)
- **Product & Processing:** GLDAS Noah 25 km downscaled to 2 km via ML (Random Forest/XGBoost) trained on BWDB piezometers
- **Methodology:** Machine learning downscaling framework and spatial water budget
- **Reported Metric & Uncertainty:** `Localized discharge rates up to 25 cm/yr in intensive Boro irrigation zones` (Uncertainty: Validation R2 = 0.96 against in situ monitoring)
- **Location in Text:** Abstract, Section 4.2
- **Direct Verified Excerpt (<=25 words):**
  > *"downscaling GLDAS groundwater storage (GWS) data to high-resolution 2 km grids across the 2003–2024 timeline... localized discharge rates reach up to 25 cm/year."*
- **Comparability Note:** Preprint presenting machine learning downscaling; reports localized aquifer discharge rates rather than regional basin-averaged secular trends.
- **Trajectory Comparison:** Physically consistent: provides the localized mechanism (intense Boro rice abstraction in the Barind tract) explaining why our regional NW trend (-1.25 cm/yr; -0.39 km3/yr) is the steepest in Bangladesh.

### [PUB-06] Rodell, M., Famiglietti, J. S., Wiese, D. N., Reager, J. T., Beaudoing, H. K., Landerer, F. W., & Lo, M. H. (2018). Emerging trends in global freshwater availability. Nature, 557(7707), 651–659.
- **DOI / Link:** [`10.1038/s41586-018-0123-1`](https://doi.org/10.1038/s41586-018-0123-1)
- **Product & Processing:** GRACE RL05 Spherical Harmonics ensemble
- **Methodology:** Harmonic trend decomposition and water budget attribution
- **Reported Metric & Uncertainty:** `-23.3 ± 1.9 Gt/yr (-23.3 ± 1.9 km3/yr) across Region 13` (Uncertainty: ±1.9 Gt/yr)
- **Location in Text:** Figure 1, Table 1, Region 13 entry
- **Direct Verified Excerpt (<=25 words):**
  > *"Region 13 (Eastern India, Bangladesh, Myanmar)... notable negative TWS trend of -23.3 ± 1.9 Gt/yr... attributed to groundwater abstraction and precipitation decrease."*
- **Comparability Note:** Broad regional footprint encompassing eastern India, Bangladesh, and Myanmar; provides macro-continental context.
- **Trajectory Comparison:** Contextually corroborating: confirms regional freshwater deficit in the 2002–2016 era; our national Bangladesh slope (-0.83 km3/yr) represents ~3.6% of this transboundary depletion.

