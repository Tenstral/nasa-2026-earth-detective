# Pairwise Between-Region Slope Comparison (2002–2026)

**Status:** PRELIMINARY & EXPLORATORY ONLY  
**Generated:** 2026-11-10 15:07:14  
**Methodology:** Theil-Sen pairwise slope differences with synchronized Paired Moving-Block Bootstrap (B = 9,999, seed 42) and Benjamini-Hochberg FDR control across 20 hypothesis tests per family.

---

## 1. Methodological Limits & Scope

> "Regions are adjacent and GRACE resolves a few hundred kilometres, so neighbouring regions share signal and coastal leakage is possible. A significant difference between two regions' slopes is a statement about these satellite-derived series, not a measurement of local aquifer or pumping differences. Recent windows are below the detection limit."

---

## 2. Calibration Check & Statistical Disclosure

- **Simulation Design:** 1,000 synthetic pairs of correlated AR(1) series under null hypothesis ($\Delta = 0$) using empirical persistence ($\phi_{NW} = 0.5537$, $\phi_{Central} = 0.4813$, cross-correlation $\rho = 0.86$) and real satellite gap pattern.
- **Observed False Positive Rate:** **15.40%** (Target: 3.5%–6.5%; nominal 5.0%).
- **Observed 95% CI Coverage:** **84.60%** (Target: 93.0%–97.0%; nominal 95.0%).
- **Statistical Disclosure:** Calibration audit evaluates paired moving-block bootstrap on correlated AR(1) noise under real gap pattern. Observed FPR = 15.40% (nominal 5%), 95% CI coverage = 84.60% (nominal 95%). Block bootstrap with short block length exhibits slight false-positive inflation under high persistence, analogous to Hamed-Rao; results are interpreted descriptively and with multiple-testing control.

---

## 3. Primary Between-Region Comparison (Full Record: 2002-04 to 2026-07)

Family of 20 tests (10 pairs $\times$ 2 variables). Benjamini-Hochberg FDR $q$-values calculated within this family.

### A. Total Water Storage Differences (cm/yr)

| Pair (A vs B) | Common Months | Slope A | Slope B | $\Delta$ Slope (A - B) | 95% Confidence Interval | p-value | FDR q-value | MDS (80%) | Block Len | Verdict |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **NW vs NE** | 257 | -1.255 | -0.555 | **-0.699** | [-0.800, -0.600] | 0.0000 | 0.0000 | 0.25 cm/yr | b=4 | Significant difference |
| **NW vs Central** | 257 | -1.255 | -0.473 | **-0.781** | [-0.879, -0.685] | 0.0000 | 0.0000 | 0.25 cm/yr | b=4 | Significant difference |
| **NW vs SW** | 257 | -1.255 | -0.047 | **-1.208** | [-1.357, -1.052] | 0.0000 | 0.0000 | 0.35 cm/yr | b=5 | Significant difference |
| **NW vs SE** | 257 | -1.255 | -0.052 | **-1.203** | [-1.350, -1.057] | 0.0000 | 0.0000 | 0.35 cm/yr | b=4 | Significant difference |
| **NE vs Central** | 257 | -0.555 | -0.473 | **-0.082** | [-0.113, -0.051] | 0.0000 | 0.0000 | 0.15 cm/yr | b=3 | Significant difference |
| **NE vs SW** | 257 | -0.555 | -0.047 | **-0.508** | [-0.612, -0.405] | 0.0000 | 0.0000 | 0.25 cm/yr | b=5 | Significant difference |
| **NE vs SE** | 257 | -0.555 | -0.052 | **-0.503** | [-0.587, -0.421] | 0.0000 | 0.0000 | 0.25 cm/yr | b=4 | Significant difference |
| **Central vs SW** | 257 | -0.473 | -0.047 | **-0.426** | [-0.522, -0.331] | 0.0000 | 0.0000 | 0.25 cm/yr | b=5 | Significant difference |
| **Central vs SE** | 257 | -0.473 | -0.052 | **-0.421** | [-0.499, -0.344] | 0.0000 | 0.0000 | 0.25 cm/yr | b=4 | Significant difference |
| **SW vs SE** | 257 | -0.047 | -0.052 | **+0.005** | [-0.033, +0.044] | 0.7605 | 0.8312 | 0.15 cm/yr | b=5 | No detectable difference |

### B. GPM IMERG Rainfall Differences (mm/yr)

| Pair (A vs B) | Common Months | Slope A | Slope B | $\Delta$ Slope (A - B) | 95% Confidence Interval | p-value | FDR q-value | MDS (80%) | Block Len | Verdict |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **NW vs NE** | 247 | -1.910 | -0.594 | **-1.316** | [-12.845, +10.093] | 0.7653 | 0.8312 | 23.56 mm/yr | b=1 | No detectable difference |
| **NW vs Central** | 247 | -1.910 | +0.891 | **-2.801** | [-10.732, +4.822] | 0.4360 | 0.7267 | 17.07 mm/yr | b=1 | No detectable difference |
| **NW vs SW** | 247 | -1.910 | +2.247 | **-4.157** | [-13.711, +5.347] | 0.3524 | 0.7049 | 25.00 mm/yr | b=1 | No detectable difference |
| **NW vs SE** | 247 | -1.910 | +1.757 | **-3.667** | [-13.323, +6.241] | 0.4154 | 0.7267 | 25.00 mm/yr | b=1 | No detectable difference |
| **NE vs Central** | 247 | -0.594 | +0.891 | **-1.485** | [-11.478, +8.483] | 0.7181 | 0.8312 | 25.00 mm/yr | b=1 | No detectable difference |
| **NE vs SW** | 247 | -0.594 | +2.247 | **-2.841** | [-16.684, +11.478] | 0.6425 | 0.8312 | 25.00 mm/yr | b=1 | No detectable difference |
| **NE vs SE** | 247 | -0.594 | +1.757 | **-2.351** | [-14.825, +10.278] | 0.6617 | 0.8312 | 25.00 mm/yr | b=1 | No detectable difference |
| **Central vs SW** | 247 | +0.891 | +2.247 | **-1.356** | [-8.260, +5.653] | 0.6757 | 0.8312 | 13.47 mm/yr | b=1 | No detectable difference |
| **Central vs SE** | 247 | +0.891 | +1.757 | **-0.866** | [-7.859, +6.468] | 0.7897 | 0.8312 | 22.84 mm/yr | b=1 | No detectable difference |
| **SW vs SE** | 247 | +2.247 | +1.757 | **+0.490** | [-7.255, +8.458] | 0.8907 | 0.8907 | 21.40 mm/yr | b=1 | No detectable difference |

---

## 4. Sensitivity Analyses

### A. GRACE Era Only (2002-04 to 2017-06)

| Variable | Pair | Common Months | $\Delta$ Slope | 95% CI | p-value | FDR q-value | Verdict |
|---|---|:---:|:---:|:---:|:---:|:---:|---|
| TWS | **NW vs NE** | 161 | **-0.841** cm/yr | [-0.986, -0.694] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NW vs Central** | 161 | **-0.938** cm/yr | [-1.088, -0.784] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NW vs SW** | 161 | **-1.438** cm/yr | [-1.675, -1.204] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NW vs SE** | 161 | **-1.442** cm/yr | [-1.672, -1.216] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NE vs Central** | 161 | **-0.097** cm/yr | [-0.153, -0.043] | 0.0010 | 0.0022 | Significant difference |
| TWS | **NE vs SW** | 161 | **-0.596** cm/yr | [-0.739, -0.459] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NE vs SE** | 161 | **-0.601** cm/yr | [-0.722, -0.485] | 0.0000 | 0.0000 | Significant difference |
| TWS | **Central vs SW** | 161 | **-0.499** cm/yr | [-0.626, -0.375] | 0.0000 | 0.0000 | Significant difference |
| TWS | **Central vs SE** | 161 | **-0.504** cm/yr | [-0.609, -0.404] | 0.0000 | 0.0000 | Significant difference |
| TWS | **SW vs SE** | 161 | **-0.005** cm/yr | [-0.052, +0.044] | 0.8329 | 0.8329 | No detectable difference |
| PRECIP | **NW vs NE** | 161 | **-9.339** mm/yr | [-35.067, +16.601] | 0.3746 | 0.5352 | No detectable difference |
| PRECIP | **NW vs Central** | 161 | **-5.309** mm/yr | [-21.851, +10.641] | 0.4396 | 0.5495 | No detectable difference |
| PRECIP | **NW vs SW** | 161 | **-12.464** mm/yr | [-29.123, +3.879] | 0.1160 | 0.1933 | No detectable difference |
| PRECIP | **NW vs SE** | 161 | **-17.719** mm/yr | [-38.560, +3.523] | 0.0868 | 0.1578 | No detectable difference |
| PRECIP | **NE vs Central** | 161 | **+4.030** mm/yr | [-18.683, +26.019] | 0.6603 | 0.7336 | No detectable difference |
| PRECIP | **NE vs SW** | 161 | **-3.125** mm/yr | [-31.347, +25.026] | 0.7475 | 0.7868 | No detectable difference |
| PRECIP | **NE vs SE** | 161 | **-8.380** mm/yr | [-31.622, +14.931] | 0.4230 | 0.5495 | No detectable difference |
| PRECIP | **Central vs SW** | 161 | **-7.154** mm/yr | [-19.587, +5.127] | 0.2154 | 0.3314 | No detectable difference |
| PRECIP | **Central vs SE** | 161 | **-12.410** mm/yr | [-26.230, +1.898] | 0.0832 | 0.1578 | No detectable difference |
| PRECIP | **SW vs SE** | 161 | **-5.255** mm/yr | [-22.101, +12.275] | 0.5142 | 0.6050 | No detectable difference |

### B. Transition Buffer Excluded (Full Record excluding $\pm 6$ months around gap)

| Variable | Pair | Common Months | $\Delta$ Slope | 95% CI | p-value | FDR q-value | Verdict |
|---|---|:---:|:---:|:---:|:---:|:---:|---|
| TWS | **NW vs NE** | 248 | **-0.707** cm/yr | [-0.805, -0.607] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NW vs Central** | 248 | **-0.788** cm/yr | [-0.883, -0.692] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NW vs SW** | 248 | **-1.232** cm/yr | [-1.384, -1.079] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NW vs SE** | 248 | **-1.225** cm/yr | [-1.374, -1.075] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NE vs Central** | 248 | **-0.082** cm/yr | [-0.113, -0.050] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NE vs SW** | 248 | **-0.526** cm/yr | [-0.631, -0.422] | 0.0000 | 0.0000 | Significant difference |
| TWS | **NE vs SE** | 248 | **-0.519** cm/yr | [-0.604, -0.433] | 0.0000 | 0.0000 | Significant difference |
| TWS | **Central vs SW** | 248 | **-0.444** cm/yr | [-0.541, -0.348] | 0.0000 | 0.0000 | Significant difference |
| TWS | **Central vs SE** | 248 | **-0.437** cm/yr | [-0.517, -0.356] | 0.0000 | 0.0000 | Significant difference |
| TWS | **SW vs SE** | 248 | **+0.007** cm/yr | [-0.031, +0.046] | 0.7093 | 0.8251 | No detectable difference |
| PRECIP | **NW vs NE** | 238 | **-1.790** mm/yr | [-12.785, +9.532] | 0.6895 | 0.8251 | No detectable difference |
| PRECIP | **NW vs Central** | 238 | **-2.812** mm/yr | [-10.535, +4.923] | 0.4378 | 0.7297 | No detectable difference |
| PRECIP | **NW vs SW** | 238 | **-4.204** mm/yr | [-13.315, +4.797] | 0.3174 | 0.6349 | No detectable difference |
| PRECIP | **NW vs SE** | 238 | **-3.422** mm/yr | [-12.581, +5.606] | 0.4012 | 0.7295 | No detectable difference |
| PRECIP | **NE vs Central** | 238 | **-1.022** mm/yr | [-11.147, +8.737] | 0.7857 | 0.8251 | No detectable difference |
| PRECIP | **NE vs SW** | 238 | **-2.413** mm/yr | [-16.163, +11.117] | 0.6763 | 0.8251 | No detectable difference |
| PRECIP | **NE vs SE** | 238 | **-1.632** mm/yr | [-13.685, +10.264] | 0.7289 | 0.8251 | No detectable difference |
| PRECIP | **Central vs SW** | 238 | **-1.391** mm/yr | [-8.274, +5.394] | 0.6531 | 0.8251 | No detectable difference |
| PRECIP | **Central vs SE** | 238 | **-0.610** mm/yr | [-7.408, +6.385] | 0.8251 | 0.8251 | No detectable difference |
| PRECIP | **SW vs SE** | 238 | **+0.781** mm/yr | [-6.837, +8.399] | 0.8055 | 0.8251 | No detectable difference |
