# Statement of Novelty and Scientific Contribution

**Project:** Bengal Hydro Detective — NASA Space Apps Challenge 2026
**Team:** Tenstral
**Status:** PRELIMINARY

---

### Empirical Context and Extension of the Scientific Record

Prior satellite gravimetry studies of terrestrial storage dynamics in Bangladesh have evaluated either:
1. The historical **GRACE-1 mission era** (e.g., Shamsudduha et al., 2012 for 2003–2007; Purdy et al., 2019 for 2002–2016; Shamsudduha & Taylor, 2020 for 2002–2016), or
2. Shorter sub-windows bridging into the early **GRACE Follow-On (GRACE-FO)** operational phase (e.g., Ouyang et al., 2024 for 2015–2022).

This study extends the observational record across the full **24-year satellite gravimetry record (2002-04 to 2026-07)**, integrating the original GRACE mission, the inter-satellite transition gap, and the modern GRACE Follow-On era under an audit-calibrated non-parametric statistical framework (Effective Sample Size corrected Mann-Kendall with Hurwicz AR(1) bias correction, duality-aligned Theil-Sen 95% confidence intervals, and Benjamini-Hochberg False Discovery Rate control).

---

### Primary Empirical Findings Relative to Published Baselines:

1. **Continuity of Depletion Across Satellite Epochs:**
   - In the historical GRACE-1 era (2002–2017), we estimate a national total water storage depletion rate of **-0.68 cm/yr** [95% CI: -0.92, -0.45] (-0.83 km³/yr), which provides a transition-free baseline.
   - Across the full 24-year record (2002–2026), national total water storage decline continues at **-0.51 cm/yr** [95% CI: -0.66, -0.38] (-0.63 km³/yr).
   - A paired circular block bootstrap epoch test ($\Delta = eta_{	ext{Epoch 2}} - eta_{	ext{Epoch 1}}$) yields a 95% confidence interval spanning zero ($+0.21$ [$-0.71, +1.13$] cm/yr), indicating that total water storage depletion across Bangladesh has continued across missions without statistically significant secular acceleration or deceleration.

2. **Persistent Regional Disparity (Northwest Hotspot):**
   - The Northwest region (Rajshahi + Rangpur divisions) exhibits the steepest depletion rate nationally across historical and full-record windows: **-1.25 cm/yr** [95% CI: -1.50, -1.02] (-0.39 km³/yr, calibrated ESS-MK $p < 0.0001$, FDR $q < 0.0001$) across the full record, and **-1.56 cm/yr** [95% CI: -1.96, -1.17] during the transition-free GRACE-1 era.
   - In contrast, Southern regions (SW: $-0.05$ cm/yr, SE: $-0.05$ cm/yr) display no statistically detectable multi-decadal trends.
   - In the shorter GRACE-FO era (2018–2026), Northwest total water storage slope is estimated at **-1.67 cm/yr** [95% CI: -3.32, 0.06] ($p = 0.0549$, FDR $q = 0.4626$, `No detectable trend` under Calibrated ESS-MK, with CI spanning zero). In the recent sensitivity window (`recent_2020`), the NW verdict is method-dependent (Theil-Sen slope: -2.93 cm/yr [95% CI: -4.97, -0.78], raw $p = 0.0107$, but within-window FDR $q = 0.0772 > 0.05$), and is therefore labeled `method-dependent` rather than Significant.

3. **Homogeneous Precipitation vs. Subsurface Depletion:**
   - Using homogenized satellite precipitation (GPM IMERG V07B), national annual rainfall exhibits no detectable secular trend (slope $+2.04	ext{ mm/yr}$, $p = 0.57$, FDR $q = 0.9342$, `No detectable trend`).
   - We detected an artifact in NASA POWER rainfall by cross-checking with IMERG; cause not established. NASA POWER exhibits an abrupt upward step change (+45% to +84%) around 2014–2015 that produced implausible spurious rainfall trends (+29 to +86 mm/yr). GPM IMERG currently ends in 2025-09, truncating the last 10 months of full_record and GRACE-FO windows.
   - Analysis of seasonal storage response ratios ($\Delta	ext{TWS} / P_{	ext{monsoon}}$) over 23 complete monsoon seasons shows no statistically detectable secular trend across 4 of 6 regions, while Northwest storage depletion continues independently of seasonal monsoon rainfall variations.

4. **Multi-Model Storage Partitioning (Independent Noah+VIC vs. Assimilated CLSM):**
   - Incorporating two independent open-loop land surface models (GLDAS Noah 2.1 and VIC 2.1), simulated unsaturated zone soil moisture shows no statistically significant secular trend in the Northwest during GRACE-FO (Noah: $+0.05$ cm/yr; VIC: $+0.20$ cm/yr; independent range: $[+0.05, +0.20]$ cm/yr).
   - The resulting partitioned residual storage ('groundwater + surface water + model error residual') spans an estimated rate of $[-1.92, -1.70]$ cm/yr during GRACE-FO and $[-1.12, -1.11]$ cm/yr across the full record across independent models.
   - Most of the decline is not accounted for by simulated soil moisture; groundwater and surface water cannot be separated here. This pattern is consistent with, not proof of, agricultural groundwater extraction from the deep subsurface. CLSM 2.2 is reported separately as it assimilates GRACE observations via EnKF and cannot serve as an independent partition.
