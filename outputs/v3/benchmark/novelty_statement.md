# Statement of Novelty and Scientific Contribution

**Project:** Bengal Hydro Detective — NASA Space Apps Challenge 2026  
**Team:** Tenstral  
**Status:** PRELIMINARY

---

### Empirical Context and Extension of the Scientific Record

Prior satellite gravimetry studies of terrestrial storage dynamics in Bangladesh have evaluated either:
1. The historical **GRACE-1 mission era** (e.g., Shamsudduha et al., 2012 for 2003–2007; Purdy et al., 2019 for 2002–2016; Shamsudduha & Taylor, 2020 for 2002–2016), or
2. Shorter sub-windows bridging into the early **GRACE Follow-On (GRACE-FO)** operational phase (e.g., Ouyang et al., 2024 for 2015–2022).

This study extends the observational record across the full **24-year satellite gravimetry record (2002-04 to 2026-07)**, integrating the original GRACE mission, the inter-satellite transition gap, and the modern GRACE Follow-On era under an audit-calibrated non-parametric statistical framework (Effective Sample Size corrected Mann-Kendall with phase-randomized surrogate testing for regions exhibiting high autoregressive memory, circular block bootstrap 95% confidence intervals, and Benjamini-Hochberg False Discovery Rate control).

---

### Primary Empirical Findings Relative to Published Baselines:

1. **Continuity of Depletion Across Satellite Epochs:**
   - In the historical GRACE-1 era (2002–2017), we estimate a national total water storage depletion rate of **-0.68 cm/yr** [95% CI: -0.91, -0.45] ($-0.83\text{ km}^3/\text{yr}$), closely corroborating the $-0.85\text{ cm/yr}$ reported by Purdy et al. (2019) and sitting within the $-0.44$ to $-2.04\text{ km}^3/\text{yr}$ multi-model range of Shamsudduha et al. (2012).
   - Across the full 24-year record (2002–2026), national total water storage decline continues at **-0.51 cm/yr** [95% CI: -0.65, -0.37] ($-0.63\text{ km}^3/\text{yr}$).
   - A paired circular block bootstrap epoch test ($\Delta = \beta_{\text{Epoch 2}} - \beta_{\text{Epoch 1}}$) yields a 95% confidence interval spanning zero ($+0.21$ [$-0.71, +1.13$] cm/yr), indicating that total water storage depletion across Bangladesh has continued across missions without statistically significant secular acceleration or deceleration.

2. **Persistent Regional Disparity (Northwest Hotspot):**
   - The Northwest region (Rajshahi + Rangpur divisions) exhibits the steepest depletion rate nationally across all windows: **-1.25 cm/yr** [95% CI: -1.49, -1.01] ($-0.39\text{ km}^3/\text{yr}$, calibrated surrogate $p = 0.0036$) across the full record, and **-1.56 cm/yr** [95% CI: -1.95, -1.15] during the GRACE-1 era, in contrast to Southern regions (SW: $-0.05$ cm/yr, SE: $-0.05$ cm/yr) which display no statistically detectable multi-decadal trends.
   - This empirically corroborates the localized findings of Ahmed et al. (2025) and Purdy et al. (2019) regarding intensive dry-season Boro rice irrigation extraction in the Barind Tract.

3. **Homogeneous Precipitation vs. Subsurface Depletion:**
   - Using homogenized satellite precipitation (GPM IMERG V07B), national annual rainfall exhibits no detectable secular trend ($+2.04\text{ mm/yr}$, $p = 0.57$, FDR $q = 0.9342$), disproving earlier spurious rainfall trends ($+60\text{ mm/yr}$) resulting from MERRA-2 assimilation jumps in reanalysis datasets.
   - Analysis of seasonal storage response ratios ($\Delta\text{TWS} / P_{\text{monsoon}}$) over 23 complete monsoon seasons shows no statistically detectable secular trend across 4 of 6 regions, while Northwest storage depletion continues independently of seasonal monsoon rainfall variations.

4. **Multi-Model Storage Partitioning (Noah, VIC, CLSM):**
   - Incorporating three distinct land surface models (GLDAS Noah 2.1, VIC 2.1, and CLSM 2.2 [labeled *Non-independent / GRACE-assimilated*]), simulated unsaturated zone soil moisture shows no statistically significant secular trend in the Northwest during GRACE-FO (Noah: $+0.05$ cm/yr; VIC: $+0.20$ cm/yr; Ensemble: $-0.29$ cm/yr, $p = 0.58$).
   - The resulting partitioned subsurface residual ('groundwater + surface water + model error residual') declines at **-1.37 cm/yr** [95% CI: -2.02, -0.71], demonstrating that terrestrial storage loss in the Bengal Basin is concentrated in the subsurface, consistent with irrigation-driven unconfined aquifer drawdown.
