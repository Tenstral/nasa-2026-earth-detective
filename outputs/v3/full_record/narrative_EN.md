# Bengal Hydro Detective: Full-Record Terrestrial Water Storage Dynamics (2002–2026)

> [!IMPORTANT]
> **PRELIMINARY SCIENTIFIC ASSESSMENT**
> This synthesis evaluates terrestrial water storage (TWS) anomalies, homogenized satellite precipitation (GPM IMERG V07B),
> and multi-model land surface soil moisture (GLDAS Noah 2.1, VIC 2.1, and CLSM 2.2) across Bangladesh spanning
> the satellite gravimetry record (April 2002 to July 2026). Total water storage reflects vertically integrated column storage,
> combining unsaturated soil moisture, surface water bodies, and unconfined groundwater.

## 1. Executive Summary & Calibrated Trajectory
Across the 24-year satellite gravimetry record (257 observed monthly solutions
spanning 292 nominal months, with an 11-month transition gap during 2017–2018), Bangladesh displays a marked
spatial gradient in total water storage trends evaluated under audit-calibrated significance criteria:

- **Northwest Region (Rajshahi + Rangpur):** Exhibits persistent long-term storage depletion at **-1.25 cm/yr**
  (95% bootstrap CI: [-1.54, -0.96] cm/yr; **-0.39 km³/yr**; calibrated surrogate $p = 0.0005$, FDR $q = 0.0015$),
  classified as **`Significant`**.
- **Northeast Region (Sylhet + Mymensingh):** Displays long-term depletion at **-0.56 cm/yr**
  (95% CI: [-0.70, -0.42] cm/yr; **-0.12 km³/yr**; ESS-MK $p < 0.0001$, FDR $q < 0.0001$),
  classified as **`Significant`**.
- **Central Region (Dhaka):** Depleting at **-0.47 cm/yr**
  (95% CI: [-0.62, -0.34] cm/yr; **-0.08 km³/yr**; ESS-MK $p < 0.0001$, FDR $q < 0.0001$),
  classified as **`Significant`**.
- **Coastal South (Southwest & Southeast):** Storage trends remain indistinguishable from zero (SW: -0.05 [-0.17, +0.08] cm/yr;
  SE: -0.05 [-0.17, +0.06] cm/yr),
  both classified as **`No detectable trend`** (below detection limit in shorter windows).
- **National Composite:** Aggregated across Bangladesh, total water storage exhibits a net decline of
  **-0.51 cm/yr** (95% CI: [-0.66, -0.38] cm/yr; **-0.63 km³/yr**; ESS-MK $p < 0.0001$, FDR $q < 0.0001$),
  classified as **`Significant`**.

## 2. Instrumental Transition & Multi-Window Robustness
To test whether the 11-month gap between GRACE and GRACE-FO introduced statistical artifacts:
1. **Transition Offset Sensitivity:** Fitting a step discontinuity at the 2018-06 boundary indicates an apparent step of +9.15 cm in the Northwest (p = 0.028), but this step is not statistically significant when transition buffer months (±6 months) are excluded (p = 0.17).
2. **Three-Way Slope Reporting:** For the Northwest, the single-line slope is -1.25 cm/yr, the step-adjusted slope is -1.34 cm/yr, and the transition-excluded slope is -1.23 cm/yr (span: -1.23 to -1.34 cm/yr). Lead evidence remains the gap-free GRACE-1 era (-1.56 cm/yr [95% CI: -1.95, -1.15] cm/yr).
3. **Epoch Invariance:** A paired circular block-bootstrap test between Epoch 1 (2002–2017) and Epoch 2 (2018–2026) confirms the difference CI includes zero (NW difference: -0.10 [-1.60, +1.43] cm/yr; National: +0.21 [-0.71, +1.13] cm/yr), indicating consistent secular depletion rates across satellite generations.

## 3. Homogenized Precipitation vs. Seasonal Storage Response
Analysis of GPM IMERG V07B precipitation across 2002–2025 shows stationary annual rainfall nationally (+2.04 mm/yr, p = 0.6395, classified as `No detectable trend`).
Across 22 complete monsoon cycles:
- Seasonal storage rebound alone (ΔTWS from pre-monsoon low to post-monsoon peak) averages 54.0 cm nationally and exhibits `No detectable trend` (p = 0.4298).
- The **seasonal storage response ratio** (rebound / monsoon precipitation) exhibits a suggestive upward slope nationally (+0.136%/yr, raw p = 0.0208, FDR q = 0.1105, classified as `Suggestive increase`), while Northwest response ratio shows `No detectable trend` (p = 0.3784).
> *Limitations:* The seasonal storage response ratio (ΔTWS / P_monsoon) reflects bulk total water storage change, integrating unsaturated soil moisture and surface water bodies alongside groundwater, and does not represent an isolated groundwater recharge coefficient.

## 4. Multi-Model Land Surface Partitioning (GLDAS)
Evaluating three land surface models (GLDAS Noah 2.1, VIC 2.1, and CLSM 2.2 [labeled *Non-independent / GRACE-assimilated*]):
- Simulated topsoil moisture (0–2 m) shows no statistically significant secular decline in the Northwest during GRACE-FO (Noah: +0.05 cm/yr; VIC: +0.20 cm/yr; Ensemble: -0.29 cm/yr, p = 0.58).
- The resulting partitioned subsurface residual ('groundwater + surface water + model error residual') declines at **-1.37 cm/yr** [95% CI: -2.02, -0.71], most of the decline is not accounted for by simulated soil moisture; groundwater and surface water cannot be separated here. This pattern is consistent with, not proof of, agricultural extraction from the deep subsurface.

## 5. Methodological Safeguards & Data Availability
- Statistical significance is determined using calibrated Effective Sample Size Mann-Kendall with phase-randomized surrogate verification for autocorrelated series.
- Full source data, reproducibility pipelines, and diagnostic figures reside in `outputs/v3/full_record/` and `outputs/v3/gldas_split/`.