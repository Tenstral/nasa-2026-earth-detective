# Bengal Hydro Detective: Full-Record Terrestrial Water Storage Dynamics (2002–2026)

> [!IMPORTANT]
> **PRELIMINARY SCIENTIFIC ASSESSMENT**
> This synthesis evaluates terrestrial water storage (TWS) anomalies and satellite-derived precipitation
> across Bangladesh spanning the entire GRACE/GRACE-FO satellite gravimetry era (April 2002 to July 2026).
> Observations reflect composite column storage (groundwater, soil moisture, and surface water).

## 1. Executive Summary & Headline Trajectory
Across the 24-year satellite gravimetry record (257 observed monthly solutions
spanning 292 nominal months, with an 11-month gap during the 2017–2018 mission transition), Bangladesh displays a
statistically robust North-to-South hydrological divergence under Benjamini-Hochberg False Discovery Rate control (FDR $q < 0.05$):

- **Northwest Region (Rajshahi + Rangpur):** Exhibits persistent long-term storage depletion at **-1.25 cm/yr**
  (95% bootstrap CI: [-1.49, -1.01] cm/yr; -0.39 km³/yr; FDR $q = 0.0000$),
  classified as **`Significant`**.
- **Northeast Region (Sylhet + Mymensingh):** Displays steady depletion at **-0.56 cm/yr**
  (95% CI: [-0.70, -0.41] cm/yr; -0.12 km³/yr; FDR $q = 0.0000$),
  classified as **`Significant`**.
- **Central Region (Dhaka):** Depleting at **-0.47 cm/yr**
  (95% CI: [-0.60, -0.34] cm/yr; -0.08 km³/yr; FDR $q = 0.0000$),
  classified as **`Significant`**.
- **Coastal South (Southwest & Southeast):** Storage trends remain indistinguishable from zero (SW: -0.05 [-0.18, +0.09] cm/yr;
  SE: -0.05 [-0.16, +0.05] cm/yr),
  both classified as **`No detectable trend`**.
- **National Composite:** Aggregated across all 8 administrative divisions, Bangladesh exhibits an overall net storage loss of
  **-0.51 cm/yr** (95% CI: [-0.65, -0.38] cm/yr; **-0.63 km³/yr**; FDR $q = 0.0000$),
  classified as **`Significant`**.

## 2. Instrumental Transition & Epoch Invariance
To evaluate whether the transition between GRACE (ended June 2017) and GRACE-FO (begun June 2018) affected trend detection:
1. **Calibration Offset Test:** Fitting a step discontinuity at the 2018-06 boundary with Newey-West HAC covariance reveals local calibration step offsets
   in the Northwest (+9.15 cm, p = 0.028) and Central (+6.93 cm, p = 0.047) regions, while the National composite shows no statistically significant step (+5.81 cm, p = 0.071).
2. **Epoch Comparison:** A paired circular block-bootstrap difference test (B = 9,999) between Epoch 1 (2002–2017) and Epoch 2 (2018–2026)
   demonstrates that the 95% confidence interval for slope differences includes zero across all regions (NW difference: -0.10 [-1.60, +1.43] cm/yr; National: +0.21 [-0.71, +1.13] cm/yr).
   Consequently, multi-decadal depletion in the northern and central aquifers is **continuing at a similar rate** across satellite generations.

## 3. Hydrological Recovery & Recharge Efficiency Dynamics
Across 24 complete monsoon cycles (2002–2025):
- Absolute seasonal storage rebound (ΔTWS from pre-monsoon low to post-monsoon peak) averages ~50–60 cm and shows no significant linear trend (p > 0.05).
- However, **Recharge Efficiency** (fractional storage recovery per unit monsoon precipitation) exhibits a statistically significant downward slope nationally
  (-1.05%/yr, p = 0.0007), consistent with increasing surface runoff partitioning and episodic monsoon precipitation characteristics.

## 4. Methodological Safeguards & Data Availability
- All statistical tests control for autocorrelation using Hamed-Rao modified Mann-Kendall and circular block bootstrap CIs.
- AR(1) calibration simulations verify that the 11-month transition gap does not introduce artificial false positives (differential FPR = +0.036).
- Full source data, reproducibility scripts, and outputs reside in `outputs/v3/full_record/`.