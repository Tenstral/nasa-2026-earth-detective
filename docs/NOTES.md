# Bengal Hydro Detective — Project Notes, Decisions & Audit Log

**NASA Space Apps Challenge 2026 — Be an Earth System Trend Detective!**  
**Team:** Tenstral  
**Status:** PRELIMINARY — Subject to Peer Review and In-Situ Hydrometric Validation  
**Last Updated:** November 2026  

---

## 1. Fixed Decisions and Scope Parameters

1. **Analytical Windows:**
   - `full_record`: April 2002 to July 2026 (292 operational calendar months, 257 observed GRACE/GRACE-FO months). **PRIMARY** analytical window.
   - `grace_era`: April 2002 to June 2017 (183 calendar months, 161 observed months). Transition-free historical baseline.
   - `grace_fo_era`: June 2018 to July 2026 (98 calendar months, 96 observed months). Single-satellite instrument era.
   - `recent_2020`: January 2020 to July 2026 (79 calendar months, 79 observed months). Sensitivity and legacy v2 comparison only.

2. **Regional Spatial Units:**
   - 5 geographic regions: Northwest (NW: Rajshahi, Rangpur), Northeast (NE: Sylhet, Mymensingh), Central (Dhaka), Southwest (SW: Khulna, Barishal), Southeast (SE: Chattogram), and National composite (all 8 divisions).
   - Division-level trends are presented for descriptive and spatial context only; statistical hypothesis testing and headline claims are made strictly at the 5-region and National scale.

3. **Statistical Significance and Verdict Rule:**
   - Primary Significance Test: Calibrated Effective Sample Size Mann-Kendall (ESS-MK) with Hurwicz small-sample bias correction for AR(1) autocorrelation and duality-aligned Theil-Sen rank confidence intervals.
   - Multiple Testing Control: Benjamini-Hochberg False Discovery Rate (BH-FDR) applied independently within each analytical window family ($q < 0.05$).
   - Verdict Categories:
     * `Significant decrease` / `Significant increase`: Within-window FDR $q < 0.05$ AND 95% confidence interval excludes zero.
     * `Suggestive decrease` / `Suggestive increase`: Raw $p < 0.05$ only.
     * `No detectable trend`: Raw $p \ge 0.05$ OR CI includes zero.
     * `method-dependent`: Assigned when statistical verdict depends on the test choice or when raw $p < 0.05$ but FDR $q \ge 0.05$ (e.g., NW in `recent_2020`).

4. **Primary Rainfall Record:**
   - NASA GPM IMERG Final Run V07B (`GPM_3IMERGM` monthly and `GPM_3IMERGDF` daily) is the designated PRIMARY precipitation dataset.
   - NASA POWER is retained for sensitivity only due to a verified non-climatic step increase (+45% to +84%) occurring between 2014-12 and 2015-12 (Pettitt $p < 0.0001$).
   - **Data Span Notice:** GPM IMERG Final V07B currently extends through September 2025. Consequently, the final 10 months of `full_record` (2025-10 to 2026-07) and `grace_fo_era` are truncated in precipitation comparisons.

5. **Mandatory Scientific Terminology:**
   - Gravimetry observations report vertically integrated **"Total Water Storage" (TWS)**.
   - The term "groundwater" is never used for total water storage and is strictly reserved for the explicitly labeled residual: `"groundwater + surface water + model error residual"`.
   - Causal relationships are phrased as **"consistent with"**, never "caused by" or causal proof assertions.
   - All findings and deliverables are labeled **PRELIMINARY**.

---

## 2. Review Audit Log & Changes in Headline Numbers

### Review Finding 1: Significance Method Consistency & Calibration
- **Problem:** The previous calibration report showed false-positive rates of 15%–19% with Hamed-Rao, yet called it passed. Furthermore, the NW surrogate test reported identical $p = 0.0005$ across multiple windows due to surrogate sample size floors ($N=2,000$), and the placebo test was circular.
- **Action Taken:**
  1. Implemented independent Monte Carlo null simulation (2,000 runs) generating synthetic AR(1) processes fitted to real regional residuals with the exact 257-month GRACE observation mask.
  2. Verified that Calibrated ESS-MK strictly satisfies pass criteria for ALL 6 regions (FPR 4.10%–5.45% $\in [3.5\%, 6.5\%]$; 95% CI coverage 94.55%–95.95% $\in [93.0\%, 97.0\%]$), whereas Hamed-Rao fails (FPR 13%–17%).
  3. Standardized Calibrated ESS-MK as the single primary significance test across all regions and windows.
  4. Expanded Fourier surrogate evaluation to $N \ge 10,000$ iterations (batched in 500-sample blocks) and reported floor values as `"< 0.0001"`.
  5. In `recent_2020`, NW TWS has raw $p = 0.0107$, but within-window FDR $q = 0.0772 > 0.05$; it was reclassified from "Significant" to `"method-dependent"`.
  6. In `grace_fo_era`, NW TWS has raw $p = 0.0549$ and CI $[-3.32, +0.06]$ cm/yr (includes zero); classified as `No detectable trend` under the primary calibrated test (nominal surrogate was Suggestive).

### Review Finding 2: Extreme Precipitation Scaling & CI-p Consistency
- **Problem:** NW annual total slope was reported as $-80.4\text{ mm/yr}$ and monsoon total as $-94.0\text{ mm/yr}$, which was physically implausible (multiplied by 12 due to calling monthly trend functions with annual data). Confidence intervals in several rows excluded zero despite $p > 0.05$ due to mixing bootstrap CI with Hamed-Rao p-values.
- **Action Taken:**
  1. Replaced calls to `v2.task3_trend_engine.run_trend` with `v3.trend_engine.run_ess_mann_kendall`. Removed spurious x12 multipliers.
  2. Fixed slope scaling: NW annual total slope is $-6.70\text{ mm/yr}$ [$-29.49, +10.33$], $p = 0.576$; NW monsoon total slope is $-7.83\text{ mm/yr}$ [$-21.29, +3.43$], $p = 0.097$; National Rx1day slope is $+0.82\text{ mm/yr}$ [$-0.20, +1.68$], $p = 0.135$.
  3. Enforced mathematical duality: every 95% CI strictly includes zero if and only if $p \ge 0.05$.
  4. Documented spatial aggregation protocol: 0.1° grid cells are area-weighted by $\cos(\text{latitude})$ to division means, then aggregated to regional means using administrative land areas (`DIV_AREAS`), and extreme indices are calculated directly on the regional daily time series.
  5. Hand cross-checked daily vs monthly totals for sample years 2010 and 2020, documenting the standard satellite algorithm difference (NW 2010: daily sum 2010.0 mm vs monthly sum 1732.8 mm, +16.0%, reflecting daily GPM_3IMERGDF gauge weighting vs monthly GPM_3IMERGM GPCC calibration).

### Review Finding 3: GLDAS Multi-Model Partitioning & Homogeneity Testing
- **Problem:** Noah 2.1, VIC 2.1, and CLSM 2.2 were averaged as equal lines of evidence despite CLSM 2.2 assimilating GRACE data (circular). Residual storage was reported with a pooled CI mixing physical and model spread. Pettitt change-point test was interpreted as data inhomogeneity, whereas Pettitt mathematically rejects the null and places a break near $t \approx N/2$ in the presence of any secular trend.
- **Action Taken:**
  1. Separated independent open-loop models (Noah 2.1 and VIC 2.1) from data-assimilating CLSM 2.2. Prominently noted that CLSM 2.2 cannot serve as an independent partition of GRACE.
  2. Reported independent soil moisture and residual storage as a model range $[\min, \max]$ rather than a single pooled number with a confidence interval.
  3. NW independent soil moisture slope range in `grace_fo_era`: $[+0.05, +0.20]\text{ cm/yr}$; independent residual storage slope range: $[-1.92, -1.70]\text{ cm/yr}$.
  4. Added prominent guidance note to homogeneity reports explaining that Pettitt test rejection under a secular trend does not imply data or instrumentation inhomogeneity.
  5. Updated wording to: *"most of the decline is not accounted for by simulated soil moisture; groundwater and surface water cannot be separated here"*.

### Review Finding 4: Literature Benchmark Table & Narrative Synchronization
- **Problem:** Outdated p-values and CIs in `novelty_statement.md`; unearned claims of refuted rainfall trends and unsubstantiated links to Boro irrigation without well data; PUB-01 unit conversion lacked basis; PUB-02 NW Purdy estimate ($-1.99\text{ cm/yr}$) was not noted as lying outside our NW CI.
- **Action Taken:**
  1. Dynamically regenerated `novelty_statement.md` directly from `results_all_windows.csv`.
  2. Replaced refuted claim with: *"we detected an artifact in NASA POWER rainfall by cross-checking with IMERG; cause not established"*.
  3. Removed assertion linking Ahmed and Purdy on Boro irrigation.
  4. Left PUB-01 converted rate blank because the source text does not state the bounding area.
  5. Noted that Purdy's NW estimate of $-1.99\text{ cm/yr}$ lies outside our NW grace_era 95% CI ($-1.95$ to $-1.15\text{ cm/yr}$): *"similar sign and order of magnitude; ours is lower; region definitions may differ"*.
  6. All studies with `Comparable: No` are labeled `"Context only"`.
  7. Extended `test_forbidden_phrases.py` with 13 banned patterns, scanning all documentation and reports under `outputs/` and `README.md`, with zero violations.

---

## 3. Master Headline Numbers Reference Table

| Region | Window | TWS Rate [95% CI] (cm/yr) | Volumetric Rate (km³/yr) | Raw p-value | BH-FDR q-value | Calibrated Verdict |
|---|---|:---:|:---:|:---:|:---:|---|
| **NW** | `full_record` | **-1.25 [-1.50, -1.02]** | -0.39 | < 0.0001 | < 0.0001 | **Significant decrease** |
| **NW** | `grace_era` | **-1.56 [-1.96, -1.17]** | -0.48 | < 0.0001 | < 0.0001 | **Significant decrease** |
| **NW** | `grace_fo_era` | -1.67 [-3.32, +0.06] | -0.52 | 0.0549 | 0.4626 | No detectable trend (CI includes zero) |
| **NW** | `recent_2020` | -2.93 [-4.97, -0.78] | -0.91 | 0.0107 | 0.0772 | Method-dependent (fails within-window FDR) |
| **NE** | `full_record` | **-0.56 [-0.70, -0.42]** | -0.12 | < 0.0001 | < 0.0001 | **Significant decrease** |
| **Central** | `full_record` | **-0.47 [-0.62, -0.34]** | -0.08 | < 0.0001 | < 0.0001 | **Significant decrease** |
| **SW** | `full_record` | -0.05 [-0.20, +0.10] | -0.01 | 0.5459 | 0.8968 | No detectable trend |
| **SE** | `full_record` | -0.05 [-0.17, +0.06] | -0.01 | 0.3754 | 0.8968 | No detectable trend |
| **National** | `full_record` | **-0.51 [-0.66, -0.38]** | **-0.63** | < 0.0001 | < 0.0001 | **Significant decrease** |
| **National** | `grace_era` | **-0.68 [-0.92, -0.45]** | **-0.83** | < 0.0001 | < 0.0001 | **Significant decrease** |
| **National** | `grace_fo_era` | -0.47 [-1.50, +0.53] | -0.58 | 0.3111 | 0.7057 | No detectable trend |
| **National** | `recent_2020` | -1.02 [-2.53, +0.51] | -1.24 | 0.1721 | 0.6884 | No detectable trend |

*Note: In `full_record`, 3 of 5 regions (NW, NE, Central) and the National composite exhibit statistically significant storage depletion under within-window BH-FDR ($q < 0.05$), while Southern regions (SW, SE) exhibit no detectable multi-decadal trend.*

---

## Consistency Fixes & Statistical Reconciliation (Audit Trail)

All numbers updated on branch `fixes-review` were derived programmatically from the single sources of truth (`outputs/v3/full_record/results_all_windows.csv` and `outputs/v3/full_record/gap_calibration_report.json`):

| Metric / Parameter | Location / Context | Old Value | New Value | Source of Truth / Justification |
|---|---|:---:|:---:|---|
| **NW full_record TWS 95% CI** | `exposure_table.csv`, `.md`, `NOTES.md` | `[-1.54, -0.96]` | **`[-1.50, -1.02]`** | Primary duality-aligned rank CI from `results_all_windows.csv` (`slope_ci_low`, `slope_ci_high`), replacing surrogate CI columns. |
| **SW full_record TWS 95% CI** | `exposure_table.csv`, `.md`, `NOTES.md` | `[-0.17, +0.08]` | **`[-0.20, +0.10]`** | Primary duality-aligned rank CI from `results_all_windows.csv` (`slope_ci_low`, `slope_ci_high`), replacing surrogate CI columns. |
| **NW full_record TWS FDR q-value** | `exposure_table.csv`, `.md` | `< 0.0001` or `0.0015` | **`< 0.0001`** | Direct within-window Benjamini-Hochberg FDR $q$-value from `results_all_windows.csv` ($q = 0.000078$). |
| **NW recent_2020 TWS 95% CI** | `README.md`, `NOTES.md` | `[-4.90, -0.57]` | **`[-4.97, -0.78]`** | Exact duality-aligned CI from `results_all_windows.csv` for 2020–2026 sensitivity window. |
| **National recent_2020 TWS 95% CI** | `README.md`, `NOTES.md` | `[-3.05, +0.94]` | **`[-2.53, +0.51]`** | Exact duality-aligned CI from `results_all_windows.csv` for 2020–2026 sensitivity window. |
| **National full_record TWS 95% CI** | `README.md` | `[-0.67, -0.35]` | **`[-0.66, -0.38]`** | Primary duality-aligned CI from `results_all_windows.csv` for full 24-year record. |
| **Depletion Corridor Exposed Population** | `PROJECT_STATUS.md`, `FIXES_REVIEW_REPORT.md`, `index.html`, `exposure_table.md` | `69.4 million` (40.9%) | **`108.5 million` (63.9%)** | Programmatic sum of NW (38.81M) + NE (24.05M) + Central (45.64M) from NASA SEDAC GPWv4 in `exposure_table.csv`. Old 69.4M unverified artifact deleted. |
| **Calibrated ESS-MK NW FPR** | `PROJECT_STATUS.md`, `FIXES_REVIEW_REPORT.md`, `index.html` | `4.60%` | **`4.10%`** | `gap_calibration_report.json` (`calibration_simulation.regional_ar1_null.NW.fpr_ess_mk` = 0.041). |
| **Calibrated ESS-MK NW CI Coverage** | `PROJECT_STATUS.md`, `FIXES_REVIEW_REPORT.md`, `index.html` | `95.40%` | **`95.90%`** | `gap_calibration_report.json` (`calibration_simulation.regional_ar1_null.NW.coverage_ess_mk` = 0.959). |
| **IMERG Satellite Observation Period** | `PROJECT_STATUS.md` | `2000–2025` | **`2002-01 to 2025-09`** | Verified GPM IMERG V07B Final Run data latency coverage. |
| **Daily Extreme Indices Catalog** | `PROJECT_STATUS.md` | `Rx1day, Rx5day, R95p, R99p, CDD, CWD, SDII (2003–2024)` | **Rx1day, Rx5day, days $\ge 50\text{ mm}$, annual total (2003–2024); monsoon total, monsoon Rx1day, monsoon Rx5day, monsoon days $\ge 50\text{ mm}$ (2002–2025)** | Matched exactly to indices computed in `v3/imerg_daily_extremes_pipeline.py` and `outputs/v3/extremes/imerg_extreme_indices_trends.csv`. |
