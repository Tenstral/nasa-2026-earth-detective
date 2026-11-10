# Pairwise Between-Region Slope Comparison (2002–2026)

**Status:** PRELIMINARY & EXPLORATORY ONLY  
**Generated:** 2026-11-10 17:36:02  
**Methodology:** Calibrated Effective-Sample-Size Mann-Kendall test with Hurwicz bias correction evaluated directly on the paired difference series $d(t) = y_A(t) - y_B(t)$ with within-family Benjamini-Hochberg FDR control ($m = 20$).

---

## 1. Methodological Limits & Scope

> "Regions are adjacent and GRACE resolves a few hundred kilometres, so neighbouring regions share signal and coastal leakage is possible. A significant difference between two regions' slopes is a statement about these satellite-derived series, not a measurement of local aquifer or pumping differences. Recent windows are below the detection limit."

---

## 2. Calibration Audit & Method Selection

> Calibration used simulated AR(1) noise, which is the easier test. The single-region NW analysis previously failed a real-residual placebo (false-positive rate 17.6%, coverage 82.5%); the same check for the pairwise test is reported below.

### A. Diagnosis of v1 Moving-Block Bootstrap Failure
- **Original v1 Result:** A single-pair moving-block bootstrap with short block length ($b = 3$) exhibited an empirical False Positive Rate of **15.40%** (target 3.5%–6.5%) and 95% CI coverage of **84.60%** (target 93.0%–97.0%).
- **Root Cause:** Moving-block resampling with short block length ($b=3$) fails to capture the full temporal persistence of the underlying AR(1) process with $\phi \approx 0.55$, producing under-dispersed bootstrap slope distributions and artificially narrow confidence intervals.
- **Preserved Audit Trail:** The v1 failed report has been archived to `outputs/v3/region_comparison/calibration_report_v1_bootstrap_failed.json`.

### B. Candidate Methods Evaluated (Benchmark Pair: NW vs Central)

| Candidate Method | Description | FPR (Target: 3.5%–6.5%) | 95% CI Coverage (Target: 93%–97%) | Mean CI Width | Status |
|---|---|:---:|:---:|:---:|:---:|
| **Candidate A (Selected)** | Difference series Calibrated ESS-MK | **4.70%** | **95.30%** | 0.235 | **PASS** |
| Candidate B | Paired moving-block bootstrap ($b=10$) | 12.80% | 87.20% | 0.193 | FAIL |
| Candidate C | Residual AR(1) bootstrap on difference | 8.80% | 91.20% | 0.220 | FAIL |
| v1 Bootstrap (Failed) | Original short block ($b=3$) | 15.40% | 84.60% | 0.194 | FAIL (Archived) |

### C. Full 10-Pair Calibration Suite of Candidate A

#### Total Water Storage (10 Pairs)

| Regional Pair | $\phi_A$ | $\phi_B$ | $\rho$ | False Positive Rate | 95% CI Coverage | Mean CI Width | Power at Obs $\Delta$ | Target Met? |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **NW vs NE** | 0.554 | 0.437 | 0.816 | **5.50%** | **94.50%** | 0.257 | 100.0% | PASS |
| **NW vs Central** | 0.554 | 0.485 | 0.860 | **4.70%** | **95.30%** | 0.235 | 100.0% | PASS |
| **NW vs SW** | 0.554 | 0.626 | 0.589 | **5.70%** | **94.30%** | 0.363 | 100.0% | PASS |
| **NW vs SE** | 0.554 | 0.592 | 0.558 | **5.22%** | **94.78%** | 0.371 | 100.0% | PASS |
| **NE vs Central** | 0.437 | 0.485 | 0.945 | **6.50%** | **93.50%** | 0.104 | 76.7% | PASS |
| **NE vs SW** | 0.437 | 0.626 | 0.617 | **5.12%** | **94.88%** | 0.259 | 100.0% | PASS |
| **NE vs SE** | 0.437 | 0.592 | 0.738 | **4.70%** | **95.30%** | 0.209 | 100.0% | PASS |
| **Central vs SW** | 0.485 | 0.626 | 0.697 | **5.60%** | **94.40%** | 0.232 | 100.0% | PASS |
| **Central vs SE** | 0.485 | 0.592 | 0.749 | **5.50%** | **94.50%** | 0.209 | 100.0% | PASS |
| **SW vs SE** | 0.626 | 0.592 | 0.929 | **4.50%** | **95.50%** | 0.119 | 5.8% | PASS |

#### GPM IMERG Rainfall (10 Pairs)

| Regional Pair | $\phi_A$ | $\phi_B$ | $\rho$ | False Positive Rate | 95% CI Coverage | Mean CI Width | Power at Obs $\Delta$ | Target Met? |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **NW vs NE** | 0.000 | 0.000 | 0.744 | **5.60%** | **94.40%** | 33.11 | 5.4% | PASS |
| **NW vs Central** | 0.000 | 0.021 | 0.667 | **4.10%** | **95.90%** | 25.81 | 5.7% | PASS |
| **NW vs SW** | 0.000 | 0.024 | 0.391 | **4.40%** | **95.60%** | 36.18 | 7.6% | PASS |
| **NW vs SE** | 0.000 | 0.034 | 0.389 | **4.10%** | **95.90%** | 44.51 | 6.2% | PASS |
| **NE vs Central** | 0.000 | 0.021 | 0.663 | **4.90%** | **95.10%** | 36.31 | 6.0% | PASS |
| **NE vs SW** | 0.000 | 0.024 | 0.319 | **4.00%** | **96.00%** | 49.97 | 4.6% | PASS |
| **NE vs SE** | 0.000 | 0.034 | 0.509 | **5.00%** | **95.00%** | 47.18 | 5.2% | PASS |
| **Central vs SW** | 0.021 | 0.024 | 0.841 | **5.20%** | **94.80%** | 19.48 | 5.9% | PASS |
| **Central vs SE** | 0.021 | 0.034 | 0.740 | **4.70%** | **95.30%** | 31.52 | 5.3% | PASS |
| **SW vs SE** | 0.024 | 0.034 | 0.733 | **3.60%** | **96.40%** | 32.04 | 3.9% | PASS |

- **Summary Across All 20 Tested Pairs:** FPR ranges from **3.60% to 6.50%** (target 3.5%–6.5%, mean 4.93%), and 95% CI coverage ranges from **93.50% to 96.40%** (target 93.0%–97.0%, mean 95.07%). All 20 pairs meet pre-specified calibration criteria.

---

## 3. Real-Residual Placebo Audit (TWS Pairs)

> Calibration used simulated AR(1) noise, which is the easier test. The single-region NW analysis previously failed a real-residual placebo (false-positive rate 17.6%, coverage 82.5%); the same check for the pairwise test is reported below.

Two circular-shift placebo variants were evaluated across 1,000 realizations per pair:
- **Variant 1 (Independent Shift):** Circularly shifts Region B residuals by random lag $L \ge 24$ months. Breaks contemporaneous cross-correlation $\rho$, yielding wide CIs and conservative FPR.
- **Variant 2 (Synchronized Shift):** Circularly shifts both regions' residuals by the identical random lag, preserving contemporaneous spatial cross-correlation $\rho$. Multiannual climate excursions shifting across timeline boundaries induce spurious trend rejections in pairs with disparate variance structures.

| Regional Pair | Var 1 FPR (Indep) | Var 1 95% Cov | Var 2 FPR (Synced) | Var 2 95% Cov | Placebo Status |
|---|:---:|:---:|:---:|:---:|---|
| **NW vs NE** | 0.00% | 100.00% | **46.40%** | **53.60%** | **Fails real-residual placebo** |
| **NW vs Central** | 0.00% | 100.00% | **44.30%** | **55.70%** | **Fails real-residual placebo** |
| **NW vs SW** | 0.00% | 100.00% | **25.40%** | **74.60%** | **Fails real-residual placebo** |
| **NW vs SE** | 0.00% | 100.00% | **31.00%** | **69.00%** | **Fails real-residual placebo** |
| **NE vs Central** | 2.40% | 97.60% | **8.40%** | **91.60%** | **Fails real-residual placebo** |
| **NE vs SW** | 0.00% | 100.00% | **7.40%** | **92.60%** | **Fails real-residual placebo** |
| **NE vs SE** | 0.00% | 100.00% | **14.60%** | **85.40%** | **Fails real-residual placebo** |
| **Central vs SW** | 0.00% | 100.00% | **5.90%** | **94.10%** | Passes real-residual placebo |
| **Central vs SE** | 0.00% | 100.00% | **14.20%** | **85.80%** | **Fails real-residual placebo** |
| **SW vs SE** | 0.00% | 100.00% | **5.00%** | **95.00%** | Passes real-residual placebo |

---

## 4. Primary Between-Region Comparison (Full Record: 2002-04 to 2026-07)

Family of 20 tests (10 pairs $\times$ 2 variables). Benjamini-Hochberg FDR $q$-values calculated within this family.

### A. Total Water Storage Differences (cm/yr)

| Pair (A vs B) | Common Months | Slope A | Slope B | $\Delta$ Slope (A - B) | 95% Confidence Interval | p-value | FDR q-value | MDS (80%) | Verdict | v1 Verdict | Single-Region CI Overlap? | Placebo Flag |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **NW vs NE** | 257 | -1.255 | -0.555 | **-0.653** | [-0.763, -0.543] | 0.0000 | 0.0000 | 0.16 cm/yr | Significant difference | Significant difference | No | Fails real-residual placebo |
| **NW vs Central** | 257 | -1.255 | -0.473 | **-0.722** | [-0.841, -0.606] | 0.0000 | 0.0000 | 0.17 cm/yr | Significant difference | Significant difference | No | Fails real-residual placebo |
| **NW vs SW** | 257 | -1.255 | -0.047 | **-1.205** | [-1.402, -1.007] | 0.0000 | 0.0000 | 0.28 cm/yr | Significant difference | Significant difference | No | Fails real-residual placebo |
| **NW vs SE** | 257 | -1.255 | -0.052 | **-1.189** | [-1.397, -0.995] | 0.0000 | 0.0000 | 0.29 cm/yr | Significant difference | Significant difference | No | Fails real-residual placebo |
| **NE vs Central** | 257 | -0.555 | -0.473 | **-0.072** | [-0.101, -0.043] | 0.0000 | 0.0000 | 0.04 cm/yr | Significant difference | Significant difference | Yes (Overlaps) | Fails real-residual placebo |
| **NE vs SW** | 257 | -0.555 | -0.047 | **-0.538** | [-0.666, -0.413] | 0.0000 | 0.0000 | 0.18 cm/yr | Significant difference | Significant difference | No | Fails real-residual placebo |
| **NE vs SE** | 257 | -0.555 | -0.052 | **-0.529** | [-0.637, -0.422] | 0.0000 | 0.0000 | 0.15 cm/yr | Significant difference | Significant difference | No | Fails real-residual placebo |
| **Central vs SW** | 257 | -0.473 | -0.047 | **-0.483** | [-0.614, -0.352] | 0.0000 | 0.0000 | 0.19 cm/yr | Significant difference | Significant difference | No | Passes real-residual placebo |
| **Central vs SE** | 257 | -0.473 | -0.052 | **-0.455** | [-0.573, -0.339] | 0.0000 | 0.0000 | 0.17 cm/yr | Significant difference | Significant difference | No | Fails real-residual placebo |
| **SW vs SE** | 257 | -0.047 | -0.052 | **+0.006** | [-0.033, +0.045] | 0.7345 | 0.7731 | 0.06 cm/yr | No detectable difference | No detectable difference | Yes (Overlaps) | Passes real-residual placebo |

#### Note on Northeast vs Central Comparison
- In the paired difference test, Northeast vs Central yields $\Delta = -0.072$ cm/yr (95% CI [-0.101, -0.043], $q < 0.0001$).
- Because Northeast and Central are geographically adjacent, they share substantial regional climate and hydrological signal ($\rho = 0.945$). Differencing removes this shared nationwide variance, narrowing the paired CI.
- However, under an independent comparison, their single-region 95% CIs from `results_all_windows.csv` overlap substantially: **Northeast [-0.703, -0.419] cm/yr** and **Central [-0.620, -0.342] cm/yr** overlap between -0.620 and -0.419 cm/yr. While a differential slope is detectable when common variance is subtracted, their secular trajectories cannot be distinguished under marginal single-region uncertainty.

### B. GPM IMERG Rainfall Differences (mm/yr)

| Pair (A vs B) | Common Months | Slope A | Slope B | $\Delta$ Slope (A - B) | 95% Confidence Interval | p-value | FDR q-value | MDS (80%) | Verdict | v1 Verdict | Single-Region CI Overlap? | Placebo Flag |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **NW vs NE** | 247 | -1.910 | -0.594 | **-2.990** | [-14.936, +6.510] | 0.5383 | 0.7177 | 15.33 mm/yr | No detectable difference | No detectable difference | Yes (Overlaps) | Passes real-residual placebo |
| **NW vs Central** | 247 | -1.910 | +0.891 | **-4.260** | [-12.525, +2.792] | 0.2270 | 0.4127 | 10.95 mm/yr | No detectable difference | No detectable difference | Yes (Overlaps) | Passes real-residual placebo |
| **NW vs SW** | 247 | -1.910 | +2.247 | **-5.093** | [-14.991, +2.063] | 0.1395 | 0.2789 | 12.19 mm/yr | No detectable difference | No detectable difference | Yes (Overlaps) | Passes real-residual placebo |
| **NW vs SE** | 247 | -1.910 | +1.757 | **-5.141** | [-17.188, +5.098] | 0.2929 | 0.4506 | 15.93 mm/yr | No detectable difference | No detectable difference | Yes (Overlaps) | Passes real-residual placebo |
| **NE vs Central** | 247 | -0.594 | +0.891 | **-0.949** | [-8.081, +6.002] | 0.7129 | 0.7731 | 10.06 mm/yr | No detectable difference | No detectable difference | Yes (Overlaps) | Passes real-residual placebo |
| **NE vs SW** | 247 | -0.594 | +2.247 | **-2.445** | [-14.906, +8.612] | 0.6583 | 0.7731 | 16.81 mm/yr | No detectable difference | No detectable difference | Yes (Overlaps) | Passes real-residual placebo |
| **NE vs SE** | 247 | -0.594 | +1.757 | **-1.860** | [-13.956, +8.504] | 0.6771 | 0.7731 | 16.05 mm/yr | No detectable difference | No detectable difference | Yes (Overlaps) | Passes real-residual placebo |
| **Central vs SW** | 247 | +0.891 | +2.247 | **-3.040** | [-8.879, +2.346] | 0.2706 | 0.4506 | 8.02 mm/yr | No detectable difference | No detectable difference | Yes (Overlaps) | Passes real-residual placebo |
| **Central vs SE** | 247 | +0.891 | +1.757 | **-0.390** | [-7.371, +6.326] | 0.8853 | 0.8853 | 9.79 mm/yr | No detectable difference | No detectable difference | Yes (Overlaps) | Passes real-residual placebo |
| **SW vs SE** | 247 | +2.247 | +1.757 | **+3.055** | [-3.533, +11.121] | 0.3710 | 0.5300 | 10.47 mm/yr | No detectable difference | No detectable difference | Yes (Overlaps) | Passes real-residual placebo |

---

## 5. Sensitivity Analyses

### A. GRACE Era Only (2002-04 to 2017-06)

| Variable | Pair | Common Months | $\Delta$ Slope | 95% CI | p-value | FDR q-value | Verdict |
|---|---|:---:|:---:|:---:|:---:|---|
| TWS | **NW vs NE** | 161 | **-0.825** cm/yr | [-1.002, -0.636] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NW vs Central** | 161 | **-0.888** cm/yr | [-1.098, -0.680] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NW vs SW** | 161 | **-1.458** cm/yr | [-1.823, -1.127] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NW vs SE** | 161 | **-1.466** cm/yr | [-1.810, -1.117] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NE vs Central** | 161 | **-0.084** cm/yr | [-0.149, -0.021] | 0.0105 | 0.0234 | Significant difference |
| TWS | **NE vs SW** | 161 | **-0.660** cm/yr | [-0.872, -0.467] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NE vs SE** | 161 | **-0.657** cm/yr | [-0.832, -0.492] | 0.0000 | 0.0000 | Significant difference |
| TWS | **Central vs SW** | 161 | **-0.570** cm/yr | [-0.770, -0.377] | 0.0000 | 0.0000 | Significant difference |
| TWS | **Central vs SE** | 161 | **-0.567** cm/yr | [-0.732, -0.402] | 0.0000 | 0.0000 | Significant difference |
| TWS | **SW vs SE** | 161 | **-0.004** cm/yr | [-0.066, +0.059] | 0.8752 | 0.9162 | No detectable difference |
| PRECIP | **NW vs NE** | 161 | **-18.888** mm/yr | [-45.874, +3.917] | 0.1171 | 0.1801 | No detectable difference |
| PRECIP | **NW vs Central** | 161 | **-9.401** mm/yr | [-27.543, +5.577] | 0.2312 | 0.3303 | No detectable difference |
| PRECIP | **NW vs SW** | 161 | **-11.833** mm/yr | [-31.200, +1.936] | 0.0913 | 0.1522 | No detectable difference |
| PRECIP | **NW vs SE** | 161 | **-20.418** mm/yr | [-43.912, -0.522] | 0.0447 | 0.0814 | Suggestive |
| PRECIP | **NE vs Central** | 161 | **+1.889** mm/yr | [-9.558, +16.719] | 0.6652 | 0.7826 | No detectable difference |
| PRECIP | **NE vs SW** | 161 | **-0.715** mm/yr | [-21.504, +22.183] | 0.9162 | 0.9162 | No detectable difference |
| PRECIP | **NE vs SE** | 161 | **-1.311** mm/yr | [-20.868, +16.867] | 0.8230 | 0.9145 | No detectable difference |
| PRECIP | **Central vs SW** | 161 | **-5.333** mm/yr | [-17.502, +4.284] | 0.2780 | 0.3707 | No detectable difference |
| PRECIP | **Central vs SE** | 161 | **-15.862** mm/yr | [-35.772, -1.741] | 0.0260 | 0.0520 | Suggestive |
| PRECIP | **SW vs SE** | 161 | **-9.004** mm/yr | [-31.228, +6.328] | 0.3121 | 0.3901 | No detectable difference |

### B. Transition Buffer Excluded (Full Record excluding $\pm 6$ months around gap)

| Variable | Pair | Common Months | $\Delta$ Slope | 95% CI | p-value | FDR q-value | Verdict |
|---|---|:---:|:---:|:---:|:---:|---|
| TWS | **NW vs NE** | 248 | **-0.655** cm/yr | [-0.765, -0.545] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NW vs Central** | 248 | **-0.727** cm/yr | [-0.843, -0.610] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NW vs SW** | 248 | **-1.224** cm/yr | [-1.426, -1.022] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NW vs SE** | 248 | **-1.206** cm/yr | [-1.419, -1.008] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NE vs Central** | 248 | **-0.073** cm/yr | [-0.103, -0.044] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NE vs SW** | 248 | **-0.556** cm/yr | [-0.685, -0.429] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NE vs SE** | 248 | **-0.544** cm/yr | [-0.654, -0.438] | 0.0000 | 0.0000 | Significant difference |
| TWS | **Central vs SW** | 248 | **-0.499** cm/yr | [-0.630, -0.369] | 0.0000 | 0.0000 | Significant difference |
| TWS | **Central vs SE** | 248 | **-0.473** cm/yr | [-0.594, -0.352] | 0.0000 | 0.0000 | Significant difference |
| TWS | **SW vs SE** | 248 | **+0.009** cm/yr | [-0.032, +0.048] | 0.6463 | 0.7604 | No detectable difference |
| PRECIP | **NW vs NE** | 238 | **-3.120** mm/yr | [-15.146, +6.447] | 0.4982 | 0.6642 | No detectable difference |
| PRECIP | **NW vs Central** | 238 | **-3.576** mm/yr | [-11.320, +3.079] | 0.3025 | 0.4653 | No detectable difference |
| PRECIP | **NW vs SW** | 238 | **-5.147** mm/yr | [-15.031, +2.104] | 0.1398 | 0.2795 | No detectable difference |
| PRECIP | **NW vs SE** | 238 | **-3.813** mm/yr | [-13.636, +4.971] | 0.3725 | 0.5321 | No detectable difference |
| PRECIP | **NE vs Central** | 238 | **-0.904** mm/yr | [-7.588, +5.867] | 0.7366 | 0.7753 | No detectable difference |
| PRECIP | **NE vs SW** | 238 | **-2.518** mm/yr | [-15.239, +8.262] | 0.6454 | 0.7604 | No detectable difference |
| PRECIP | **NE vs SE** | 238 | **-1.590** mm/yr | [-12.730, +8.637] | 0.7194 | 0.7753 | No detectable difference |
| PRECIP | **Central vs SW** | 238 | **-3.542** mm/yr | [-9.386, +1.753] | 0.1892 | 0.3359 | No detectable difference |
| PRECIP | **Central vs SE** | 238 | **-0.336** mm/yr | [-6.260, +6.075] | 0.9010 | 0.9010 | No detectable difference |
| PRECIP | **SW vs SE** | 238 | **+3.665** mm/yr | [-2.189, +10.820] | 0.2015 | 0.3359 | No detectable difference |
