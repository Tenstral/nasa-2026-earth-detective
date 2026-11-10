# Evaluation Report: Literature Alignment and Empirical Findings

> **PRELIMINARY — NASA Space Apps Challenge 2026**  
> **Team Tenstral | Project: Bengal Hydro Detective**  
> **Scope:** Multi-decadal satellite gravimetry observations (2002–2026) vs. peer-reviewed hydrological literature on Bangladesh.

---

## Executive Summary

This evaluation report systematically assesses how the empirical findings of the **Bengal Hydro Detective** project align with published peer-reviewed hydrogeological literature. Using a 24-year satellite observational record (CSR GRACE/GRACE-FO RL0603 mascons, GPM IMERG V07B precipitation, and GLDAS v2.1 land surface models), we examine:
1. The extent to which satellite-derived total water storage trajectories agree with published benchmarks;
2. What that alignment signifies for scientific understanding and regional water resources;
3. Where and why divergences emerge between satellite observations and specific literature claims; and
4. The physical, spatial, and methodological limitations that account for those discrepancies.

---

## 1. Summary of Alignment Across Key Hydrogeological Findings

| Scientific Domain | Our Empirical Finding (2002–2026 / Eras) | Peer-Reviewed Literature Benchmark | Extent of Alignment | Scientific Meaning |
|---|---|---|---|---|
| **Northwest Depletion Hotspot** | NW total water storage declines at **-1.25 cm/yr** (95% CI: [-1.50, -1.02]; full record) and **-1.56 cm/yr** ([-1.96, -1.17]; GRACE era). Three-way step-adjusted range spans **-1.81 to -1.25 cm/yr**. | **Purdy et al. (2019):** -1.99 cm/yr NW TWS (2002–2016).<br>**Ouyang et al. (2024):** Depletion centered across Rangpur and Rajshahi divisions.<br>**Ahmed et al. (2025):** Deep winter drawdown documented across the Barind Tract (preprint, not peer reviewed). | **High Qualitative / Strong Order-of-Magnitude Alignment**<br>(Purdy point estimate is slightly steeper; falls within 0.03 cm/yr of our GRACE-era upper CI bound [-1.96 cm/yr]). | The Northwest depletion signal is consistent across satellite sensors, independent processing centers (CSR vs. JPL), and observational decades. It represents an enduring multi-decadal pattern. |
| **National Total Water Storage Trend** | National total water storage declines at **-0.68 cm/yr** (95% CI: [-0.92, -0.45]; -0.83 km³/yr) during the GRACE era (2002–2017) and **-0.51 cm/yr** ([-0.66, -0.38]; -0.63 km³/yr) across the full record. | **Purdy et al. (2019):** -0.85 cm/yr (-1.16 km³/yr) national TWS.<br>**Shamsudduha et al. (2012):** -0.44 to -2.04 km³/yr GRACE GWS; -0.52 ± 0.30 km³/yr in situ borehole GWS.<br>**Rodell et al. (2018):** Macro-regional freshwater deficit across Region 13 (-23.3 ± 1.9 km³/yr; transboundary macro-region). | **High Quantitative Alignment**<br>(Purdy’s -0.85 cm/yr falls directly within our GRACE-era 95% CI [-0.92, -0.45]; Shamsudduha’s in situ borehole rate matches our volumetric magnitude). | Multi-mission analysis indicates that storage loss continued across the inter-mission gap without significant secular acceleration or deceleration (+0.21 cm/yr epoch delta; CI spans zero). |
| **Unsaturated Soil Moisture Share** | Northwest GLDAS Noah and VIC 0–2 m soil moisture trend is **-0.12 to -0.10 cm/yr** (~8% to 10% of total storage decline), leaving the unpartitioned residual (groundwater + surface water + biomass + model error) at **-1.12 to -1.11 cm/yr**. | **Shamsudduha et al. (2012) & Purdy et al. (2019):** Simulated unsaturated soil moisture storage exhibits negligible multi-year secular trends compared to subsurface storage depletion. | **High Direct Alignment** across independent open-loop land surface models. | Total water storage depletion is overwhelmingly situated in the unpartitioned residual (groundwater + surface water + biomass + model error), rather than near-surface root-zone soil moisture desiccation. |
| **Precipitation Homogeneity** | GPM IMERG V07B shows **no detectable trend** nationally (+2.04 mm/yr; CI: [-7.70, +12.45]) and in the Northwest (-1.9 mm/yr; CI: [-11.0, +4.5]; FDR q = 0.8968). | **Shamsudduha et al. (2012, 2020):** Monsoon rainfall exhibits high interannual variability but no long-term secular decline accounting for multi-decadal storage reduction. | **High Direct Alignment.** | Total water storage reduction occurs alongside absence of a secular monsoon precipitation decline. Water departs or is abstracted faster than natural seasonal replenishment over multi-year cycles. |
| **Coastal Delta Balance** | Southwest and Southeast show **no detectable trend** (-0.05 cm/yr; 95% CIs span zero). Paired test shows no detectable difference between SW and SE. | Literature on coastal Bangladesh documents seasonal estuarine salinity intrusion and tidal waterlogging, rather than regional bulk terrestrial mass deficits. | **Context only (not a like-for-like comparison)** | Satellite gravimetry measures total mass anomalies. The literature topic (salinity and waterlogging) is a water-quality and surface-water issue that GRACE total water storage cannot measure; the absence of a detectable storage trend in SW and SE says nothing about salinity. |

---

## 2. To What Extent Do Findings Align and What Does It Mean?

### A. Spatial Pattern Alignment
Across the literature, every study examining spatial variations within Bangladesh identifies the Northwest (Rajshahi and Rangpur divisions) as experiencing the most pronounced storage reduction. Our calibrated paired regional tests indicate that the Northwest declines approximately 1.2 cm/year faster than the Southwest and Southeast, while the Northeast and Central regions decline approximately 0.5 cm/year faster than the southern regions. This aligns with the spatial distribution observed in borehole piezometer networks (Shamsudduha et al., 2012) and downscaled models (Ahmed et al., 2025; Ouyang et al., 2024).

### B. Magnitude and Temporal Alignment
During the historical GRACE mission (2002–2017), our estimated national total water storage depletion rate of **-0.68 cm/yr** [95% CI: -0.92, -0.45] (-0.83 km³/yr) directly encompasses the **-0.85 cm/yr** (-1.16 km³/yr) estimate reported by Purdy et al. (2019) using independent mascon processing. Furthermore, our volumetric rate falls within the multi-model satellite range (-0.44 to -2.04 km³/yr) and closely aligns with the in situ borehole estimate of -0.52 ± 0.30 km³/yr published by Shamsudduha et al. (2012).

### C. What This Alignment Means Scientifically
1. **Measurement Robustness:** Agreement across independent processing choices and published estimates is consistent with the Northwest decline being a real signal rather than a processing artifact. It does not by itself validate the magnitude, which has not been checked against in-situ wells.
2. **Persistence Beyond Early Observations:** The 24-year record is consistent with a continuing decline, but the GRACE-FO era alone is not independently detectable (NW slope -1.67 cm/yr, 95% CI [-3.32, +0.06], below the detection limit).
3. **Decoupling from Near-Surface Desiccation:** Soil moisture accounts for a minor part of the Northwest decline in the GLDAS comparison. The remainder is an unpartitioned residual (groundwater + surface water + biomass + model error); the analysis cannot say which component dominates.

---

## 3. Where Literature and Findings Do Not Align (and Why)

While qualitative patterns agree, four key divergences appear when comparing our satellite results with specific literature claims:

### Divergence 1: Northwest Depletion Magnitude (Purdy -1.99 cm/yr vs. Our -1.56 cm/yr / -1.25 cm/yr)
- **The Contrast:** Purdy et al. (2019) reported a Northwest TWS slope of **-1.99 cm/yr** (2002–2016). Our transition-free GRACE-era slope is **-1.56 cm/yr** [95% CI: -1.96, -1.17] and our full-record slope is **-1.25 cm/yr** [95% CI: -1.50, -1.02]. Our GRACE-era interval ends 0.03 cm/yr from Purdy's value, so the two are close but not overlapping.
- **Possible reasons (to be verified in the source paper):**
  1. *Spatial Delineation:* Purdy et al. may have used a different Northwest delineation, possibly including areas outside Bangladesh; their exact boundary and mascon solution (JPL versus CSR) need to be checked in the paper.
  2. *Evaluation Window:* Purdy evaluated 2002–2016 (14 years). Adding the remaining GRACE data (through 2017) and the extended GRACE-FO era moderates the long-term Theil-Sen slope.
  3. *Mascon Solution:* Differences between mascon implementations (JPL versus CSR) and their respective coastline and smoothing parameterizations.

### Divergence 2: Localized Pumping Hotspots vs. Regional Footprints (Ahmed et al. 2025 up to -25 cm/yr vs. Our -1.25 cm/yr)
- **The Contrast:** Local well hydrographs and downscaled studies report much larger local rates than a 300 km regional average can show; the exact figures in the Ahmed et al. preprint (arXiv 2503.22771) are to be verified.
- **Why It Diverged:**
  1. *Spatial Dilution:* Satellite gravimetry resolves mass anomalies over footprints of approximately 300 km (~100,000 km²). Individual intensive tubewell clusters operate at scales of 100 meters to 10 kilometers. Regional spatial integration intrinsically averages intense cone-of-depression cones with adjacent non-irrigated floodplains and river recharge corridors.
  2. *Metric Discrepancy (Hydraulic Head vs. Equivalent Water Thickness):* Local well hydrographs measure water table depth (hydraulic head in meters below ground). To convert head changes to equivalent water thickness (EWT), head must be multiplied by an assumed specific yield ($S_y$). In fine sand and silt formations characteristic of the Bengal Basin, $S_y$ ranges between 0.05 and 0.12. A 15–20 cm/year water table drop multiplied by an assumed specific yield of $S_y = 0.08$ corresponds to **1.2 to 1.6 cm/year** of equivalent water thickness—bringing local hydrographs into plausible consistency with our satellite EWT measurements. This is an order-of-magnitude consistency check resting on an assumed specific yield, not a direct validation.

### Divergence 3: Linear Trends vs. Episodic Recharge Pulses (Shamsudduha & Taylor 2020)
- **The Contrast:** Shamsudduha & Taylor (2020) argued that linear trends in large Asian "aquifer" systems (including the Ganges-Brahmaputra Basin) are unrepresentative because dynamics are dominated by non-linear episodic monsoonal recharge pulses.
- **Why It Diverged and How It Is Reconciled:**
  - Over short observation windows (<10 years), extreme flood years (such as 2004, 2007, or 2017) cause substantial positive storage jumps (+50 to +60 cm seasonal rebound) that distort standard linear regression.
  - Across a 24-year baseline, non-parametric Theil-Sen regression paired with Hurwicz-corrected Effective Sample Size Mann-Kendall testing indicates a statistically significant multi-decadal downward drift in the Northwest ($p < 0.0001$).
  - Our seasonal analysis reconciles this: seasonal drawdown (mean 55.2 cm) and response ratios (mean 39.6%) show no secular trend. Episodic recharge pulses continue seasonally, but they operate upon a multi-decadal baseline that shifts systematically downward.

### Divergence 4: Short-window estimates vs detection limits
- **The Contrast:** Our own earlier 2020-onward window estimate for the Northwest (-2.93 cm/yr, 95% CI [-4.97, -0.78]) is method-dependent (raw p = 0.0107 but FDR q = 0.077) and falls below the detection limit for that window (minimum detectable slope 2.34 cm/yr). Short windows of this kind should not be read as evidence of acceleration.
- **Why It Diverged:**
  - *Statistical Power:* In short windows (e.g., recent 2020–2026, $n = 79$ months, compared to $n = 257$ months for the full record), strong serial autocorrelation reduces the effective sample size well below n. Calibrated testing yields an FDR $q$-value of 0.0772 (> 0.05), placing short-term acceleration below the rigorous detection limit.
  - *Inter-Satellite Calibration Step:* The transition between GRACE and GRACE-FO introduces a +9.15 cm step offset. Depending on step adjustment, full-record slopes range between -1.81 and -1.25 cm/year, showing that short-term segmentations are sensitive to edge effects and instrument transitions.

---

## 4. Methodological and Epistemic Limitations

The discrepancies identified above stem from five fundamental observational and methodological constraints:

1. **Spatial Footprint and Resolution Limits:**  
   GRACE/GRACE-FO gravimetry has an effective spatial resolution of roughly 300 km. It captures aggregate regional mass changes but cannot resolve localized tubewell drawdowns, village-level cone of depression formations, or pumping lift variations.

2. **Equivalence of Physical Metrics:**  
   Point borehole observations report water table levels (hydraulic head in meters), whereas satellite gravimetry measures vertically integrated mass anomalies (equivalent water thickness in centimeters). Direct comparison requires spatial kriging and specific yield ($S_y$) assumptions that introduce substantial spatial uncertainty.

3. **Storage Partitioning Constraints:**  
   Open-loop land surface models (GLDAS Noah and VIC) estimate unsaturated zone soil moisture (0–2 m). The remaining unpartitioned residual (groundwater + surface water + biomass + model error) combines unconfined groundwater, deep confined storage, surface water bodies, and model structural error, which cannot be separated using satellite data alone.

4. **Inter-Satellite Mission Gap and Calibration:**  
   The 11-month observation gap (July 2017 – May 2018) between GRACE and GRACE-FO, combined with a +9.15 cm mean step offset between mission solutions, introduces calibration uncertainty. While multi-model step adjustments indicate that depletion remains significant across modeling choices (-1.81 to -1.25 cm/yr in the NW), short sub-period trends remain sensitive to step parameterization.

5. **Precipitation Data Truncation and Homogeneity:**  
   Homogenized precipitation observations from GPM IMERG V07B currently terminate in September 2025, truncating the final 10 months of the satellite record. Furthermore, sensor artifacts detected in alternative datasets (such as an artificial step jump in NASA POWER around 2014–2015) emphasize the necessity of rigorous sensor cross-checking.

---

## 5. Conclusions for Regional Water Assessment

1. **Broad Consensus on Regional Disparity:**  
   Satellite observations and peer-reviewed literature are consistent in identifying the Northwest as the area of most pronounced storage reduction, while southern coastal areas exhibit no detectable secular loss of bulk water mass.

2. **Reconciliation of Local and Regional Rates:**  
   A plausible scaling reconciles local and regional rates: a head change of 15–20 cm/yr multiplied by an assumed specific yield of 0.05–0.12 gives about 1–2.4 cm/yr of equivalent water thickness, the same order as the regional figure. This is an order-of-magnitude consistency check that rests on an assumed specific yield, not a validation.

3. **Baseline Lowering vs. Seasonal Cycles:**  
   The multi-decadal decline is not characterized by failing seasonal monsoon recharge, but by an unresolved net negative balance over multi-year cycles.

---

## References Cited

- **Ahmed, S. S., Zzaman, R. U., Jony, S. R., Himel, F. R., Sharmin, A., Rahman, A. H. M. K., Rahman, M. S., & Nowreen, S.** (2025). GroundHog: Revolutionizing GLDAS Groundwater Storage Downscaling for Enhanced Recharge Estimation in Bangladesh. *arXiv preprint arXiv:2503.22771 (preprint, not peer reviewed)*. https://doi.org/10.48550/arXiv.2503.22771
- **Ouyang, L., Zhao, Z., Zhou, D., Cao, J., Qin, J., Cao, Y., & He, Y.** (2024). Study on the Relationship between Groundwater and Land Subsidence in Bangladesh Combining GRACE and InSAR. *Remote Sensing*, 16(19), 3715. https://doi.org/10.3390/rs16193715
- **Purdy, A. J., David, C. H., Sikder, M. S., Reager, J. T., Chandanpurkar, H. A., Jones, N. L., & Matin, M. A.** (2019). An Open-Source Tool to Facilitate the Processing of GRACE Observations and GLDAS Outputs: An Evaluation in Bangladesh. *Frontiers in Environmental Science*, 7, 155. https://doi.org/10.3389/fenvs.2019.00155
- **Rodell, M., Famiglietti, J. S., Wiese, D. N., Reager, J. T., Beaudoing, H. K., Landerer, F. W., & Lo, M. H.** (2018). Emerging trends in global freshwater availability. *Nature*, 557(7707), 651–659. https://doi.org/10.1038/s41586-018-0123-1
- **Shamsudduha, M., & Taylor, R. G.** (2020). Groundwater storage dynamics in the world's large "aquifer" systems from GRACE: uncertainty and role of extreme precipitation. *Earth System Dynamics*, 11(3), 755–774. https://doi.org/10.5194/esd-11-755-2020
- **Shamsudduha, M., Taylor, R. G., & Longuevergne, L.** (2012). Monitoring groundwater storage changes in the highly seasonal humid tropics: Validation of GRACE measurements in the Bengal Basin. *Water Resources Research*, 48(2), W02508. https://doi.org/10.1029/2011WR010993
