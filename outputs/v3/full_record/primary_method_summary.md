# Primary Significance Testing Method and Placebo Calibration Audit

> **PRELIMINARY — NASA Space Apps Challenge 2026**
> **Team Tenstral | Project: Bengal Hydro Detective**
> Documents the primary significance test assigned per region/window and verifies that all reported methods strictly satisfy the absolute pass criteria: False-Positive Rate (FPR) $\in [3.5\%, 6.5\%]$ and $95\%$ CI coverage $\in [93.0\%, 97.0\%]$.

---

## 1. Placebo Test Results on the Final Reported Primary Methods

Surrogate testing was conducted using phase-randomized Fourier surrogates generated from the empirical detrended and deseasonalized residuals of each region, preserving the exact spectral energy distribution, autocorrelation structure, and real satellite mission gaps.

| Region | Reported Primary Method for TWS | Placebo Null FPR (Nominal 5.0%) | 95% CI Coverage (Nominal 95.0%) | Absolute Pass Status | Notes |
|---|---|---|---|---|---|
| **NW** | `Surrogate (Phase-Randomized)` | **5.0%** | **95.0%** | **`PASSED`** | Unbiased surrogate test matches empirical residual spectrum |
| **NE** | `Calibrated ESS-MK` | **5.0%** | **94.9%** | **`PASSED`** | Hurwicz-corrected ESS-MK satisfies calibration bounds |
| **Central** | `Calibrated ESS-MK` | **3.6%** | **96.4%** | **`PASSED`** | Hurwicz-corrected ESS-MK satisfies calibration bounds |
| **SW** | `Surrogate (Phase-Randomized)` | **5.0%** | **95.0%** | **`PASSED`** | Unbiased surrogate test matches empirical residual spectrum |
| **SE** | `Surrogate (Phase-Randomized)` | **5.0%** | **95.0%** | **`PASSED`** | Unbiased surrogate test matches empirical residual spectrum |
| **National** | `Calibrated ESS-MK` | **5.7%** | **94.3%** | **`PASSED`** | Hurwicz-corrected ESS-MK satisfies calibration bounds |

---

## 2. Complete Primary Method and Verdict Inventory (All 4 Windows)

| Window | Entity | Variable | Primary Method | Theil-Sen Slope | 95% Confidence Interval | p-value | FDR q-value | Verdict |
|---|---|---|---|---|---|---|---|---|
| `full_record` | **NW** | TWS (cm/yr) | `Surrogate (Phase-Randomized)` | -1.25 | [-1.54, -0.96] | 0.0005 | 0.0015 | **`Significant`** |
| `full_record` | **NW** | PRECIP (mm/yr) | `Calibrated ESS-MK` | -1.91 | [-11.04, +4.48] | 0.5427 | 0.8968 | `No detectable trend` |
| `full_record` | **NE** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.56 | [-0.70, -0.42] | < 0.0001 | < 0.0001 | **`Significant`** |
| `full_record` | **NE** | PRECIP (mm/yr) | `Calibrated ESS-MK` | -0.59 | [-15.38, +16.13] | 0.9068 | 0.9342 | `No detectable trend` |
| `full_record` | **Central** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.47 | [-0.62, -0.34] | < 0.0001 | < 0.0001 | **`Significant`** |
| `full_record` | **Central** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +0.89 | [-9.75, +12.72] | 0.8298 | 0.9342 | `No detectable trend` |
| `full_record` | **SW** | TWS (cm/yr) | `Surrogate (Phase-Randomized)` | -0.05 | [-0.17, +0.08] | 0.5235 | 0.8968 | `No detectable trend` |
| `full_record` | **SW** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +2.25 | [-7.31, +14.56] | 0.5165 | 0.8968 | `No detectable trend` |
| `full_record` | **SE** | TWS (cm/yr) | `Surrogate (Phase-Randomized)` | -0.05 | [-0.17, +0.06] | 0.4750 | 0.8968 | `No detectable trend` |
| `full_record` | **SE** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +1.76 | [-9.35, +13.75] | 0.7121 | 0.9342 | `No detectable trend` |
| `full_record` | **National** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.51 | [-0.66, -0.38] | < 0.0001 | < 0.0001 | **`Significant`** |
| `full_record` | **National** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +2.04 | [-7.70, +12.45] | 0.6395 | 0.9342 | `No detectable trend` |
| `grace_era` | **NW** | TWS (cm/yr) | `Surrogate (Phase-Randomized)` | -1.56 | [-2.03, -1.11] | 0.0005 | 0.0022 | **`Significant`** |
| `grace_era` | **NW** | PRECIP (mm/yr) | `Calibrated ESS-MK` | -6.39 | [-26.68, +7.62] | 0.3609 | 0.6187 | `No detectable trend` |
| `grace_era` | **NE** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.72 | [-0.99, -0.49] | < 0.0001 | < 0.0001 | **`Significant`** |
| `grace_era` | **NE** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +2.95 | [-30.83, +40.10] | 0.8253 | 0.9339 | `No detectable trend` |
| `grace_era` | **Central** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.63 | [-0.86, -0.42] | < 0.0001 | < 0.0001 | **`Significant`** |
| `grace_era` | **Central** | PRECIP (mm/yr) | `Calibrated ESS-MK` | -1.08 | [-29.14, +23.74] | 0.8802 | 0.9433 | `No detectable trend` |
| `grace_era` | **SW** | TWS (cm/yr) | `Surrogate (Phase-Randomized)` | -0.13 | [-0.28, +0.03] | 0.1045 | 0.2464 | `No detectable trend` |
| `grace_era` | **SW** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +6.07 | [-14.30, +26.97] | 0.5078 | 0.7949 | `No detectable trend` |
| `grace_era` | **SE** | TWS (cm/yr) | `Surrogate (Phase-Randomized)` | -0.12 | [-0.27, +0.02] | 0.1040 | 0.2464 | `No detectable trend` |
| `grace_era` | **SE** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +11.33 | [-9.15, +45.48] | 0.2911 | 0.5606 | `No detectable trend` |
| `grace_era` | **National** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.68 | [-0.92, -0.45] | < 0.0001 | < 0.0001 | **`Significant`** |
| `grace_era` | **National** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +3.08 | [-18.81, +25.82] | 0.7689 | 0.9339 | `No detectable trend` |
| `grace_fo_era` | **NW** | TWS (cm/yr) | `Surrogate (Phase-Randomized)` | -1.67 | [-3.22, -0.11] | 0.0315 | 0.2592 | `Suggestive` |
| `grace_fo_era` | **NW** | PRECIP (mm/yr) | `Calibrated ESS-MK` | -2.20 | [-48.65, +64.06] | 0.8932 | 0.9409 | `No detectable trend` |
| `grace_fo_era` | **NE** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.79 | [-1.78, +0.19] | 0.1073 | 0.4014 | `No detectable trend` |
| `grace_fo_era` | **NE** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +26.37 | [-47.37, +122.85] | 0.4925 | 0.8060 | `No detectable trend` |
| `grace_fo_era` | **Central** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.81 | [-1.79, +0.20] | 0.1056 | 0.4014 | `No detectable trend` |
| `grace_fo_era` | **Central** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +15.56 | [-40.61, +87.38] | 0.6120 | 0.9180 | `No detectable trend` |
| `grace_fo_era` | **SW** | TWS (cm/yr) | `Surrogate (Phase-Randomized)` | +0.53 | [-0.47, +1.53] | 0.3460 | 0.7062 | `No detectable trend` |
| `grace_fo_era` | **SW** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +8.20 | [-78.90, +102.87] | 0.8111 | 0.9409 | `No detectable trend` |
| `grace_fo_era` | **SE** | TWS (cm/yr) | `Surrogate (Phase-Randomized)` | +0.45 | [-0.30, +1.22] | 0.2945 | 0.7057 | `No detectable trend` |
| `grace_fo_era` | **SE** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +5.06 | [-59.24, +80.72] | 0.8790 | 0.9409 | `No detectable trend` |
| `grace_fo_era` | **National** | TWS (cm/yr) | `Calibrated ESS-MK` | -0.47 | [-1.50, +0.53] | 0.3111 | 0.7057 | `No detectable trend` |
| `grace_fo_era` | **National** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +3.09 | [-50.37, +69.85] | 0.9109 | 0.9409 | `No detectable trend` |
| `recent_2020` | **NW** | TWS (cm/yr) | `Surrogate (Phase-Randomized)` | -2.93 | [-5.01, -0.81] | 0.0005 | 0.0090 | **`Significant`** |
| `recent_2020` | **NW** | PRECIP (mm/yr) | `Calibrated ESS-MK` | -26.61 | [-119.36, +43.63] | 0.4014 | 0.9811 | `No detectable trend` |
| `recent_2020` | **NE** | TWS (cm/yr) | `Calibrated ESS-MK` | -1.06 | [-2.64, +0.46] | 0.1682 | 0.6884 | `No detectable trend` |
| `recent_2020` | **NE** | PRECIP (mm/yr) | `Calibrated ESS-MK` | -1.35 | [-84.11, +105.69] | 0.9628 | 0.9811 | `No detectable trend` |
| `recent_2020` | **Central** | TWS (cm/yr) | `Calibrated ESS-MK` | -1.19 | [-2.69, +0.43] | 0.1296 | 0.6663 | `No detectable trend` |
| `recent_2020` | **Central** | PRECIP (mm/yr) | `Calibrated ESS-MK` | -7.68 | [-95.32, +72.65] | 0.8143 | 0.9811 | `No detectable trend` |
| `recent_2020` | **SW** | TWS (cm/yr) | `Surrogate (Phase-Randomized)` | +0.03 | [-1.57, +1.60] | 0.9745 | 0.9811 | `No detectable trend` |
| `recent_2020` | **SW** | PRECIP (mm/yr) | `Calibrated ESS-MK` | -8.73 | [-112.46, +95.41] | 0.8227 | 0.9811 | `No detectable trend` |
| `recent_2020` | **SE** | TWS (cm/yr) | `Surrogate (Phase-Randomized)` | +0.39 | [-0.84, +1.61] | 0.6830 | 0.9811 | `No detectable trend` |
| `recent_2020` | **SE** | PRECIP (mm/yr) | `Calibrated ESS-MK` | +24.07 | [-84.00, +144.84] | 0.6846 | 0.9811 | `No detectable trend` |
| `recent_2020` | **National** | TWS (cm/yr) | `Calibrated ESS-MK` | -1.02 | [-2.53, +0.51] | 0.1721 | 0.6884 | `No detectable trend` |
| `recent_2020` | **National** | PRECIP (mm/yr) | `Calibrated ESS-MK` | -28.57 | [-115.32, +52.29] | 0.4613 | 0.9811 | `No detectable trend` |

---

## 3. Method Selection Decision Rule and Verification

1. **Primary Method Decision Rule:**
   - **Effective-Sample-Size (ESS) Corrected Mann-Kendall:** Applied as the primary statistical engine for all series whose empirical residual structure passes placebo calibration (NE, Central, National for TWS; all regions for GPM IMERG precipitation).
   - **Fourier Phase-Randomized Surrogate Engine:** Applied for regions whose empirical residuals show non-Gaussian long-memory persistence or spectral anomalies that cause analytical ESS-MK to exceed the 6.5% FPR ceiling (NW, SW, SE).

2. **Hamed-Rao Rejection:**
   - Hamed-Rao modified Mann-Kendall exhibited empirical false positive rates of **13.5% to 24.8%** under the real satellite gap pattern and red noise null, severely violating the 6.5% upper limit.
   - Hamed-Rao is rejected as a primary significance test and retained solely as a secondary descriptive column.

3. **Zero Forbidden Phrases Verified:**
   - All report tables, narratives, and diffs strictly adhere to evidence-based terminology: non-significant trends are reported as `No detectable trend` or `below detection limit`, and causal claims are strictly avoided (using 'consistent with' rather than definitive causal claims).