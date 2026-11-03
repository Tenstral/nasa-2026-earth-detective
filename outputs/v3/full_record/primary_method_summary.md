# Primary Significance Testing Method and Independent Null Validation Audit

> **PRELIMINARY — NASA Space Apps Challenge 2026**
> **Team Tenstral | Project: Bengal Hydro Detective**
> Documents the unified primary significance method assigned across all regions, validated using an **independent AR(1) null generator** fitted directly to each region's empirical detrended residuals with the real satellite mission gap pattern. Pass criteria: False-Positive Rate (FPR) $\in [3.5\%, 6.5\%]$ and $95\%$ CI coverage $\in [93.0\%, 97.0\%]$.

---

## 1. Independent Null Generator Validation Results (All 6 Regions)

Validation was conducted using an independent null generator: an autoregressive AR(1) process parameterised by each region's empirical detrended residual autocorrelation ($\phi$) and standard deviation ($\sigma$), simulated under the exact 257-month GRACE/GRACE-FO observation mask (including the 11-month transition gap) across 2,000 Monte Carlo realizations.

| Region | Empirical Noise $\phi$ | Residual SD $\sigma$ (cm) | Primary Method | Null FPR (Nominal 5.0%) | 95% CI Coverage (Nominal 95.0%) | Status | Method Pass Notes |
|---|---|---|---|---|---|---|---|
| **NW** | `0.5537` | 7.17 | `Calibrated ESS-MK` | **4.10%** | **95.90%** | **`PASSED`** | Hurwicz bias-corrected rank bounds strictly satisfy calibration bounds |
| **NE** | `0.4340` | 5.88 | `Calibrated ESS-MK` | **5.40%** | **94.60%** | **`PASSED`** | Hurwicz bias-corrected rank bounds strictly satisfy calibration bounds |
| **Central** | `0.4813` | 5.55 | `Calibrated ESS-MK` | **5.30%** | **94.70%** | **`PASSED`** | Hurwicz bias-corrected rank bounds strictly satisfy calibration bounds |
| **SW** | `0.6248` | 4.31 | `Calibrated ESS-MK` | **5.45%** | **94.55%** | **`PASSED`** | Hurwicz bias-corrected rank bounds strictly satisfy calibration bounds |
| **SE** | `0.5907` | 3.56 | `Calibrated ESS-MK` | **5.20%** | **94.80%** | **`PASSED`** | Hurwicz bias-corrected rank bounds strictly satisfy calibration bounds |
| **National** | `0.5394` | 4.74 | `Calibrated ESS-MK` | **5.05%** | **94.95%** | **`PASSED`** | Hurwicz bias-corrected rank bounds strictly satisfy calibration bounds |

---

## 2. Complete Primary Method and Side-by-Side Verdict Inventory (All 4 Windows)

Calibrated ESS-MK is applied as the **single primary significance test across all regions**. The side-by-side Surrogate test (phase-randomized Fourier, 10,000 runs) and Hamed-Rao test are presented alongside for full methodological transparency.

| Window | Entity | Variable | Primary Method | Primary Slope (95% CI) | Primary p | FDR q | Primary Verdict | Surrogate Slope (95% CI) | Surrogate p | Surrogate Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| `full_record` | **NW** | TWS (cm/yr) | `Calibrated ESS-MK` | -1.25 [-1.50, -1.02] | < 0.0001 | < 0.0001 | **`Significant`** | -1.25 [-1.54, -0.97] | 0.0001 | `Significant (nominal surrogate)` |
| `full_record` | **NW** | PRECIP (mm/yr) | `Calibrated ESS-MK` | -1.91 [-11.04, +4.48] | 0.5427 | 0.8968 | `No detectable trend` | — | — | — |
| `full_record` | **NE** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.56 [-0.70, -0.42] | < 0.0001 | < 0.0001 | **`Significant`** | -0.56 [-0.73, -0.38] | 0.0001 | `Significant (nominal surrogate)` |
| `full_record` | **NE** | PRECIP (mm/yr) | `Calibrated ESS-MK` | -0.59 [-15.38, +16.13] | 0.9068 | 0.9342 | `No detectable trend` | — | — | — |
| `full_record` | **Central** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.47 [-0.62, -0.34] | < 0.0001 | < 0.0001 | **`Significant`** | -0.47 [-0.64, -0.31] | 0.0001 | `Significant (nominal surrogate)` |
| `full_record` | **Central** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +0.89 [-9.75, +12.72] | 0.8298 | 0.9342 | `No detectable trend` | — | — | — |
| `full_record` | **SW** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.05 [-0.20, +0.10] | 0.5459 | 0.8968 | `No detectable trend` | -0.05 [-0.17, +0.08] | 0.5203 | `No detectable trend (surrogate)` |
| `full_record` | **SW** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +2.25 [-7.31, +14.56] | 0.5165 | 0.8968 | `No detectable trend` | — | — | — |
| `full_record` | **SE** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.05 [-0.17, +0.06] | 0.3754 | 0.8968 | `No detectable trend` | -0.05 [-0.16, +0.06] | 0.4776 | `No detectable trend (surrogate)` |
| `full_record` | **SE** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +1.76 [-9.35, +13.75] | 0.7121 | 0.9342 | `No detectable trend` | — | — | — |
| `full_record` | **National** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.51 [-0.66, -0.38] | < 0.0001 | < 0.0001 | **`Significant`** | -0.51 [-0.66, -0.36] | 0.0001 | `Significant (nominal surrogate)` |
| `full_record` | **National** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +2.04 [-7.70, +12.45] | 0.6395 | 0.9342 | `No detectable trend` | — | — | — |
| `grace_era` | **NW** | TWS (cm/yr) | `Calibrated ESS-MK` | -1.56 [-1.96, -1.17] | < 0.0001 | < 0.0001 | **`Significant`** | -1.56 [-2.03, -1.11] | 0.0001 | `Significant (nominal surrogate)` |
| `grace_era` | **NW** | PRECIP (mm/yr) | `Calibrated ESS-MK` | -6.39 [-26.68, +7.62] | 0.3609 | 0.6435 | `No detectable trend` | — | — | — |
| `grace_era` | **NE** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.72 [-0.99, -0.49] | < 0.0001 | < 0.0001 | **`Significant`** | -0.72 [-1.02, -0.43] | 0.0001 | `Significant (nominal surrogate)` |
| `grace_era` | **NE** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +2.95 [-30.83, +40.10] | 0.8253 | 0.9339 | `No detectable trend` | — | — | — |
| `grace_era` | **Central** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.63 [-0.86, -0.42] | < 0.0001 | < 0.0001 | **`Significant`** | -0.63 [-0.91, -0.35] | 0.0001 | `Significant (nominal surrogate)` |
| `grace_era` | **Central** | PRECIP (mm/yr) | `Calibrated ESS-MK` | -1.08 [-29.14, +23.74] | 0.8802 | 0.9433 | `No detectable trend` | — | — | — |
| `grace_era` | **SW** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.13 [-0.36, +0.10] | 0.2896 | 0.5917 | `No detectable trend` | -0.13 [-0.28, +0.03] | 0.1146 | `No detectable trend (surrogate)` |
| `grace_era` | **SW** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +6.07 [-14.30, +26.97] | 0.5078 | 0.8016 | `No detectable trend` | — | — | — |
| `grace_era` | **SE** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.12 [-0.32, +0.07] | 0.2296 | 0.5510 | `No detectable trend` | -0.12 [-0.27, +0.03] | 0.1113 | `No detectable trend (surrogate)` |
| `grace_era` | **SE** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +11.33 [-9.15, +45.48] | 0.2911 | 0.5917 | `No detectable trend` | — | — | — |
| `grace_era` | **National** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.68 [-0.92, -0.45] | < 0.0001 | < 0.0001 | **`Significant`** | -0.68 [-0.92, -0.45] | 0.0001 | `Significant (nominal surrogate)` |
| `grace_era` | **National** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +3.08 [-18.81, +25.82] | 0.7689 | 0.9339 | `No detectable trend` | — | — | — |
| `grace_fo_era` | **NW** | TWS (cm/yr) | `Calibrated ESS-MK` | -1.67 [-3.32, +0.06] | 0.0549 | 0.4626 | `No detectable trend` | -1.67 [-3.26, -0.08] | 0.0354 | `Significant (nominal surrogate)` |
| `grace_fo_era` | **NW** | PRECIP (mm/yr) | `Calibrated ESS-MK` | -2.20 [-48.65, +64.06] | 0.8932 | 0.9409 | `No detectable trend` | — | — | — |
| `grace_fo_era` | **NE** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.79 [-1.78, +0.19] | 0.1073 | 0.5517 | `No detectable trend` | -0.79 [-1.84, +0.27] | 0.1929 | `No detectable trend (surrogate)` |
| `grace_fo_era` | **NE** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +26.37 [-47.37, +122.85] | 0.4925 | 0.7725 | `No detectable trend` | — | — | — |
| `grace_fo_era` | **Central** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.81 [-1.79, +0.20] | 0.1056 | 0.5517 | `No detectable trend` | -0.81 [-1.92, +0.30] | 0.2051 | `No detectable trend (surrogate)` |
| `grace_fo_era` | **Central** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +15.56 [-40.61, +87.38] | 0.6120 | 0.8812 | `No detectable trend` | — | — | — |
| `grace_fo_era` | **SW** | TWS (cm/yr) | `Calibrated ESS-MK` | +0.53 [-0.63, +1.53] | 0.3419 | 0.7062 | `No detectable trend` | +0.53 [-0.49, +1.56] | 0.3652 | `No detectable trend (surrogate)` |
| `grace_fo_era` | **SW** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +8.20 [-78.90, +102.87] | 0.8111 | 0.9409 | `No detectable trend` | — | — | — |
| `grace_fo_era` | **SE** | TWS (cm/yr) | `Calibrated ESS-MK` | +0.45 [-0.27, +1.18] | 0.1848 | 0.6516 | `No detectable trend` | +0.45 [-0.32, +1.24] | 0.3109 | `No detectable trend (surrogate)` |
| `grace_fo_era` | **SE** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +5.06 [-59.24, +80.72] | 0.8790 | 0.9409 | `No detectable trend` | — | — | — |
| `grace_fo_era` | **National** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.47 [-1.50, +0.53] | 0.3111 | 0.7057 | `No detectable trend` | -0.47 [-1.52, +0.58] | 0.4534 | `No detectable trend (surrogate)` |
| `grace_fo_era` | **National** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +3.09 [-50.37, +69.85] | 0.9109 | 0.9409 | `No detectable trend` | — | — | — |
| `recent_2020` | **NW** | TWS (cm/yr) | `Calibrated ESS-MK` | -2.93 [-4.97, -0.78] | 0.0107 | 0.0772 | `method-dependent` | -2.93 [-5.02, -0.83] | 0.0001 | `Significant (nominal surrogate)` |
| `recent_2020` | **NW** | PRECIP (mm/yr) | `Calibrated ESS-MK` | -26.61 [-119.36, +43.63] | 0.4014 | 0.9766 | `No detectable trend` | — | — | — |
| `recent_2020` | **NE** | TWS (cm/yr) | `Calibrated ESS-MK` | -1.06 [-2.64, +0.46] | 0.1682 | 0.6884 | `No detectable trend` | -1.06 [-2.78, +0.64] | 0.3860 | `No detectable trend (surrogate)` |
| `recent_2020` | **NE** | PRECIP (mm/yr) | `Calibrated ESS-MK` | -1.35 [-84.11, +105.69] | 0.9628 | 0.9811 | `No detectable trend` | — | — | — |
| `recent_2020` | **Central** | TWS (cm/yr) | `Calibrated ESS-MK` | -1.19 [-2.69, +0.43] | 0.1296 | 0.6663 | `No detectable trend` | -1.19 [-2.96, +0.58] | 0.3287 | `No detectable trend (surrogate)` |
| `recent_2020` | **Central** | PRECIP (mm/yr) | `Calibrated ESS-MK` | -7.68 [-95.32, +72.65] | 0.8143 | 0.9811 | `No detectable trend` | — | — | — |
| `recent_2020` | **SW** | TWS (cm/yr) | `Calibrated ESS-MK` | +0.03 [-1.60, +1.49] | 0.9506 | 0.9811 | `No detectable trend` | +0.03 [-1.54, +1.61] | 0.9780 | `No detectable trend (surrogate)` |
| `recent_2020` | **SW** | PRECIP (mm/yr) | `Calibrated ESS-MK` | -8.73 [-112.46, +95.41] | 0.8227 | 0.9811 | `No detectable trend` | — | — | — |
| `recent_2020` | **SE** | TWS (cm/yr) | `Calibrated ESS-MK` | +0.39 [-0.80, +1.43] | 0.4069 | 0.9766 | `No detectable trend` | +0.39 [-0.83, +1.61] | 0.6755 | `No detectable trend (surrogate)` |
| `recent_2020` | **SE** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +24.07 [-84.00, +144.84] | 0.6846 | 0.9811 | `No detectable trend` | — | — | — |
| `recent_2020` | **National** | TWS (cm/yr) | `Calibrated ESS-MK` | -1.02 [-2.53, +0.51] | 0.1721 | 0.6884 | `No detectable trend` | -1.02 [-2.61, +0.57] | 0.3528 | `No detectable trend (surrogate)` |
| `recent_2020` | **National** | PRECIP (mm/yr) | `Calibrated ESS-MK` | -28.57 [-115.32, +52.29] | 0.4613 | 0.9811 | `No detectable trend` | — | — | — |

---

## 3. Decision Rules & Headline Verification

1. **Single Primary Method Standardized Across All Regions:**
   - **Effective-Sample-Size (ESS) Corrected Mann-Kendall with Analytical Theil-Sen Duality:** Selected as the primary statistical engine for all 6 regions and both variables (TWS storage and IMERG rainfall). Passes independent null validation across all regions with empirical FPR in $[4.10\%, 5.45\%]$ (nominal $5.0\%$) and $95\%$ CI coverage in $[94.55\%, 95.95\%]$ (nominal $95.0\%$).
   - Eliminates circularity: the test is validated against an independent AR(1) null model rather than surrogates constructed by the same algorithm.

2. **Resolution of Method-Dependence for Northwest (NW) in recent_2020:**
   - In the legacy `recent_2020` sensitivity window (2020-01 to 2026-07), NW has a raw ESS-MK p-value of $p = 0.01072$.
   - When evaluated within the complete regional family ($m=36$), the Benjamini-Hochberg FDR adjusted q-value is $q = 0.386 > 0.05$.
   - Because NW `recent_2020` fails FDR under the calibrated primary method (and previously appeared significant only due to an artificial surrogate resolution floor), its verdict is strictly labeled **`method-dependent`** and is **NOT classified as Significant**.

3. **Consistency Between Epochs:**
   - In the superset `grace_fo_era` (2018-06 to 2026-07), NW exhibits $p = 0.05487$ ($95\%$ CI $[-3.32, +0.06]$ includes zero) and is classified as `No detectable trend` (below detection limit).
   - Labeling `recent_2020` as `method-dependent` resolves the logical inversion where a short 6-year window previously claimed significance while its 8-year superset did not.